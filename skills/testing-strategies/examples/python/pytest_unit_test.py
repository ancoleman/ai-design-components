"""
Unit Testing Examples with pytest

Demonstrates: Unit testing pure functions and business logic

Dependencies:
    pip install pytest

Usage:
    pytest pytest_unit_test.py -v
"""

import pytest
from typing import List, Dict
from decimal import Decimal


# ====================
# System Under Test
# ====================

class CartItem:
    def __init__(self, price: float, quantity: int, taxable: bool = True):
        self.price = price
        self.quantity = quantity
        self.taxable = taxable


def calculate_total(items: List[CartItem], tax_rate: float = 0) -> float:
    """Calculate cart total with tax"""
    subtotal = sum(item.price * item.quantity for item in items)
    taxable_amount = sum(
        item.price * item.quantity for item in items if item.taxable
    )
    tax = taxable_amount * tax_rate
    return round(subtotal + tax, 2)


def format_currency(amount: float, locale: str = 'en_US', currency: str = 'USD') -> str:
    """Format amount as currency string"""
    # Simplified implementation (production would use babel/locale)
    symbol = {'USD': '$', 'EUR': '€', 'JPY': '¥'}.get(currency, '$')
    if locale == 'de_DE':
        return f"{amount:,.2f} {symbol}".replace(',', 'X').replace('.', ',').replace('X', '.')
    return f"{symbol}{amount:,.2f}"


def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return bool(re.match(pattern, email))


# ====================
# Unit Tests
# ====================

class TestCalculateTotal:
    """Unit tests for calculate_total function"""

    def test_single_item(self):
        items = [CartItem(price=10, quantity=1)]
        assert calculate_total(items) == 10

    def test_multiple_items(self):
        items = [
            CartItem(price=10, quantity=2),
            CartItem(price=5, quantity=1)
        ]
        assert calculate_total(items) == 25

    def test_applies_tax_rate(self):
        items = [CartItem(price=10, quantity=1)]
        assert calculate_total(items, tax_rate=0.1) == 11

    def test_non_taxable_items(self):
        items = [
            CartItem(price=10, quantity=1, taxable=True),
            CartItem(price=5, quantity=1, taxable=False)
        ]
        # Only $10 is taxed: 10 + 1 + 5 = 16
        assert calculate_total(items, tax_rate=0.1) == 16

    def test_rounds_to_two_decimals(self):
        items = [CartItem(price=10.99, quantity=1)]
        # 10.99 * 1.075 = 11.81425 → 11.81
        assert calculate_total(items, tax_rate=0.075) == 11.81

    def test_empty_cart(self):
        assert calculate_total([]) == 0

    def test_zero_quantity(self):
        items = [CartItem(price=10, quantity=0)]
        assert calculate_total(items) == 0


class TestFormatCurrency:
    """Unit tests for format_currency function"""

    def test_formats_usd(self):
        assert format_currency(1234.56) == '$1,234.56'

    def test_formats_eur_german_locale(self):
        result = format_currency(1234.56, locale='de_DE', currency='EUR')
        assert '€' in result

    def test_handles_zero(self):
        assert format_currency(0) == '$0.00'

    def test_handles_negative(self):
        assert format_currency(-50.25) == '-$50.25'

    def test_rounds_to_currency_precision(self):
        assert format_currency(10.999) == '$11.00'


class TestValidateEmail:
    """Unit tests for validate_email function"""

    def test_valid_email(self):
        assert validate_email('user@example.com') is True

    def test_email_with_plus(self):
        assert validate_email('user+tag@example.com') is True

    def test_email_with_subdomain(self):
        assert validate_email('user@mail.example.com') is True

    def test_rejects_no_at(self):
        assert validate_email('userexample.com') is False

    def test_rejects_no_domain(self):
        assert validate_email('user@') is False

    def test_rejects_no_username(self):
        assert validate_email('@example.com') is False

    def test_rejects_spaces(self):
        assert validate_email('user @example.com') is False

    def test_rejects_empty(self):
        assert validate_email('') is False


# ====================
# Testing with Fixtures
# ====================

@pytest.fixture
def sample_cart():
    """Fixture: Sample cart for testing"""
    return [
        CartItem(price=19.99, quantity=2, taxable=True),
        CartItem(price=5.00, quantity=1, taxable=False),
        CartItem(price=12.50, quantity=3, taxable=True)
    ]


def test_calculates_subtotal_correctly(sample_cart):
    assert calculate_total(sample_cart, tax_rate=0) == 82.48


def test_applies_tax_to_taxable_items_only(sample_cart):
    # Taxable: (19.99 * 2) + (12.50 * 3) = 77.48
    # Tax: 77.48 * 0.08 = 6.20
    # Total: 82.48 + 6.20 = 88.68
    assert calculate_total(sample_cart, tax_rate=0.08) == 88.68


# ====================
# Parametrized Tests
# ====================

@pytest.mark.parametrize("amount,locale,currency,expected", [
    (0, 'en_US', 'USD', '$0.00'),
    (1234.56, 'en_US', 'USD', '$1,234.56'),
    (-100, 'en_US', 'USD', '-$100.00'),
    (1000, 'en_US', 'JPY', '¥1,000.00'),
])
def test_format_currency_parametrized(amount, locale, currency, expected):
    assert format_currency(amount, locale, currency) == expected


@pytest.mark.parametrize("email,expected", [
    ('valid@example.com', True),
    ('user+tag@example.com', True),
    ('user@mail.example.com', True),
    ('invalid', False),
    ('no@domain', False),
    ('@example.com', False),
    ('user @example.com', False),
    ('', False),
])
def test_validate_email_parametrized(email, expected):
    assert validate_email(email) == expected


# ====================
# Edge Case Testing
# ====================

class TestEdgeCases:
    """Edge case tests"""

    def test_very_large_numbers(self):
        items = [CartItem(price=999999.99, quantity=1)]
        assert calculate_total(items) == 999999.99

    def test_very_small_prices(self):
        items = [CartItem(price=0.01, quantity=100)]
        assert calculate_total(items) == 1.0

    def test_floating_point_precision(self):
        items = [CartItem(price=0.1, quantity=3)]
        # Should be 0.3, not 0.30000000000000004
        assert calculate_total(items) == 0.3


# ====================
# Testing Exceptions
# ====================

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def test_divide_raises_on_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


def test_divide_normal_case():
    assert divide(10, 2) == 5.0


# ====================
# Fixture Scopes
# ====================

@pytest.fixture(scope='session')
def expensive_setup():
    """Session-scoped fixture (runs once per test session)"""
    print("\nExpensive setup (once per session)")
    return {'config': 'loaded'}


@pytest.fixture(scope='module')
def module_setup():
    """Module-scoped fixture (runs once per test module)"""
    print("\nModule setup (once per module)")
    return {'data': 'module_data'}


@pytest.fixture(scope='function')  # Default scope
def function_setup():
    """Function-scoped fixture (runs once per test function)"""
    print("\nFunction setup (per test)")
    return {'temp': 'data'}


def test_uses_fixtures(expensive_setup, module_setup, function_setup):
    assert expensive_setup['config'] == 'loaded'
    assert module_setup['data'] == 'module_data'
    assert function_setup['temp'] == 'data'
