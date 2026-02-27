"""
Módulo de ingeniería de características para datos de gasto en salud y esperanza de vida.
Proporciona funciones para crear nuevas variables (features) que mejoran el análisis y modelado.
"""

import pandas as pd
import numpy as np


def add_log_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega características transformadas con logaritmo.
    
    La transformación logarítmica es útil para variables económicas con sesgo positivo
    (como el PIB per cápita), ya que:
    - Reduce el impacto de valores extremos/outliers
    - Facilita el cumplimiento de supuestos de normalidad
    - Mejora la interpretación en términos de porcentajes
    
    Args:
        df: DataFrame con los datos del dataset final
        
    Returns:
        DataFrame con la nueva columna 'log_gdp_per_capita' añadida
    """

    # Crear una copia para no modificar el DataFrame original
    df = df.copy()

    # Calcular el logaritmo natural del PIB per cápita
    # np.log maneja automáticamente valores NaN
    df["log_gdp_per_capita"] = np.log(df["gdp_per_capita"])

    return df


def add_yoy_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega características de crecimiento año a año (year-over-year).
    
    Estas métricas capturan la dinámica de cambio temporal:
    - Crecimiento porcentual del gasto en salud
    - Cambio absoluto en la esperanza de vida
    
    Args:
        df: DataFrame con los datos del dataset final
        
    Returns:
        DataFrame con las nuevas columnas de crecimiento anual
    """

    # Ordenar primero por código de país y año para garantizar orden temporal
    # Crear una copia para no modificar el DataFrame original
    df = df.sort_values(["country_code", "year"]).copy()

    # Calcular el crecimiento porcentual anual del gasto en salud
    # groupby('country_code'): calcula dentro de cada país
    # pct_change(): calcula (valor_actual - valor_anterior) / valor_anterior
    # El primer año de cada país será NaN (no hay año anterior)
    df["health_exp_yoy_growth"] = df.groupby("country_code")[
        "health_expenditure_pct_gdp"
    ].pct_change()

    # Calcular el cambio absoluto anual en la esperanza de vida
    # diff(): calcula valor_actual - valor_anterior
    # A diferencia de pct_change, aquí es cambio absoluto (en años)
    df["life_expectancy_yoy_change"] = df.groupby("country_code")[
        "life_expectancy"
    ].diff()

    return df


def add_lag_features(df: pd.DataFrame, lag: int = 1) -> pd.DataFrame:
    """
    Agrega características de valores rezagados (lags).
    
    Los valores rezagados son útiles para:
    - Capturar efectos retardados (el gasto de salud de hoy afecta la esperanza de vida futura)
    - Crear variables para modelos de series de tiempo
    - Analizar relaciones causales con desfase temporal
    
    Args:
        df: DataFrame con los datos del dataset final
        lag: Número de períodos hacia atrás para crear el rezago (default: 1 año)
        
    Returns:
        DataFrame con la nueva columna de gasto en salud rezagado
    """

    # Crear una copia para no modificar el DataFrame original
    df = df.copy()

    # Crear columna con valor del gasto en salud de 'lag' años atrás
    # shift(lag): mueve los valores hacia abajo por 'lag' posiciones
    # groupby('country_code'): asegura que el rezago sea dentro de cada país
    df[f"health_exp_lag_{lag}y"] = df.groupby("country_code")[
        "health_expenditure_pct_gdp"
    ].shift(lag)

    return df


def add_efficiency_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega indicadores simples de eficiencia.
    
    Este indicador busca medir cuántos años de esperanza de vida se obtienen
    por cada punto porcentual de gasto en salud. Es una medida rudimentaria
    de la "eficiencia" del sistema de salud.
    
    Args:
        df: DataFrame con los datos del dataset final
        
    Returns:
        DataFrame con la nueva columna de eficiencia
    """

    # Crear una copia para no modificar el DataFrame original
    df = df.copy()

    # Calcular la esperanza de vida por unidad de gasto en salud
    # Nota: puede generar inf si health_expenditure_pct_gdp es 0
    df["life_expectancy_per_health_exp"] = (
        df["life_expectancy"] / df["health_expenditure_pct_gdp"]
    )

    return df


def apply_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica todos los pasos de ingeniería de características en secuencia.
    
    Esta función orquesta la aplicación de todas las transformaciones de features:
    1. Transformaciones logarítmicas
    2. Características de crecimiento año a año
    3. Características rezagadas
    4. Indicadores de eficiencia
    
    Args:
        df: DataFrame con los datos del dataset final
        
    Returns:
        DataFrame con todas las nuevas características añadidas
    """

    # Aplicar cada transformación secuencialmente
    df = add_log_features(df)
    df = add_yoy_features(df)
    df = add_lag_features(df, lag=1)
    df = add_efficiency_features(df)

    return df
