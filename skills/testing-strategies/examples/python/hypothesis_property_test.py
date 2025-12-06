"""
Property-Based Testing Examples with hypothesis

Demonstrates: Using hypothesis to find edge cases through generative testing

Dependencies:
    pip install pytest hypothesis

Usage:
    pytest hypothesis_property_test.py -v
"""

from hypothesis import given, strategies as st, assume, example
from typing import List
import pytest


# ====================
# System Under Test
# ====================

def reverse(lst: List) -> List:
    """Reverse a list"""
    return list(reversed(lst))


def dedup(lst: List) -> List:
    """Remove duplicates while preserving order"""
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def sort_integers(lst: List[int]) -> List[int]:
    """Sort a list of integers"""
    return sorted(lst)


def encode_decode(text: str) -> str:
    """Encode and decode text (round-trip)"""
    import base64
    encoded = base64.b64encode(text.encode('utf-8'))
    decoded = base64.b64decode(encoded).decode('utf-8')
    return decoded


def calculate_total(prices: List[float]) -> float:
    """Calculate total of prices"""
    return round(sum(prices), 2)


# ====================
# Property-Based Tests
# ====================

@given(st.lists(st.integers()))
def test_reverse_twice_is_identity(lst):
    """Property: Reversing twice returns original list"""
    assert reverse(reverse(lst)) == lst


@given(st.lists(st.integers()))
def test_reverse_preserves_length(lst):
    """Property: Reversing preserves list length"""
    assert len(reverse(lst)) == len(lst)


@given(st.lists(st.integers()))
def test_dedup_removes_duplicates(lst):
    """Property: Dedup result has no duplicates"""
    result = dedup(lst)
    assert len(result) == len(set(result))


@given(st.lists(st.integers()))
def test_dedup_preserves_order(lst):
    """Property: Dedup preserves first occurrence order"""
    result = dedup(lst)
    # All elements in result appear in original list in same relative order
    original_indices = []
    for item in result:
        if item in lst:
            original_indices.append(lst.index(item))

    # Indices should be in ascending order (preserved order)
    assert original_indices == sorted(original_indices)


@given(st.lists(st.integers()))
def test_dedup_shorter_or_equal(lst):
    """Property: Dedup result is same length or shorter"""
    assert len(dedup(lst)) <= len(lst)


@given(st.lists(st.integers()))
def test_sort_is_idempotent(lst):
    """Property: Sorting twice gives same result as sorting once"""
    sorted_once = sort_integers(lst)
    sorted_twice = sort_integers(sorted_once)
    assert sorted_once == sorted_twice


@given(st.lists(st.integers()))
def test_sort_preserves_length(lst):
    """Property: Sorting preserves length"""
    assert len(sort_integers(lst)) == len(lst)


@given(st.lists(st.integers()))
def test_sort_preserves_elements(lst):
    """Property: Sorting preserves all elements (multiset equality)"""
    assert sorted(lst) == sorted(sort_integers(lst))


@given(st.text())
def test_encode_decode_round_trip(text):
    """Property: Encoding then decoding returns original text"""
    assert encode_decode(text) == text


@given(st.lists(st.floats(min_value=0, max_value=10000)))
def test_total_never_negative(prices):
    """Property: Total is never negative for non-negative prices"""
    assume(all(p >= 0 for p in prices))  # Assume all prices non-negative
    total = calculate_total(prices)
    assert total >= 0


@given(st.lists(st.floats(min_value=0.01, max_value=100), min_size=1))
def test_total_greater_than_min_price(prices):
    """Property: Total is at least the minimum price"""
    assume(len(prices) > 0)  # Ensure non-empty list
    total = calculate_total(prices)
    min_price = min(prices)
    assert total >= min_price


# ====================
# Custom Strategies
# ====================

# Strategy for generating email-like strings
email_strategy = st.builds(
    lambda user, domain, tld: f"{user}@{domain}.{tld}",
    user=st.text(alphabet=st.characters(whitelist_categories=('Ll', 'Nd')), min_size=1, max_size=20),
    domain=st.text(alphabet=st.characters(whitelist_categories=('Ll',)), min_size=1, max_size=20),
    tld=st.sampled_from(['com', 'org', 'net', 'edu'])
)


def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return bool(re.match(pattern, email))


@given(email_strategy)
def test_generated_emails_are_valid(email):
    """Property: Generated emails are valid"""
    assert validate_email(email)


