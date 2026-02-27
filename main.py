"""Main script for extracting and processing World Bank data."""

from src.config import INDICATORS
from src.data_loader import extract_and_store
from src.data_cleaning import (
    clean_all_indicators,
    save_cleaned_indicators,
    build_merged_dataset,
    save_dataset,
)
from src.feature_engineering import apply_feature_engineering


def main():
    """Main function to orchestrate the data pipeline."""

    # 1️⃣ Extract
    extract_and_store(INDICATORS)

    # 2️⃣ Clean
    cleaned_data = clean_all_indicators(INDICATORS)

    # 3️⃣ Save cleaned indicators
    save_cleaned_indicators(cleaned_data)

    # 4️⃣ Build merged dataset
    merged_df = build_merged_dataset(cleaned_data)

    # 5️⃣ Save merged dataset
    save_dataset(merged_df, "merged_dataset.csv")

    # 6️⃣ Feature engineering (next step)
    enriched_df = apply_feature_engineering(merged_df)

    # 7️⃣ Save enriched dataset
    save_dataset(enriched_df, "final_enriched_dataset.csv")


if __name__ == "__main__":
    main()
