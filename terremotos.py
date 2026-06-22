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
# COMANDOS ÚTILES DEL DATAFRAME
# --------------------------------------------------

st.header("📚 Comandos Útiles del DataFrame")

# Primeras filas
st.subheader("🔹 df.head() - Primeras 5 filas")
st.dataframe(df.head())

# Últimas filas
st.subheader("🔹 df.tail() - Últimas 5 filas")
st.dataframe(df.tail())

# Dimensiones
st.subheader("🔹 df.shape - Dimensiones del Dataset")

filas, columnas = df.shape

col1, col2 = st.columns(2)

with col1:
    st.metric("📊 Filas", filas)

with col2:
    st.metric("📋 Columnas", columnas)

# Nombres de columnas
st.subheader("🔹 df.columns - Nombres de las Columnas")

st.dataframe(
    pd.DataFrame({
        "Columnas": df.columns
    }),
    use_container_width=True
)

# Tipos de datos
st.subheader("🔹 df.dtypes - Tipos de Datos")

tipos = pd.DataFrame({
    "Columna": df.columns,
    "Tipo de Dato": df.dtypes.astype(str)
})

st.dataframe(tipos, use_container_width=True)

# Valores nulos
st.subheader("🔹 df.isnull().sum() - Valores Nulos")

nulos = pd.DataFrame({
    "Columna": df.columns,
    "Valores Nulos": df.isnull().sum().values
})

st.dataframe(nulos, use_container_width=True)

# Estadísticas descriptivas
st.subheader("🔹 df.describe() - Estadísticas Descriptivas")

st.dataframe(
    df.describe(),
    use_container_width=True
)
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
st.header("🗑️ Eliminar Filas con Valores Nulos")

# Cantidad antes
st.write(f"📊 Registros originales: {len(df)}")

# Eliminar filas con nulos
df_sin_nulos = df.dropna()

# Cantidad después
st.write(f"✅ Registros después de eliminar nulos: {len(df_sin_nulos)}")

# Filas eliminadas
st.write(f"❌ Filas eliminadas: {len(df) - len(df_sin_nulos)}")

# Vista previa
st.dataframe(df_sin_nulos.head())

st.subheader("🔍 Verificación de Valores Nulos")

st.dataframe(
    df_sin_nulos.isnull().sum().reset_index().rename(
        columns={"index":"Columna",0:"Nulos"}
    )
)

st.header("Reemplazo de valores nulos por un valor fijo")

df_reemplazar = df.copy()

columnas_texto = df_reemplazar.select_dtypes(include="object").columns

for col in columnas_texto:
    df_reemplazar[col] = df_reemplazar[col].fillna("Desconocido")

st.dataframe(df_reemplazar.head())

st.header("Reemplazo de valores nulos por la media")

df_media = df.copy()

columnas_numericas = df_media.select_dtypes(include="number").columns

for col in columnas_numericas:
    df_media[col] = df_media[col].fillna(df_media[col].mean())

st.dataframe(df_media)

st.header("🔍 Detección de registros duplicados")

duplicados = df.duplicated().sum()

st.write(f"Número de registros duplicados: {duplicados}")

st.header("🧹 Tratamiento de Registros Duplicados")

# Eliminar duplicados
df_sin_duplicados = df.drop_duplicates()

st.write(f"Cantidad de registros antes: {len(df)}")
st.write(f"Cantidad de registros después: {len(df_sin_duplicados)}")

st.dataframe(df_sin_duplicados.head())

st.header("📊 Estadísticas Descriptivas")

st.dataframe(df["mag"].describe())

st.header("🔍 Detección de Valores Atípicos en la Magnitud")

Q1 = df["mag"].quantile(0.25)
Q3 = df["mag"].quantile(0.75)

IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

outliers = df[
    (df["mag"] < limite_inferior) |
    (df["mag"] > limite_superior)
]

st.write(f"Cantidad de valores atípicos encontrados: {len(outliers)}")

st.dataframe(outliers[["time", "place", "mag"]])

st.header("🧹 Eliminación de Valores Atípicos")

df_filtrado = df[
    (df["mag"] >= limite_inferior) &
    (df["mag"] <= limite_superior)
]

st.write(f"Registros originales: {len(df)}")
st.write(f"Registros después del filtrado: {len(df_filtrado)}")

st.header("✏️ Renombrar Columnas al Español")

df_renombrado = df.rename(columns={
    "time": "Fecha_Hora",
    "latitude": "Latitud",
    "longitude": "Longitud",
    "depth": "Profundidad",
    "mag": "Magnitud",
    "magType": "Tipo_Magnitud",
    "nst": "Numero_Estaciones",
    "gap": "Brecha_Angular",
    "dmin": "Distancia_Minima",
    "rms": "Error_RMS",
    "net": "Red_Sismica",
    "id": "Identificador",
    "updated": "Fecha_Actualizacion",
    "place": "Ubicacion",
    "type": "Tipo_Evento",
    "horizontalError": "Error_Horizontal",
    "depthError": "Error_Profundidad",
    "magError": "Error_Magnitud",
    "magNst": "Estaciones_Magnitud",
    "status": "Estado",
    "locationSource": "Fuente_Ubicacion",
    "magSource": "Fuente_Magnitud"
})
st.dataframe(df_renombrado.head())
# --------------------------------------------------
# VERIFICACIÓN FINAL DEL DATASET
# --------------------------------------------------

st.header("✅ Verificación Final del Dataset")

st.success("Se completó el proceso de limpieza y transformación de datos.")

# Dimensiones
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="📊 Número de Filas",
        value=df_renombrado.shape[0]
    )

with col2:
    st.metric(
        label="📋 Número de Columnas",
        value=df_renombrado.shape[1]
    )

# Resumen estadístico
st.subheader("📈 Resumen Estadístico")

st.dataframe(
    df_renombrado.describe(),
    use_container_width=True
)

# Verificar valores nulos
st.subheader("🔍 Verificación de Valores Nulos")

nulos_finales = df_renombrado.isnull().sum().sum()

st.metric(
    label="Valores Nulos Restantes",
    value=int(nulos_finales)
)

# Vista previa final
st.subheader("📋 Dataset Final Limpio")

st.dataframe(
    df_renombrado.head(20),
    use_container_width=True
)

# Guardar CSV limpio
csv = df_renombrado.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇️ Descargar Dataset Limpio",
    data=csv,
    file_name="terremotos_limpios.csv",
    mime="text/csv"
)