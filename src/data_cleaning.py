"""
Módulo de limpieza de datos para indicadores del Banco Mundial.
Proporciona funciones para transformar y preparar los datos crudos para el análisis.
"""

import os
from typing import Dict
import pandas as pd
from src.config import RAW_DATA_PATH


# Ruta del directorio donde se almacenarán los datos limpiados
PROCESSED_CLEAN_PATH = "data/processed/cleaned_indicators/"


def clean_worldbank_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia un DataFrame de indicador del Banco Mundial.

    Este proceso incluye:
    - Selección de columnas relevantes
    - Renombrado de columnas a nombres más descriptivos
    - Conversión de tipos de datos
    - Eliminación de valores nulos
    - Ordenamiento de los datos

    Args:
        df: DataFrame raw (sin procesar) obtenido de la API del Banco Mundial

    Returns:
        DataFrame limpio y estructurado listo para análisis
    """

    # Seleccionar solo las columnas necesarias del DataFrame
    # Las columnas originales tienen nombres con puntos (ej: 'country.value')
    df = df[["country.value", "country.id", "date", "value"]].copy()

    # Renombrar las columnas a nombres más claros y descriptivos
    # country.value -> country: nombre del país
    # country.id -> country_code: código ISO de 3 letras del país
    # date -> year: año del dato
    # value -> value: valor numérico del indicador
    df.columns = ["country", "country_code", "year", "value"]

    # Convertir la columna 'year' a tipo numérico
    # errors='coerce' convierte valores inválidos a NaN en lugar de generar error
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    # Convertir la columna 'value' a tipo numérico
    # Maneja casos donde el valor puede ser strings inválidos o missing
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # Eliminar filas que tienen valores nulos en la columna 'value'
    # Son registros sin datos válidos para el indicador
    df = df.dropna(subset=["value"])

    # Ordenar el DataFrame por código de país y año
    # Esto facilita la exploración y análisis secuencial de los datos
    df = df.sort_values(["country_code", "year"])

    # Reiniciar el índice del DataFrame después de las transformaciones
    # drop=True evita que el índice antiguo se guarde como columna
    return df.reset_index(drop=True)


def clean_all_indicators(indicators: Dict[str, str]) -> Dict[str, pd.DataFrame]:
    """
    Carga todos los archivos CSV crudos y aplica limpieza a cada indicador.

    Args:
        indicators: Diccionario con los nombres de los indicadores a procesar

    Returns:
        Diccionario con los nombres de indicadores como claves
        y DataFrames limpios como valores
    """

    # Diccionario para almacenar los datos limpios de cada indicador
    cleaned_data = {}

    # Iterar sobre cada indicador definido en la configuración
    for name in indicators.keys():
        # Construir la ruta del archivo CSV crudo
        file_path = os.path.join(RAW_DATA_PATH, f"{name}.csv")

        # Cargar el archivo CSV en un DataFrame
        df = pd.read_csv(file_path)

        # Aplicar la función de limpieza al DataFrame
        df_clean = clean_worldbank_df(df)

        # Almacenar el DataFrame limpio en el diccionario
        cleaned_data[name] = df_clean

    return cleaned_data


def save_cleaned_indicators(cleaned_data: Dict[str, pd.DataFrame]) -> None:
    """
    Guarda los DataFrames de indicadores limpiados en el directorio procesado.

    Args:
        cleaned_data: Diccionario con DataFrames limpiados por indicador
    """

    # Crear el directorio de indicadores limpiados si no existe
    os.makedirs(PROCESSED_CLEAN_PATH, exist_ok=True)

    # Iterar sobre cada indicador y su DataFrame limpio
    for name, df in cleaned_data.items():
        # Construir la ruta del archivo de salida
        file_path = os.path.join(PROCESSED_CLEAN_PATH, f"{name}_clean.csv")

        # Guardar el DataFrame como CSV sin índice
        df.to_csv(file_path, index=False)

    print("Todos los indicadores limpiados guardados exitosamente.")
