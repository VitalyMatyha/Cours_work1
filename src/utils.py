from datetime import datetime

def mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты.
    Пример: 1234567812345678 → 1234 56** **** 5678
    """
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def mask_account_number(account_number: str) -> str:
    """
    Маскирует номер счёта.
    Пример: 40817810099910004312 → **4312
    """
    return f"**{account_number[-4:]}"


def format_date(date_str: str) -> str:
    """
    Форматирует дату из ISO-строки.
    Пример: 2021-05-01T12:30:00 → 01.05.2021
    """
    return datetime.fromisoformat(date_str).strftime("%d.%m.%Y")


def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Возвращает список операций с нужным статусом.
    По умолчанию оставляет только выполненные (EXECUTED).
    """
    return [op for op in operations if op.get("state") == state]


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует операции по дате.
    По умолчанию от новых к старым.
    """
    return sorted(operations, key=lambda x: x["date"], reverse=reverse)
