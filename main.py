"""Main script for extracting and processing World Bank data."""

from src.config import INDICATORS
from src.data_loader import extract_and_store
from src.data_cleaning import clean_all_indicators, save_cleaned_indicators


def main():
    """Main function to orchestrate the data pipeline."""

    # 1️⃣ Extract
    # extract_and_store(INDICATORS)

    # 2️⃣ Clean
    cleaned_data = clean_all_indicators(INDICATORS)

    # 3️⃣ Save cleaned indicators
    save_cleaned_indicators(cleaned_data)

    # 4️⃣ Feature engineering
    # 5️⃣ Analysis
    # 6️⃣ Save final dataset


if __name__ == "__main__":
    main()
