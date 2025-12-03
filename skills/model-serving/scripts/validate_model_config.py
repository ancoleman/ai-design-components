#!/usr/bin/env python3
"""
Model Configuration Validator

Validates model deployment configurations, estimates GPU memory requirements,
and checks for common misconfigurations.
"""

import argparse
import json
import sys
from typing import Dict, List, Tuple

# Model parameter counts (billions)
MODEL_SIZES = {
    "llama-3.1-8b": 8,
    "llama-3.1-70b": 70,
    "llama-2-7b": 7,
    "llama-2-13b": 13,
    "llama-2-70b": 70,
    "mistral-7b": 7,
    "mixtral-8x7b": 47,  # 8 experts × 7B, only 2 active
    "qwen-2-7b": 7,
    "qwen-2-72b": 72,
    "phi-3-mini": 3.8,
    "phi-3-medium": 14,
}

# Bytes per parameter by precision
BYTES_PER_PARAM = {
    "fp32": 4,
    "fp16": 2,
    "bfloat16": 2,
    "int8": 1,
    "int4": 0.5,
    "awq": 0.5,
    "gptq": 0.5,
    "fp8": 1
}

class ValidationResult:
    def __init__(self):
        self.warnings: List[str] = []
        self.errors: List[str] = []
        self.info: List[str] = []

    def add_warning(self, msg: str):
        self.warnings.append(msg)

    def add_error(self, msg: str):
        self.errors.append(msg)

    def add_info(self, msg: str):
        self.info.append(msg)

    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def print_results(self):
        print("\n" + "="*60)
        print("VALIDATION RESULTS")
        print("="*60)

        if self.info:
            print("\nInfo:")
            for msg in self.info:
                print(f"  ℹ {msg}")

        if self.warnings:
            print("\nWarnings:")
            for msg in self.warnings:
                print(f"  ⚠ {msg}")

        if self.errors:
            print("\nErrors:")
            for msg in self.errors:
                print(f"  ✗ {msg}")
        else:
            print("\n✓ Configuration is valid")

        print()

def estimate_gpu_memory(
    num_params_billions: float,
    precision: str,
    include_overhead: bool = True
) -> float:
    """
    Estimate GPU memory requirements.

    Args:
        num_params_billions: Model parameters in billions
        precision: Data type (fp16, int8, etc.)
        include_overhead: Include KV cache and activation overhead

    Returns:
        Estimated GPU memory in GB
    """
    bytes_per_param = BYTES_PER_PARAM.get(precision, 2)

    # Model weights
    model_memory_gb = num_params_billions * bytes_per_param

    if include_overhead:
        # KV cache and activations (~20% overhead)
        total_memory_gb = model_memory_gb * 1.2
    else:
        total_memory_gb = model_memory_gb

    return total_memory_gb

