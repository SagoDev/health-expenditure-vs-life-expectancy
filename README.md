# Gasto en Salud vs Esperanza de Vida
**Un estudio analítico utilizando datos abiertos del Banco Mundial**

## 📌 Descripción del Proyecto

Este proyecto analiza la relación entre el gasto en salud y los resultados de salud
en diferentes países utilizando datos públicos del Banco Mundial.

El objetivo no solo es identificar correlaciones, sino comprender:
- Cómo el gasto en salud se relaciona con la esperanza de vida
- Si mayor gasto siempre conduce a mejores resultados
- Si el impacto de la inversión en salud es inmediato o retrasado
- Cómo difiere la eficiencia entre países

El proyecto está diseñado como un pipeline de datos reproducible y modular
con un fuerte enfoque analítico.

---

## 🧠 Preguntas Clave

- ¿Mayor gasto en salud lleva a mayor esperanza de vida?
- ¿Hay rendimientos decrecientes del gasto en salud?
- ¿Países con gasto similar logran resultados diferentes?
- ¿El impacto de la inversión en salud es inmediato o rezagado?

---

## 🔄 Pipeline de Datos

1. **Extracción**
   - Datos obtenidos de la API del Banco Mundial
   - Múltiples indicadores descargados independientemente

2. **Limpieza**
   - Normalización estructural
   - Eliminación de entidades inválidas o agregadas
   - Granularidad consistente país-año

3. **Integración**
   - Indicadores combinados en un único dataset analítico
   - Clave primaria: `(country_code, year)`

4. **Ingeniería de Características**
   - Características temporales (cambio anual, variables rezagadas)
   - Transformaciones logarítmicas para escala económica
   - Indicadores de eficiencia

5. **Análisis Exploratorio**
   - EDA basado en hipótesis
   - Un notebook por hipótesis

---

## 📊 Fuentes de Datos

- API de Datos Abiertos del Banco Mundial  
  Indicadores utilizados:
  - Esperanza de vida al nacer
  - Gasto en salud (% del PIB)
  - Tasa de mortalidad infantil
  - PIB per cápita

---

## 📈 Enfoque Analítico

El análisis está basado en hipótesis en lugar de ser puramente descriptivo.

Cada hipótesis se explora utilizando:
- Visualizaciones dirigidas
- Ingeniería de características contextual
- Conclusiones analíticas claras
- Limitaciones explícitas

---

## ⚠️ Limitaciones

- Solo datos observacionales (sin inferencia causal)
- Valores faltantes para algunos países-años
- Sin control de factores institucionales o de política
- Datos agregados a nivel nacional

---

## 🧪 Cómo Ejecutar el Pipeline

```bash
pip install -r requirements.txt
python main.py
```

---

## 📁 Estructura del Proyecto

```
├── main.py                 # Script principal del pipeline
├── src/
│   ├── config.py          # Configuración y constantes
│   ├── data_loader.py     # Extracción de datos de la API
│   ├── data_cleaning.py  # Limpieza y merge de datos
│   ├── feature_engineering.py  # Creación de features
│   ├── analysis.py       # Análisis estadístico
│   └── visualization.py  # Generación de gráficos
├── data/
│   ├── raw/              # Datos crudos de la API
│   └── processed/        # Datos procesados
├── notebooks/            # Notebooks de análisis
└── README.md
```

---

## 📓 Notebooks de Análisis

El proyecto incluye 3 notebooks que exploran hipótesis específicas:

| Notebook | Tema |
|----------|------|
| `01_expenditure_vs_life_expectancy.ipynb` | Relación entre gasto en salud y esperanza de vida |
| `02_efficiency_of_health_spending.ipynb` | Eficiencia del gasto en salud entre países |
| `03_lagged_effects_of_spending.ipynb` | Efectos rezagados del gasto en salud |

Para ejecutarlos: `jupyter notebook notebooks/`

---

## 📦 Dependencias

- pandas
- numpy
- requests
- matplotlib / seaborn (para visualización)
