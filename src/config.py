"""Configuration file for the World Bank API project."""

BASE_URL = "https://api.worldbank.org/v2/country/all/indicator"

INDICATORS = {
    "life_expectancy": "SP.DYN.LE00.IN",
    "health_expenditure_pct_gdp": "SH.XPD.CHEX.GD.ZS",
    "infant_mortality": "SP.DYN.IMRT.IN",
    "gdp_per_capita": "NY.GDP.PCAP.CD",
}

START_YEAR = 2000
END_YEAR = 2023

RAW_DATA_PATH = "data/raw/"
