"""
Archivo de configuración para el proyecto de la API del Banco Mundial.
Contiene los parámetros globales necesarios para la extracción de datos.
"""

# URL base de la API del Banco Mundial para indicadores
BASE_URL = "https://api.worldbank.org/v2/country/all/indicator"

# Diccionario que mapea nombres descriptivos a códigos de indicadores del Banco Mundial
# Cada código corresponde a un indicador específico de la base de datos del Banco Mundial
INDICATORS = {
    "life_expectancy": "SP.DYN.LE00.IN",  # Esperanza de vida al nacer (años)
    "health_expenditure_pct_gdp": "SH.XPD.CHEX.GD.ZS",  # Gasto en salud como porcentaje del PIB (%)
    "infant_mortality": "SP.DYN.IMRT.IN",  # Mortalidad infantil (por cada 1000 nacimientos)
    "gdp_per_capita": "NY.GDP.PCAP.CD",  # PIB per cápita (en dólares actuales)
}

# Año de inicio para la extracción de datos históricos
START_YEAR = 2000

# Año de fin para la extracción de datos históricos
END_YEAR = 2023

# Ruta del directorio donde se almacenarán los datos crudos (sin procesar)
RAW_DATA_PATH = "data/raw/"
