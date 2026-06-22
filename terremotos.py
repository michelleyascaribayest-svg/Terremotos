import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# --------------------------------------------------
st.set_page_config(
    page_title="Análisis Exploratorio de Terremotos",
    layout="wide"
)

# --------------------------------------------------
# TÍTULO
# --------------------------------------------------
st.title("🌋 Análisis Exploratorio de Terremotos en el Mundo")

st.markdown("""
## Información del Estudiante

**Nombre:** Michelle  Yascaribay 

**Asignatura:** Mineria de Datos

**Paralelo:** M2A

---

### Instrucciones de Uso

1. La aplicación obtiene datos reales desde una fuente pública oficial.
2. Visualice el conjunto de datos.
3. Revise los tipos de datos presentes.
4. Explore el reporte automático generado por Sweetviz.
5. Analice tendencias y características de los terremotos registrados durante los últimos 30 días.
""")

# --------------------------------------------------
# CARGA DE DATOS
# --------------------------------------------------
URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv"

@st.cache_data
def cargar_datos():
    df = pd.read_csv(URL)

    # Convertir columna temporal
    df["time"] = pd.to_datetime(df["time"])

    return df

df = cargar_datos()

# --------------------------------------------------
# MOSTRAR DATOS
# --------------------------------------------------
st.subheader("📊 Vista Previa del Dataset")

st.dataframe(df.head(20))

# --------------------------------------------------
# INFORMACIÓN GENERAL
# --------------------------------------------------
st.subheader("📋 Información General")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Número de Registros", len(df))

with col2:
    st.metric("Número de Columnas", len(df.columns))

with col3:
    st.metric("Magnitud Máxima", round(df["mag"].max(), 2))

# --------------------------------------------------
# TIPOS DE DATOS
# --------------------------------------------------
st.subheader("🔍 Tipos de Datos")

tipos = pd.DataFrame({
    "Columna": df.columns,
    "Tipo de Dato": df.dtypes.astype(str)
})

st.dataframe(tipos)

st.markdown("""
### Tipos de Datos Identificados

**Datos Cuantitativos**
- mag (magnitud)
- depth (profundidad)
- latitude
- longitude

**Datos Cualitativos**
- place
- type
- status

**Datos Temporales**
- time
- updated
""")

# --------------------------------------------------
# REPORTE SWEETVIZ
# --------------------------------------------------
st.subheader("📈 Análisis Exploratorio Automático (Sweetviz)")

with open("reporte_sweetviz.html", "r", encoding="utf-8") as archivo:
    html = archivo.read()

components.html(
    html,
    height=4000,
    scrolling=True
)