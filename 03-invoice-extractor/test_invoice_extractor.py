"""Tests for the validation logic. They run without an API key or internet.

Run with:  pytest
"""

from invoice_extractor import parse_amount, validate


def valid_invoice(**overrides):
    data = {
        "vendor": "Acme HVAC Supply",
        "invoice_number": "INV-1001",
        "invoice_date": "2026-10-01",
        "total": 216.0,
        "tax": 16.0,
        "currency": "USD",
        "line_items": [
            {"description": "Filter", "quantity": 2, "unit_price": 50.0, "amount": 100.0},
            {"description": "Labor", "quantity": 1, "unit_price": 100.0, "amount": 100.0},
        ],
    }
    data.update(overrides)
    return data


def test_valid_invoice_has_no_issues():
    assert validate(valid_invoice()) == []


def test_missing_required_field_is_flagged():
    assert "Missing vendor" in validate(valid_invoice(vendor=None))


def test_total_mismatch_is_flagged():
    issues = validate(valid_invoice(total=300.0))
    assert any("Total mismatch" in i for i in issues)


def test_small_rounding_difference_is_accepted():
    assert validate(valid_invoice(total=216.03)) == []


def test_money_strings_are_parsed():
    assert validate(valid_invoice(total="$216.00", tax="16")) == []


def test_invalid_total_is_flagged_instead_of_crashing():
    issues = validate(valid_invoice(total="two hundred"))
    assert any("Invalid total" in i for i in issues)


def test_line_item_math_is_checked():
    items = [{"description": "Filter", "quantity": 2, "unit_price": 50.0, "amount": 200.0}]
    issues = validate(valid_invoice(line_items=items, total=216.0))
    assert any("Line 1" in i for i in issues)


def test_invoice_without_line_items_needs_review():
    issues = validate(valid_invoice(line_items=[]))
    assert any("No line items" in i for i in issues)


def test_parse_amount():
    assert parse_amount("$1,200.50") == 1200.50
    assert parse_amount(10) == 10.0
    assert parse_amount("abc") is None
    assert parse_amount(None) is None
    assert parse_amount(True) is None
