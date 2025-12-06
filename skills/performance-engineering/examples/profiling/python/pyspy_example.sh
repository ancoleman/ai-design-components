#!/bin/bash
#
# py-spy Profiling Example
#
# Demonstrates: CPU profiling with py-spy (production-safe)
#
# Usage:
#   ./pyspy_example.sh
#
# Requirements:
#   pip install py-spy

# Profile running Python process
echo "=== Profile running process (30 seconds) ==="
# Replace <PID> with actual process ID
# py-spy record -o profile.svg --pid <PID> --duration 30

# Profile command
echo "=== Profile Python script ==="
py-spy record -o profile.svg -- python app.py

# Top-like view of running process
echo "=== Top view (press Ctrl+C to stop) ==="
# py-spy top --pid <PID>

# Flamegraph output (Speedscope format)
echo "=== Generate speedscope flamegraph ==="
py-spy record -o profile.speedscope.json --format speedscope -- python app.py

# Open in browser: https://www.speedscope.app/
# Drag and drop profile.speedscope.json

echo "Done! View profile.svg in browser"
