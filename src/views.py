import json
import logging
import math
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from dateutil.parser import parse as parse_date
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "operations.csv"
SETTINGS_PATH = Path(__file__).resolve().parent.parent / "user_settings.json"
API_KEY = os.getenv("API_KEY")


def parse_date_(date_str: str) -> datetime:
    logging.debug(f"Парсинг даты: {date_str}")
    return pd.to_datetime(date_str)


def filter_operations_by_date(
    date_str: str, filepath: str = r"C:\Users\PC\PycharmProjects\course_work_1\data\operations.csv"
) -> pd.DataFrame:
def filter_operations_by_date(date_str: str, filepath: str = str(DATA_PATH)) -> pd.DataFrame:
    """Возвращает операции из CSV-файла в период с начала месяца по указанную дату."""
    current_date = parse_date(date_str)
    start_date = current_date.replace(day=1)

    logging.info(f"Чтение данных операций из: {filepath}")
    df = pd.read_csv(filepath, sep=",", parse_dates=["Дата операции"], dayfirst=True)

    df.rename(
@@ -36,15 +42,18 @@ def filter_operations_by_date(
        },
        inplace=True,
    )

    mask = (df["date"] >= start_date) & (df["date"] <= current_date)
    filtered_df = df.loc[mask]
    logging.info(f"Найдено операций в периоде: {len(filtered_df)}")

    return filtered_df


def get_greeting(current_time: datetime) -> str:
    """Функция для приветствия"""
    hour = current_time.hour
    logging.debug(f"Определение приветствия по времени: {hour} ч.")

    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
@@ -56,19 +65,21 @@ def get_greeting(current_time: datetime) -> str:


def get_card_stats(df: pd.DataFrame) -> list[dict]:
    """Функция для подсчёта по картам с кешбэком 1 рубль за каждые 100 рублей."""
    card_stats = []
    grouped = df[df["amount"] < 0].groupby("card")

    for card, group in grouped:
        total_spent = round(-group["amount"].sum(), 2)
        cashback = math.floor(total_spent / 100)
        card_stats.append({"last_digits": str(card)[-4:], "total_spent": total_spent, "cashback": cashback})

    logging.info(f"Статистика по картам рассчитана для {len(card_stats)} карт")
    return card_stats


def get_top_transactions(df: pd.DataFrame) -> list[dict]:
    """Функция для топ-5 транзакций по сумме платежа"""
    top_df = df.sort_values(by="payment_amount", key=abs, ascending=False).head(5)
    logging.info("Сформирован топ-5 транзакций")
    return [
        {
            "date": row["date"].strftime("%d.%m.%Y"),
@@ -82,33 +93,37 @@ def get_top_transactions(df: pd.DataFrame) -> list[dict]:

def get_stock_prices(api_key: str | None = None) -> list[dict]:
    if api_key is None:
        raise RuntimeError("API_KEY not set in environment variables")
    """Получает цены акций с Alpha Vantage по списку из user_settings.json"""
    with open(r"C:\Users\PC\PycharmProjects\course_work_1\user_settings.json", "r", encoding="utf-8") as f:
        raise RuntimeError("API_KEY не задано в переменных окружения")

    logging.info("Получение цен акций через Alpha Vantage")
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        settings = json.load(f)

    stocks = settings.get("user_stocks", [])
    result = []

    for symbol in stocks:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        try:
            response = requests.get(url)
            data = response.json()
            price = float(data["Global Quote"]["05. price"])
            result.append({"stock": symbol, "price": round(price, 2)})
        except (KeyError, ValueError):
            logging.warning(f"Не удалось получить цену для акции: {symbol}")
            result.append({"stock": symbol, "price": None})

    return result


def get_currency_rates() -> list[dict]:
    """Получает курсы валют из user_settings.json через exchangerate.host"""
    with open(r"C:\Users\PC\PycharmProjects\course_work_1\user_settings.json", "r", encoding="utf-8") as f:
    logging.info("Получение курсов валют через exchangerate.host")
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        settings = json.load(f)
    currencies = settings.get("user_currencies", [])

    currencies = settings.get("user_currencies", [])
    base_url = "https://api.exchangerate.host/latest?base=RUB"

    response = requests.get(base_url)
    data = response.json()
    rates = data.get("rates", {})
@@ -117,15 +132,16 @@ def get_currency_rates() -> list[dict]:
    for currency in currencies:
        rate = rates.get(currency)
        if rate:
            result.append({"currency": currency, "rate": round(1 / rate, 2)})  # RUB → USD (обратный)
            result.append({"currency": currency, "rate": round(1 / rate, 2)})
        else:
            logging.warning(f"Курс для валюты {currency} не найден")
            result.append({"currency": currency, "rate": None})

    return result


def generate_main_page_data(date_str: str) -> dict:
    """Главная функция для генерации JSON-ответа по входной дате"""
    logging.info(f"Генерация главной страницы на дату: {date_str}")
    current_date = parse_date(date_str)
    df = filter_operations_by_date(date_str)

@@ -134,7 +150,7 @@ def generate_main_page_data(date_str: str) -> dict:
        "cards": get_card_stats(df),
        "top_transactions": get_top_transactions(df),
        "currency_rates": get_currency_rates(),
        "stock_prices": get_stock_prices(),
        "stock_prices": get_stock_prices(api_key=API_KEY),
    }