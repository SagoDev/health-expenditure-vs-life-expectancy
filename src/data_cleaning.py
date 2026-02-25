"""Data cleaning functions for World Bank indicators."""

# src/data_cleaning.py

import os
from typing import Dict
import pandas as pd
from src.config import RAW_DATA_PATH


PROCESSED_CLEAN_PATH = "data/processed/cleaned_indicators/"


def clean_worldbank_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw World Bank indicator dataframe.
    """

    df = df[["country.value", "country.id", "date", "value"]].copy()

    df.columns = ["country", "country_code", "year", "value"]

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    df = df.dropna(subset=["value"])

    df = df.sort_values(["country_code", "year"])

    return df.reset_index(drop=True)


def clean_all_indicators(indicators: Dict[str, str]) -> Dict[str, pd.DataFrame]:
    """
    Load raw CSV files and apply cleaning to each indicator.
    """

    cleaned_data = {}

    for name in indicators.keys():
        file_path = os.path.join(RAW_DATA_PATH, f"{name}.csv")

        df = pd.read_csv(file_path)
        df_clean = clean_worldbank_df(df)

        cleaned_data[name] = df_clean

    return cleaned_data


def save_cleaned_indicators(cleaned_data: Dict[str, pd.DataFrame]) -> None:
    """
    Save cleaned indicator dataframes to processed directory.
    """

    os.makedirs(PROCESSED_CLEAN_PATH, exist_ok=True)

    for name, df in cleaned_data.items():
        file_path = os.path.join(PROCESSED_CLEAN_PATH, f"{name}_clean.csv")

        df.to_csv(file_path, index=False)

    print("All cleaned indicators saved successfully.")
