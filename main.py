"""Main script for extracting and processing World Bank data."""

from src.config import INDICATORS
from src.data_loader import extract_and_store


def main():
    """Main function to orchestrate the data extraction and processing."""
    # 1. Extract
    extract_and_store(INDICATORS)

    # 2. Clean
    # 3. Feature engineering
    # 4. Analysis
    # 5. Save results


if __name__ == "__main__":
    main()
