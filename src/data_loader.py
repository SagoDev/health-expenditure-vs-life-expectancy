"""Data loader module for fetching and processing World Bank data."""

# src/data_loader.py

from typing import Dict
import os
import requests
import pandas as pd
from src.config import BASE_URL, RAW_DATA_PATH, START_YEAR, END_YEAR


def fetch_indicator(indicator_code: str) -> pd.DataFrame:
    """
    Fetch data for a given World Bank indicator.
    Includes validation of API-level errors.
    """

    url = (
        f"{BASE_URL}/{indicator_code}"
        f"?format=json&per_page=20000"
        f"&date={START_YEAR}:{END_YEAR}"
    )

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")

    data = response.json()

    # Detect API error structure
    if isinstance(data, list) and len(data) == 1 and "message" in data[0]:
        error_msg = data[0]["message"][0]["value"]
        raise Exception(f"World Bank API error: {error_msg}")

    if len(data) < 2:
        raise Exception("Unexpected API response structure.")

    df = pd.json_normalize(data[1])

    return df


def save_raw_data(df: pd.DataFrame, indicator_name: str) -> None:
    """
    Save raw data to disk.
    """

    os.makedirs(RAW_DATA_PATH, exist_ok=True)

    file_path = os.path.join(RAW_DATA_PATH, f"{indicator_name}.csv")

    df.to_csv(file_path, index=False)

    print(f"Saved raw data to {file_path}")


def extract_and_store(indicators: Dict[str, str]) -> None:
    """
    Extract all indicators and store them locally.
    """

    for name, code in indicators.items():
        print(f"Fetching {name}...")
        df = fetch_indicator(code)
        save_raw_data(df, name)