def validate_vllm_config(config: Dict) -> ValidationResult:
    """Validate vLLM deployment configuration."""
    result = ValidationResult()

    # Required fields
    required_fields = ["model", "gpu_memory_utilization"]
    for field in required_fields:
        if field not in config:
            result.add_error(f"Missing required field: {field}")

    if not result.is_valid():
        return result

    # Extract config
    model = config.get("model", "")
    gpu_mem_util = config.get("gpu_memory_utilization", 0.9)
    max_model_len = config.get("max_model_len")
    dtype = config.get("dtype", "auto")
    quantization = config.get("quantization")
    tensor_parallel_size = config.get("tensor_parallel_size", 1)

    # GPU memory utilization check
    if gpu_mem_util < 0.5:
        result.add_warning(f"GPU memory utilization very low ({gpu_mem_util}). Consider increasing to 0.85-0.95")
    elif gpu_mem_util > 0.95:
        result.add_warning(f"GPU memory utilization very high ({gpu_mem_util}). Risk of OOM errors. Consider 0.9")

    # Model size estimation
    model_name_lower = model.lower()
    num_params = None

    for name, params in MODEL_SIZES.items():
        if name in model_name_lower:
            num_params = params
            break

    if num_params:
        # Determine precision
        if quantization in ["awq", "gptq"]:
            precision = "int4"
        elif quantization == "fp8":
            precision = "fp8"
        elif dtype in ["float16", "fp16"]:
            precision = "fp16"
        elif dtype == "bfloat16":
            precision = "bfloat16"
        else:
            precision = "fp16"  # default assumption

        gpu_memory_needed = estimate_gpu_memory(num_params, precision)
        gpu_memory_per_device = gpu_memory_needed / tensor_parallel_size

        result.add_info(f"Model size: {num_params}B parameters")
        result.add_info(f"Precision: {precision}")
        result.add_info(f"Estimated GPU memory: {gpu_memory_needed:.1f} GB total")
        result.add_info(f"Memory per GPU: {gpu_memory_per_device:.1f} GB (with {tensor_parallel_size} GPU(s))")

        # Check if fits on common GPUs
        if gpu_memory_per_device > 80:
            result.add_error(f"Model requires {gpu_memory_per_device:.1f}GB per GPU. No single GPU has this much memory.")
            result.add_info("Consider: Increase tensor_parallel_size or use quantization")
        elif gpu_memory_per_device > 40:
            result.add_warning("Model requires A100 80GB or H100 80GB")
        elif gpu_memory_per_device > 24:
            result.add_info("Model fits on A100 40GB or RTX 4090")
        elif gpu_memory_per_device > 16:
            result.add_info("Model fits on RTX 4080 or A10")
        else:
            result.add_info("Model fits on most GPUs (16GB+)")

    # Context length check
    if max_model_len:
        if max_model_len > 32768:
            result.add_warning(f"Very long context ({max_model_len}). High memory usage. Consider reducing.")
        elif max_model_len < 2048:
            result.add_warning(f"Short context ({max_model_len}). May limit use cases.")

    # Quantization check
    if quantization:
        if dtype not in ["auto", quantization]:
            result.add_warning(f"dtype={dtype} with quantization={quantization}. Use dtype=auto for quantized models.")

    # Tensor parallelism check
    if tensor_parallel_size > 1:
        if tensor_parallel_size not in [2, 4, 8]:
            result.add_warning(f"tensor_parallel_size={tensor_parallel_size}. Use powers of 2 for efficiency.")

        if num_params and num_params < 30:
            result.add_warning(f"{num_params}B model with {tensor_parallel_size} GPUs. May not need multi-GPU.")

    return result

def validate_bentoml_config(config: Dict) -> ValidationResult:
    """Validate BentoML service configuration."""
    result = ValidationResult()

    # Check batching config
    if "batchable" in config:
        if config["batchable"]:
            if "max_batch_size" not in config:
                result.add_warning("Batching enabled but max_batch_size not set")
            else:
                batch_size = config["max_batch_size"]
                if batch_size > 128:
                    result.add_warning(f"Large batch size ({batch_size}). May increase latency.")
                elif batch_size < 4:
                    result.add_warning(f"Small batch size ({batch_size}). Limited throughput benefit.")

            if "max_latency_ms" not in config:
                result.add_warning("Batching enabled but max_latency_ms not set")

    # Check resource allocation
    if "resources" in config:
        resources = config["resources"]

        if "cpu" in resources:
            cpu = resources["cpu"]
            if isinstance(cpu, str):
                cpu = float(cpu)
            if cpu < 1:
                result.add_warning(f"Low CPU allocation ({cpu}). May limit performance.")

        if "memory" in resources:
            memory = resources["memory"]
            # Parse memory (e.g., "4Gi")
            if isinstance(memory, str):
                if memory.endswith("Gi"):
                    mem_gb = float(memory[:-2])
                    if mem_gb < 2:
                        result.add_warning(f"Low memory allocation ({memory}). May cause OOM.")

    result.add_info("BentoML configuration validated")
    return result

def main():
    parser = argparse.ArgumentParser(description="Validate model deployment configuration")

    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to configuration JSON file"
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["vllm", "bentoml"],
        default="vllm",
        help="Deployment type"
    )

    args = parser.parse_args()

    # Load configuration
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found: {args.config}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file: {e}")
        sys.exit(1)

    print(f"Validating {args.type} configuration from {args.config}")

    # Validate based on type
    if args.type == "vllm":
        result = validate_vllm_config(config)
    elif args.type == "bentoml":
        result = validate_bentoml_config(config)
    else:
        print(f"Unknown deployment type: {args.type}")
        sys.exit(1)

    # Print results
    result.print_results()

    # Exit with error code if validation failed
    sys.exit(0 if result.is_valid() else 1)

if __name__ == "__main__":
    main()
