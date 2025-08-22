import pytest
from src.utils import (
    mask_card_number,
    mask_account_number,
    format_date,
    filter_by_state,
    sort_by_date,
)


def test_mask_card_number():
    assert mask_card_number("1234567812345678") == "1234 56** **** 5678"


def test_mask_account_number():
    assert mask_account_number("40817810099910004312") == "**4312"


def test_format_date():
    assert format_date("2021-05-01T12:30:00") == "01.05.2021"


def test_filter_by_state():
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]
    result = filter_by_state(data)
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_sort_by_date():
    data = [
        {"id": 1, "date": "2021-05-01T12:30:00"},
        {"id": 2, "date": "2021-06-01T12:30:00"},
    ]
    result = sort_by_date(data)
    assert result[0]["id"] == 2  # сначала более новая дата
