"""
Módulo de carga de datos para obtener y procesar datos del Banco Mundial.
Proporciona funciones para realizar solicitudes a la API y almacenar los resultados.
"""

from typing import Dict
import os
import requests
import pandas as pd
from src.config import BASE_URL, RAW_DATA_PATH, START_YEAR, END_YEAR


def fetch_indicator(indicator_code: str) -> pd.DataFrame:
    """
    Obtiene datos de un indicador específico del Banco Mundial.

    Args:
        indicator_code: Código del indicador en la API del Banco Mundial
                        (ej: 'SP.DYN.LE00.IN' para esperanza de vida)

    Returns:
        DataFrame de pandas con los datos del indicador

    Raises:
        Exception: Si ocurre un error HTTP o de la API
    """

    # Construir la URL de la API con los parámetros adecuados
    # format=json: respuesta en formato JSON
    # per_page=20000: número máximo de registros por solicitud
    # date=rango: filtro por período de años
    url = (
        f"{BASE_URL}/{indicator_code}"
        f"?format=json&per_page=20000"
        f"&date={START_YEAR}:{END_YEAR}"
    )

    # Realizar la solicitud HTTP a la API
    # timeout=60: esperar hasta 60 segundos por respuesta
    response = requests.get(url, timeout=60)

    # Validar que la respuesta HTTP sea exitosa (código 200)
    if response.status_code != 200:
        raise Exception(f"Error HTTP: {response.status_code}")

    # Parsear la respuesta JSON de la API
    data = response.json()

    # Detectar errores específicos de la API del Banco Mundial
    # La API devuelve un mensaje de error si el indicador no existe
    if isinstance(data, list) and len(data) == 1 and "message" in data[0]:
        error_msg = data[0]["message"][0]["value"]
        raise Exception(f"Error de la API del Banco Mundial: {error_msg}")

    # Validar que la estructura de datos sea la esperada
    # La API devuelve una lista con metadatos en [0] y datos en [1]
    if len(data) < 2:
        raise Exception("Estructura de respuesta de API inesperada.")

    # Normalizar los datos JSON en un DataFrame de pandas
    # Esto facilita el manejo y procesamiento posterior de los datos
    df = pd.json_normalize(data[1])

    return df


def save_raw_data(df: pd.DataFrame, indicator_name: str) -> None:
    """
    Guarda los datos crudos (sin procesar) en el disco.

    Args:
        df: DataFrame con los datos a guardar
        indicator_name: Nombre del indicador (se usará para el nombre del archivo)
    """

    # Asegurarse de que el directorio de datos crudos exista
    # exist_ok=True evita errores si el directorio ya existe
    os.makedirs(RAW_DATA_PATH, exist_ok=True)

    # Construir la ruta completa del archivo CSV
    file_path = os.path.join(RAW_DATA_PATH, f"{indicator_name}.csv")

    # Guardar el DataFrame en formato CSV
    # index=False omite el índice del DataFrame en el archivo
    df.to_csv(file_path, index=False)

    print(f"Datos crudos guardados en {file_path}")


def extract_and_store(indicators: Dict[str, str]) -> None:
    """
    Orchestrates la extracción de todos los indicadores y los guarda localmente.

    Args:
        indicators: Diccionario con nombres y códigos de indicadores
                    (mapeado desde src.config.INDICATORS)
    """

    # Iterar sobre cada indicador definido en la configuración
    for name, code in indicators.items():
        print(f"Obteniendo {name}...")

        # Obtener los datos del indicador desde la API
        df = fetch_indicator(code)

        # Guardar los datos crudos en el disco
        save_raw_data(df, name)
