import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Título de la aplicación
st.title('🚀 Análisis de Almacenamiento para la Empresa XYZ')

# --- 1. Descripción del Escenario ---
st.header('1. Descripción del Escenario')
st.write(
    'La empresa XYZ enfrenta desafíos de infraestructura de almacenamiento, '
    'incluyendo lentitud en el acceso a datos y limitaciones de escalabilidad. '
    'El objetivo es evaluar HDD, SSD y almacenamiento en la nube para mejorar el '
    'rendimiento, la fiabilidad y la capacidad de crecimiento.'
)

# --- 2. Carga de Datos ---
# URL del archivo raw CSV de GitHub.
# Asegúrate de reemplazar "tu_usuario" y "tu_repositorio" con los tuyos.
url_github = 'https://raw.githubusercontent.com/tu_usuario/proyecto-almacenamiento-streamlity/main/almacenamiento.csv'
df = pd.read_csv(url_github)
st.write('---')
st.header('2. Criterios y Comparación de Tecnologías')
st.dataframe(df.set_index('Tecnología'))

# --- 3. Análisis Gráfico y Visualización ---
st.write('---')
st.header('3. Análisis Gráfico y Visualización')

# Gráfico de Barras de Velocidad
st.subheader('Gráfico de Barras: Velocidad de Lectura/Escritura')
fig_barras = px.bar(df, x='Tecnología', y=['Velocidad_Lectura_MBps', 'Velocidad_Escritura_MBps'], 
                    barmode='group', title='Comparación de Velocidad por Tecnología')
st.plotly_chart(fig_barras)

# Gráfico Radar de Fiabilidad, Escalabilidad y Seguridad
st.subheader('Gráfico Radar: Fiabilidad, Escalabilidad y Seguridad')
# Normalizar datos para el gráfico radar (ej. Fiabilidad, Escalabilidad)
df_radar = df[['Tecnología', 'Fiabilidad_MTBF_horas', 'Seguridad', 'Escalabilidad']].copy()
df_radar['Fiabilidad_MTBF_horas'] = df_radar['Fiabilidad_MTBF_horas'] / 100000
# Crear un mapeo para convertir valores de texto a numéricos
mapa_seguridad = {'Básica': 1, 'Media': 3, 'Alta': 5}
mapa_escalabilidad = {'Baja': 1, 'Media': 3, 'Muy alta': 5, 'Ilimitada': 5}
df_radar['Seguridad_num'] = df_radar['Seguridad'].map(mapa_seguridad)
df_radar['Escalabilidad_num'] = df_radar['Escalabilidad'].map(mapa_escalabilidad)

fig_radar = go.Figure()
for tecnologia in df_radar['Tecnología'].unique():
    subset = df_radar[df_radar['Tecnología'] == tecnologia]
    fig_radar.add_trace(go.Scatterpolar(
        r=[subset['Fiabilidad_MTBF_horas'].iloc[0], subset['Escalabilidad_num'].iloc[0], subset['Seguridad_num'].iloc[0]],
        theta=['Fiabilidad (x10^5 horas)', 'Escalabilidad', 'Seguridad'],
        fill='toself',
        name=tecnologia
    ))
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
    showlegend=True,
    title='Comparación de Criterios Clave'
)
st.plotly_chart(fig_radar)

# Gráfico de Costos
st.subheader('Gráfico de Costos: Costo por GB')
fig_costos = px.bar(df, x='Tecnología', y='Costo_por_GB_USD', 
                    title='Costo por GB por Tecnología de Almacenamiento',
                    labels={'Costo_por_GB_USD': 'Costo por GB (USD)'})
st.plotly_chart(fig_costos)

# --- 4. Simulación y Diagrama de Infraestructura ---
st.write('---')
st.header('4. Simulación y Diagrama de Infraestructura')

st.subheader('Simulación de Rendimiento')
st.write(
    'Simulación del impacto en el tiempo de respuesta al pasar de HDD a SSD, '
    'considerando un aumento del 50% en el volumen de datos en 2 años.'
)
# Datos de la simulación
volumen_actual_GB = 100
volumen_2_años_GB = volumen_actual_GB * 1.5
tiempo_respuesta_hdd = 250  # ms por GB (ejemplo)
tiempo_respuesta_ssd = 50   # ms por GB (ejemplo)

# Calcular tiempos de respuesta
simulacion_df = pd.DataFrame({
    'Escenario': ['Actual (HDD)', 'Proyectado (HDD)', 'Proyectado (SSD)'],
    'Volumen de Datos (GB)': [volumen_actual_GB, volumen_2_años_GB, volumen_2_años_GB],
    'Tiempo de Respuesta Total (ms)': [
        volumen_actual_GB * tiempo_respuesta_hdd,
        volumen_2_años_GB * tiempo_respuesta_hdd,
        volumen_2_años_GB * tiempo_respuesta_ssd
    ]
})

fig_simulacion = px.line(simulacion_df, x='Escenario', y='Tiempo de Respuesta Total (ms)', 
                         title='Impacto de la Simulación en el Tiempo de Respuesta',
                         markers=True)
st.plotly_chart(fig_simulacion)

st.subheader('Diagrama de Infraestructura')
st.write('Representación visual de la integración de la solución recomendada.')
st.code("""
graph TD
    subgraph Infraestructura Actual (HDD)
        A[Servidor Web] --> B(Base de Datos - HDD)
        B --> C[Aplicaciones Legado]
    end

    subgraph Infraestructura Propuesta (Híbrida)
        D[Servidor Web] --> E(Base de Datos Crítica - SSD)
        D --> F(Almacenamiento de Archivos - Nube)
        E --> G[Aplicaciones de Alto Rendimiento]
        F --> H[Respaldo y Archivo]
    end

    A -- "Migración" --> E
    B -- "Migración" --> F
    E -- "Acceso Rápido" --> G
    F -- "Escalabilidad" --> H
""", language="mermaid")

# --- 5. Análisis de Riesgos y Oportunidades ---
st.write('---')
st.header('5. Análisis de Riesgos y Oportunidades')
st.subheader('Riesgos')
st.markdown("""
* **Alto costo inicial del SSD:** La inversión inicial es considerable.
* **Durabilidad de los SSD:** Tienen un número limitado de ciclos de escritura.
* **Dependencia de la conectividad para la nube:** Se requiere una conexión a internet estable.
* **Seguridad de los datos en la nube:** La responsabilidad de la configuración de seguridad es crucial.
""")
st.subheader('Oportunidades')
st.markdown("""
* **Escalabilidad con almacenamiento en la nube:** Permite un crecimiento ilimitado.
* **Mejora del rendimiento con SSD:** Aumenta drásticamente la velocidad.
* **Reducción de costos operativos a largo plazo:** Menor consumo de energía y mantenimiento.
* **Reducción de los tiempos de inactividad:** Un sistema más fiable reduce las fallas.
""")

# --- 6. Conclusiones Técnicas ---
st.write('---')
st.header('6. Conclusiones Técnicas')
st.markdown(
    '**Resumen:** El análisis muestra que las **oportunidades de mejora superan los riesgos**. '
    'Las tecnologías actuales son inadecuadas para el crecimiento futuro de la empresa.'
)
st.markdown(
    '**Recomendación:** Se propone una **solución híbrida** que combina **SSD para aplicaciones '
    'críticas** y **almacenamiento en la nube para respaldo y escalabilidad**.'
)