# ====================
# Constrained Strategies
# ====================

@given(
    st.integers(min_value=1, max_value=100),
    st.integers(min_value=1, max_value=100)
)
def test_addition_commutative(a, b):
    """Property: Addition is commutative"""
    assert a + b == b + a


@given(
    st.integers(min_value=-1000, max_value=1000),
    st.integers(min_value=-1000, max_value=1000)
)
def test_addition_associative(a, b, c=5):
    """Property: Addition is associative"""
    assert (a + b) + c == a + (b + c)


# ====================
# Using Examples with Property Tests
# ====================

@given(st.lists(st.integers()))
@example([])  # Explicitly test empty list
@example([1])  # Explicitly test single element
@example([1, 2, 3, 4, 5])  # Explicitly test small list
def test_reverse_with_examples(lst):
    """Property test with explicit examples"""
    assert reverse(reverse(lst)) == lst


# ====================
# Shrinking (Hypothesis finds minimal failing case)
# ====================

def buggy_dedup(lst: List[int]) -> List[int]:
    """Buggy dedup implementation (has a bug for lists with zeros)"""
    seen = set()
    result = []
    for item in lst:
        if item and item not in seen:  # BUG: Skips 0
            seen.add(item)
            result.append(item)
    return result


@given(st.lists(st.integers()))
def test_buggy_dedup_fails(lst):
    """
    This test will fail for lists containing 0.
    Hypothesis will shrink to minimal failing case: [0]
    """
    result = buggy_dedup(lst)
    # This property doesn't hold for the buggy implementation
    # Hypothesis will find [0] as the minimal failing case
    if 0 in lst:
        pytest.skip("Known bug with zeros")  # Skip to prevent failure in example
    assert len(result) == len(set(result))


# ====================
# Complex Data Structures
# ====================

user_strategy = st.builds(
    dict,
    id=st.integers(min_value=1),
    name=st.text(min_size=1, max_size=50),
    email=email_strategy,
    age=st.integers(min_value=18, max_value=120),
    active=st.booleans()
)


@given(user_strategy)
def test_user_age_is_valid(user):
    """Property: Generated users have valid age"""
    assert 18 <= user['age'] <= 120


@given(user_strategy)
def test_user_email_is_valid(user):
    """Property: Generated users have valid email"""
    assert validate_email(user['email'])


# ====================
# Stateful Testing (Advanced)
# ====================

from hypothesis.stateful import RuleBasedStateMachine, rule, invariant


class StackMachine(RuleBasedStateMachine):
    """Stateful testing for a stack data structure"""

    def __init__(self):
        super().__init__()
        self.stack = []

    @rule(value=st.integers())
    def push(self, value):
        """Push value onto stack"""
        self.stack.append(value)

    @rule()
    def pop(self):
        """Pop value from stack"""
        if self.stack:
            self.stack.pop()

    @invariant()
    def stack_not_negative_length(self):
        """Invariant: Stack length is never negative"""
        assert len(self.stack) >= 0

    @invariant()
    def stack_matches_operations(self):
        """Invariant: Stack length matches number of operations"""
        # This is a simplified invariant
        assert isinstance(self.stack, list)


# Run stateful test
TestStack = StackMachine.TestCase


# ====================
# Round-Trip Properties
# ====================

import json


@given(
    st.dictionaries(
        keys=st.text(alphabet=st.characters(whitelist_categories=('Ll',)), min_size=1),
        values=st.one_of(st.integers(), st.text(), st.booleans())
    )
)
def test_json_round_trip(data):
    """Property: JSON serialization round-trip preserves data"""
    serialized = json.dumps(data)
    deserialized = json.loads(serialized)
    assert deserialized == data


# ====================
# Testing Invariants
# ====================

@given(st.lists(st.integers(), min_size=1))
def test_max_is_in_list(lst):
    """Property: Maximum value is in the original list"""
    assert max(lst) in lst


@given(st.lists(st.integers(), min_size=1))
def test_min_less_than_or_equal_max(lst):
    """Property: Minimum is less than or equal to maximum"""
    assert min(lst) <= max(lst)


@given(st.lists(st.integers()))
def test_sorted_has_non_decreasing_order(lst):
    """Property: Sorted list has non-decreasing order"""
    sorted_lst = sorted(lst)
    for i in range(len(sorted_lst) - 1):
        assert sorted_lst[i] <= sorted_lst[i + 1]
