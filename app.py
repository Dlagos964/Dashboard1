import streamlit as st
import pandas as pd
import numpy as np      
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

#Configuración inicial
st.set_page_config(
    page_title="Data Visualization Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

 # Generación de datos de ejemplo
def generate_datos_empresa():
       
    fechas = pd.date_range(start="2023-01-01", end=datetime.today(), freq='D')
    datos ={
        'fecha': fechas,
        'ingresos_diarios': np.random.normal(25000, 150, size=len(fechas)),
        'costos': np.random.normal(12000, 3000, size=len(fechas)),
        'usuarios_activos': np.random.normal(50, 200, size=len(fechas)),
        'conversion_rate': np.random.normal(2.5, 0.6, size=len(fechas)),
        'ltv_cliente': np.random.normal(180, 40, size=len(fechas)),
        'costo_adquisicion_cliente': np.random.normal(45, 12, size=len(fechas))
    }
    df = pd.DataFrame(datos)
    df['ingresos_diarios'] *= (1 + np.arange(len(df)) * 0.0001) # tendencia

    return df 

df = generate_datos_empresa()


#Título
st.markdown('<h1 class="main-header"> 🚀 Dashboard Ejecutivo 2025</h1>',unsafe_allow_html=True)

#Filtros
col1, col2, col3 = st.columns(3)
with col1:
    periodo = st.selectbox("📅 Período:",
                            ["Últimos 30 días","Último Trimestre","Último año"])
with col2:
    categoria = st.selectbox("🎯 Categoría:", 
                            ["General", "Ventas", "Marketing", "Producto", "Finanzas", "Clientes"])
with col3:
    comparaciom = st.selectbox("📊 Comparación con:",
                            ["Mes Anterior", "Trimestre Anterior", "Año Anterior", "Promedio del Año"])
    
#KPIs
st.markdown('<h2 class="sub-header">📈 OKRs de Empresa</h2>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    ingresos = df[df['fecha'].dt.month == datetime.today().month]['ingresos_diarios'].sum()
    # Filtra el mismo mes pero del año anterior
    ingresos_anio_ant = df[
        (df['fecha'].dt.month == datetime.today().month) &
        (df['fecha'].dt.year == datetime.today().year - 1)
    ]['ingresos_diarios'].sum()
    # Calcula el delta
    if ingresos_anio_ant > 0:
        delta = f"{((ingresos - ingresos_anio_ant) / ingresos_anio_ant) * 100:.2f}%"
    else:
        delta = "N/A"
    st.metric("Ingresos Totales", f"${ingresos:,.0f}", delta=delta)

with col2:
    costos = df[df['fecha'].dt.month == datetime.today().month]['costos'].sum()
    # Filtra el mismo mes pero del año anterior
    costos_anio_ant = df[
        (df['fecha'].dt.month == datetime.today().month) &
        (df['fecha'].dt.year == datetime.today().year - 1)
    ]['costos'].sum()
    # Calcula el delta
    if costos_anio_ant > 0:
        delta = f"{((costos - costos_anio_ant) / costos_anio_ant) * 100:.2f}%"
    else:
        delta = "N/A"
    st.metric("Costos Totales", f"${costos:,.0f}", delta=delta)

with col3:
    usuarios_activos = df[df['fecha'].dt.month == datetime.today().month]['usuarios_activos'].sum()
    # Filtra el mismo mes pero del año anterior
    usuarios_activos_anio_ant = df[
        (df['fecha'].dt.month == datetime.today().month) &
        (df['fecha'].dt.year == datetime.today().year - 1)
    ]['usuarios_activos'].sum()
    # Calcula el delta
    if usuarios_activos_anio_ant > 0:
        delta = f"{((usuarios_activos - usuarios_activos_anio_ant) / usuarios_activos_anio_ant) * 100:.2f}%"
    else:
        delta = "N/A"
    st.metric("Usuarios Activos", f"{usuarios_activos:,.0f}", delta=delta)
    
    # Promedio de usuarios activos del mes actual
    promedio_usuarios = df[df['fecha'].dt.month == datetime.today().month]['usuarios_activos'].mean()
    st.write(f"Promedio diario de usuarios activos: {promedio_usuarios:,.2f}")

with col4:  
    tasa_conversion = df[df['fecha'].dt.month == datetime.today().month]['conversion_rate'].mean()
    # Filtra el mismo mes pero del año anterior
    tasa_conversion_anio_ant = df[
        (df['fecha'].dt.month == datetime.today().month) &
        (df['fecha'].dt.year == datetime.today().year - 1)
    ]['conversion_rate'].mean()
    # Calcula el delta
    if tasa_conversion_anio_ant > 0:
        delta = f"{((tasa_conversion - tasa_conversion_anio_ant) / tasa_conversion_anio_ant) * 100:.2f}%"
    else:
        delta = "N/A"
    st.metric("Tasa de Conversión", f"{tasa_conversion:.2f}%", delta=delta)

#Graficos
st.markdown('<h2 class="sub-header">📊 Gráficos de Tendencias</h2>', unsafe_allow_html=True)
col1, col2 = st.columns(2)  

with col1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['fecha'], y=df['ingresos_diarios'], mode='lines', name='Ingresos Diarios',line=dict(color='blue')))
    z = np.polyfit(range(len(df)), df['ingresos_diarios'], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(x=df['fecha'], y=p(range(len(df))), mode='lines', name='Tendencia', line=dict(color='red', dash='dash')))
    fig.update_layout(title="💰 Ingresos Diarios con Tendencia",height = 400, template = "plotly_white")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    etapas = ['visitantes', 'leads', 'Oportunidades', 'clientes']
    valores = [10000, 2500, 500, 200]
    funnel = go.Figure(go.Funnel(y=etapas,x=valores, textinfo="value+percent initial"))
    funnel.update_layout(title="🎯 Embudo de Ventas", height=400, template="plotly_white")
    st.plotly_chart(funnel, use_container_width=True)

#Alerta inteligente
st.markdown("## ⚠️ Alerta Inteligente")
alertas = []
if df['ingresos_diarios'].tail(7).mean() < df['ingresos_diarios'].head(-7).mean():
    alertas.append({'tipo':'Advertencia', 'mensaje': 'Ingresos por debajo del promedio en últimoso 7 días','color': 'orange'})

if df['conversion_rate'].tail(1).iloc[0] < 2.0:
    alertas.append({'tipo':'Crítico', 'mensaje': 'Tasa de conversión por debajo del 2%','color': 'red'})

if df['usuarios_activos'].tail(1).iloc[0] > df['usuarios_activos'].quantile(0.95):
    alertas.append({'tipo':'Éxito', 'mensaje': 'Usuarios activos en el 95% más alto','color': 'green'})

for alerta in alertas:
    st.markdown(f"""
                <div style = "padding: 1rem; margin: 0.5rem 0; background-color: {alerta['color']};
                  color: white; border-radius: 10px; font-weight: bold;">
                {alerta['tipo']}: {alerta['mensaje']}
                </div>
                """, unsafe_allow_html=True)

#Datos de la empresa
st.markdown('<h2 class="sub-header">📊 Datos de la empresa</h2>', unsafe_allow_html=True)
st.dataframe(df)

streamlit
pandas
numpy
plotly
