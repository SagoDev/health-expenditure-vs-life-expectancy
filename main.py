"""Main script for extracting and processing World Bank data."""

from src.config import INDICATORS
from src.data_loader import extract_and_store
from src.data_cleaning import (
    clean_all_indicators,
    save_cleaned_indicators,
    build_final_dataset,
    save_final_dataset,
)


def main():
    """Main function to orchestrate the data pipeline."""

    # 1️⃣ Extract
    extract_and_store(INDICATORS)

    # 2️⃣ Clean
    cleaned_data = clean_all_indicators(INDICATORS)

    # 3️⃣ Save cleaned indicators
    save_cleaned_indicators(cleaned_data)

    # 4️⃣ Build final dataset
    final_df = build_final_dataset(cleaned_data)

    # 5️⃣ Save final dataset
    save_final_dataset(final_df)

    # 6️⃣ Feature engineering (next step)
    # 7️⃣ Analysis


if __name__ == "__main__":
    main()
