#!/usr/bin/env python3

"""
Token calculation utilities for AI chat interfaces
Estimates token usage for various AI models
"""

import json
import sys
import re
from typing import Dict, List, Union, Tuple


class TokenCalculator:
    """Calculate token estimates for different AI models"""

    # Approximate tokens per character for different models
    MODEL_RATIOS = {
        'gpt-4': 0.25,          # ~4 chars per token
        'gpt-4-turbo': 0.25,
        'gpt-3.5-turbo': 0.27,  # ~3.7 chars per token
        'claude-3-opus': 0.24,  # ~4.2 chars per token
        'claude-3-sonnet': 0.24,
        'claude-3-haiku': 0.24,
        'default': 0.25
    }

    # Token limits for different models
    MODEL_LIMITS = {
        'gpt-4': 8192,
        'gpt-4-turbo': 128000,
        'gpt-4-32k': 32768,
        'gpt-3.5-turbo': 4096,
        'gpt-3.5-turbo-16k': 16384,
        'claude-3-opus': 200000,
        'claude-3-sonnet': 200000,
        'claude-3-haiku': 200000,
        'default': 4096
    }

    def __init__(self, model: str = 'default'):
        """Initialize calculator for specific model"""
        self.model = model
        self.ratio = self.MODEL_RATIOS.get(model, self.MODEL_RATIOS['default'])
        self.limit = self.MODEL_LIMITS.get(model, self.MODEL_LIMITS['default'])

    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text
        Uses character-based approximation for speed
        """
        if not text:
            return 0

        # Basic character count method
        char_count = len(text)
        base_tokens = int(char_count * self.ratio)

        # Adjust for special content
        adjustments = 0

        # Code blocks typically use more tokens
        code_blocks = len(re.findall(r'```[\s\S]*?```', text))
        adjustments += code_blocks * 10

        # URLs use more tokens
        urls = len(re.findall(r'https?://\S+', text))
        adjustments += urls * 5

        # Numbers and special characters
        numbers = len(re.findall(r'\d+', text))
        adjustments += numbers * 0.5

        # Punctuation typically increases token count
        punctuation = len(re.findall(r'[.,!?;:]', text))
        adjustments += punctuation * 0.1

        return int(base_tokens + adjustments)

    def count_message_tokens(self, message: Dict[str, str]) -> int:
        """Count tokens in a message object"""
        # Message overhead (role, formatting)
        overhead = 4

        # Content tokens
        content_tokens = self.count_tokens(message.get('content', ''))

        # Role tokens
        role_tokens = 1

        return overhead + content_tokens + role_tokens

    def count_conversation_tokens(self, messages: List[Dict[str, str]]) -> Dict[str, any]:
        """
        Count tokens in entire conversation
        Returns detailed breakdown
        """
        total_tokens = 0
        message_counts = []

        for msg in messages:
            tokens = self.count_message_tokens(msg)
            total_tokens += tokens
            message_counts.append({
                'role': msg.get('role', 'user'),
                'tokens': tokens,
                'preview': msg.get('content', '')[:50] + '...' if len(msg.get('content', '')) > 50 else msg.get('content', '')
            })

        return {
            'total_tokens': total_tokens,
            'message_count': len(messages),
            'average_tokens_per_message': total_tokens / len(messages) if messages else 0,
            'model_limit': self.limit,
            'tokens_remaining': self.limit - total_tokens,
            'percentage_used': (total_tokens / self.limit) * 100,
            'messages': message_counts
        }

    def estimate_remaining_messages(self, current_tokens: int, avg_message_tokens: int = 50) -> int:
        """Estimate how many more messages can fit"""
        remaining_tokens = self.limit - current_tokens
        if remaining_tokens <= 0:
            return 0
        return remaining_tokens // avg_message_tokens

    def suggest_summarization_point(self, messages: List[Dict[str, str]]) -> Tuple[int, str]:
        """
        Suggest where to summarize conversation
        Returns (index, reason)
        """
        conversation_stats = self.count_conversation_tokens(messages)

        if conversation_stats['percentage_used'] < 70:
            return (-1, "No summarization needed yet")

        # Find natural break point (topic change, time gap, etc.)
        total_tokens = 0
        target_tokens = self.limit * 0.3  # Keep 30% of context

        for i in range(len(messages) - 1, -1, -1):
            tokens = self.count_message_tokens(messages[i])
            total_tokens += tokens

            if total_tokens >= target_tokens:
                # Found cutoff point
                return (i, f"Summarize messages 0 to {i-1}, keep {i} to {len(messages)-1}")

        return (len(messages) // 2, "Summarize first half of conversation")

    def format_token_display(self, tokens: int) -> Dict[str, str]:
        """Format tokens for user-friendly display"""
        words = tokens * 0.75  # Rough estimate: 1 token ≈ 0.75 words
        pages = words / 250  # Rough estimate: 250 words per page

        return {
            'tokens': f"{tokens:,}",
            'words': f"~{int(words):,} words",
            'pages': f"~{pages:.1f} pages",
            'percentage': f"{(tokens / self.limit * 100):.1f}%",
            'remaining': f"{self.limit - tokens:,} tokens left"
        }


class ContextOptimizer:
    """Optimize context to fit within token limits"""

    def __init__(self, calculator: TokenCalculator):
        self.calculator = calculator

    def compress_messages(self, messages: List[Dict[str, str]], target_tokens: int) -> List[Dict[str, str]]:
        """Compress messages to fit within target token count"""
        compressed = []
        current_tokens = 0

        # Always keep system messages
        system_messages = [m for m in messages if m.get('role') == 'system']
        for msg in system_messages:
            compressed.append(msg)
            current_tokens += self.calculator.count_message_tokens(msg)

        # Keep recent messages in full
        recent_count = min(10, len(messages) // 4)
        recent_messages = messages[-recent_count:] if recent_count > 0 else []

        for msg in recent_messages:
            if msg not in compressed:
                compressed.append(msg)
                current_tokens += self.calculator.count_message_tokens(msg)

        # Compress middle messages if needed
        remaining_tokens = target_tokens - current_tokens
        middle_messages = [m for m in messages if m not in compressed and m not in recent_messages]

        if middle_messages and remaining_tokens > 100:
            summary = self.create_summary(middle_messages, remaining_tokens)
            compressed.insert(len(system_messages), {
                'role': 'system',
                'content': f"[Summary of {len(middle_messages)} previous messages]\n{summary}"
            })

        return compressed

    def create_summary(self, messages: List[Dict[str, str]], max_tokens: int) -> str:
        """Create a summary of messages within token limit"""
        summary_points = []

        # Extract key information
        for msg in messages:
            content = msg.get('content', '')

            # Extract questions
            questions = re.findall(r'[^.!?]*\?', content)
            if questions:
                summary_points.append(f"Question: {questions[0][:100]}")

            # Extract code blocks
            code_blocks = re.findall(r'```[\s\S]*?```', content)
            if code_blocks:
                summary_points.append(f"Code discussed: {len(code_blocks)} blocks")

            # Extract key phrases (simplified)
            if 'error' in content.lower():
                summary_points.append("Error discussed")
            if 'solution' in content.lower() or 'fixed' in content.lower():
                summary_points.append("Solution provided")

        # Build summary within token limit
        summary = "Previous conversation covered:\n"
        for point in summary_points:
            test_summary = summary + f"- {point}\n"
            if self.calculator.count_tokens(test_summary) < max_tokens:
                summary = test_summary
            else:
                break

        return summary

    def prioritize_messages(self, messages: List[Dict[str, str]]) -> List[Tuple[int, Dict[str, str]]]:
        """
        Assign priority scores to messages
        Returns list of (priority, message) tuples
        """
        prioritized = []

        for i, msg in enumerate(messages):
            priority = 0

            # System messages have highest priority
            if msg.get('role') == 'system':
                priority += 100

            # Recent messages have higher priority
            recency_score = (i / len(messages)) * 50
            priority += recency_score

            # Messages with code have higher priority
            if '```' in msg.get('content', ''):
                priority += 20

            # Questions have higher priority
            if '?' in msg.get('content', ''):
                priority += 15

            # Longer messages might be more detailed
            content_length = len(msg.get('content', ''))
            if content_length > 500:
                priority += 10

            # User messages that got long responses are important
            if msg.get('role') == 'user' and i < len(messages) - 1:
                next_msg = messages[i + 1]
                if next_msg.get('role') == 'assistant' and len(next_msg.get('content', '')) > 500:
                    priority += 25

            prioritized.append((priority, msg))

        return sorted(prioritized, key=lambda x: x[0], reverse=True)


def main():
    """CLI interface for token calculation"""
    import argparse

    parser = argparse.ArgumentParser(description='Calculate tokens for AI chat messages')
    parser.add_argument('--model', default='gpt-4', help='AI model name')
    parser.add_argument('--file', help='JSON file with messages')
    parser.add_argument('--text', help='Text to count tokens for')
    parser.add_argument('--optimize', action='store_true', help='Optimize context to fit')
    parser.add_argument('--target', type=int, help='Target token count for optimization')

    args = parser.parse_args()

    calculator = TokenCalculator(args.model)

    if args.text:
        # Count tokens in text
        tokens = calculator.count_tokens(args.text)
        display = calculator.format_token_display(tokens)
        print(json.dumps(display, indent=2))

    elif args.file:
        # Count tokens in conversation file
        with open(args.file, 'r') as f:
            messages = json.load(f)

        stats = calculator.count_conversation_tokens(messages)

        if args.optimize:
            # Optimize context
            optimizer = ContextOptimizer(calculator)
            target = args.target or calculator.limit * 0.8

            optimized = optimizer.compress_messages(messages, target)
            optimized_stats = calculator.count_conversation_tokens(optimized)

            print(json.dumps({
                'original': stats,
                'optimized': optimized_stats,
                'compression_ratio': optimized_stats['total_tokens'] / stats['total_tokens'],
                'messages_removed': len(messages) - len(optimized)
            }, indent=2))
        else:
            # Just show stats
            print(json.dumps(stats, indent=2))

            # Suggest summarization point
            cutoff, reason = calculator.suggest_summarization_point(messages)
            print(f"\nSummarization suggestion: {reason}")

    else:
        # Interactive mode
        print(f"Token Calculator - Model: {args.model} (Limit: {calculator.limit:,} tokens)")
        print("Enter text to count tokens (Ctrl+D to finish):")

        try:
            text = sys.stdin.read()
            tokens = calculator.count_tokens(text)
            display = calculator.format_token_display(tokens)

            print("\nToken count analysis:")
            for key, value in display.items():
                print(f"  {key}: {value}")

        except KeyboardInterrupt:
            print("\nCancelled")


if __name__ == '__main__':
    main()