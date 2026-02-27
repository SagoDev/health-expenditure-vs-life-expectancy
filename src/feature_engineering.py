"""Feature engineering functions for health expenditure and life expectancy data."""

import pandas as pd
import numpy as np


def add_log_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add log-transformed economic features.
    """

    df = df.copy()

    df["log_gdp_per_capita"] = np.log(df["gdp_per_capita"])

    return df


def add_yoy_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add year-over-year growth features.
    """

    df = df.sort_values(["country_code", "year"]).copy()

    df["health_exp_yoy_growth"] = df.groupby("country_code")[
        "health_expenditure_pct_gdp"
    ].pct_change()

    df["life_expectancy_yoy_change"] = df.groupby("country_code")[
        "life_expectancy"
    ].diff()

    return df


def add_lag_features(df: pd.DataFrame, lag: int = 1) -> pd.DataFrame:
    """
    Add lagged health expenditure feature.
    """

    df = df.copy()

    df[f"health_exp_lag_{lag}y"] = df.groupby("country_code")[
        "health_expenditure_pct_gdp"
    ].shift(lag)

    return df


def add_efficiency_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add simple efficiency indicators.
    """

    df = df.copy()

    df["life_expectancy_per_health_exp"] = (
        df["life_expectancy"] / df["health_expenditure_pct_gdp"]
    )

    return df


def apply_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all feature engineering steps.
    """

    df = add_log_features(df)
    df = add_yoy_features(df)
    df = add_lag_features(df, lag=1)
    df = add_efficiency_features(df)

    return df
