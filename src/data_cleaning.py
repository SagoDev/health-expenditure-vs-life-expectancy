"""
Módulo de limpieza de datos para indicadores del Banco Mundial.
Proporciona funciones para transformar y preparar los datos crudos para el análisis.
"""

import os
from typing import Dict
import pandas as pd
from src.config import RAW_DATA_PATH, PROCESSED_CLEAN_PATH, FINAL_DATA_PATH


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


def build_final_dataset(cleaned_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Combina los indicadores limpiados en un único dataset basado en país-año.

    Esta función realiza un merge (unión) de todos los DataFrames de indicadores
    utilizando las columnas 'country', 'country_code' y 'year' como clave.
    El resultado es un dataset donde cada fila representa un país en un año específico
    con todos los indicadores disponibles para ese registro.

    Args:
        cleaned_data: Diccionario con DataFrames limpiados por indicador

    Returns:
        DataFrame combinado con todos los indicadores mergeados

    Raises:
        ValueError: Si se detectan duplicados en la clave país-año
    """

    # DataFrame que almacenará el resultado acumulado del merge
    merged_df = None

    # Iterar sobre cada indicador en el diccionario de datos limpiados
    for name, df in cleaned_data.items():
        # Renombrar la columna 'value' al nombre del indicador
        # Esto evita conflictos cuando se hace el merge
        df = df.rename(columns={"value": name})

        # Si es el primer indicador, inicializar el DataFrame mergeado
        if merged_df is None:
            merged_df = df
        else:
            # Para indicadores posteriores, hacer merge con el DataFrame existente
            # how='inner' mantiene solo las filas que existen en ambos DataFrames
            # Esto asegura que solo tengamos registros completos
            merged_df = merged_df.merge(
                df, on=["country", "country_code", "year"], how="inner"
            )

    # Validación: verificar si hay duplicados en la clave primaria (country_code + year)
    # La clave primaria no debe tener duplicados para evitar inconsistencias
    duplicates = merged_df.duplicated(subset=["country_code", "year"]).sum()

    # Si hay duplicados, lanzar un error para notificar al usuario
    if duplicates > 0:
        raise ValueError(f"Se detectaron filas duplicadas país-año: {duplicates}")

    # Ordenar el DataFrame final por código de país y año
    # Reiniciar el índice después de las transformaciones
    merged_df = merged_df.sort_values(["country_code", "year"]).reset_index(drop=True)

    return merged_df


def save_final_dataset(df: pd.DataFrame) -> None:
    """
    Guarda el dataset final combinado en el directorio de datos procesados.

    Args:
        df: DataFrame final con todos los indicadores mergeados
    """

    # Crear el directorio para el dataset final si no existe
    os.makedirs(FINAL_DATA_PATH, exist_ok=True)

    # Construir la ruta completa del archivo CSV
    file_path = os.path.join(FINAL_DATA_PATH, "final_dataset.csv")

    # Guardar el DataFrame como CSV sin índice
    df.to_csv(file_path, index=False)

    print("Dataset final guardado exitosamente.")
