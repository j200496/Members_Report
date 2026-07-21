import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path
import google.generativeai as genai



# Configuración de la página de Streamlit
st.set_page_config(layout="wide", page_title="Reporte de Votantes", page_icon="📊")

# Encabezado y Logo
left, center, right = st.columns([2, 3, 2])
with center:
    st.image(
        "Images/logofupu.png", 
        caption="Plataforma electoral de reportes -- Desarrollado por joeltechrd -- All rights reserved",
        use_container_width=True
    )  

st.header("Reporte de votantes inscritos", divider="green", text_alignment="center")

# Carga de datos
data = st.file_uploader("Sube el archivo excel", type=["xlsx"])

if data is not None:
    df = pd.read_excel(data)
    
    # Selectores de filtros
    prov = df["Territorio"].unique()
    sel = st.selectbox(
        "Filtrar por territorio",
        options=prov,
        index=None,
        placeholder="Buscar un territorio"
    )
    
    sel2 = st.selectbox(
        "Filtrar por líderes de equipo",
        options=df["Lider"].unique(),
        index=None,
        placeholder="Buscar un líder"
    )
    
    # Dataframes filtrados
    df_filter = df[df["Territorio"] == sel]
    df_filterusers = df[df["Lider"] == sel2]

    # Contenedores para las métricas kpi
    col1, col2, col3 = st.columns(3)

    if sel:
        total = df_filter["Nombre"].count()
        hombres = (df_filter["Género"] == "M").sum()
        mujeres = (df_filter["Género"] == "F").sum()
        
        col1.metric(label="Total de votantes (Territorio)", value=total, border=True)
        col2.metric(label="Hombres", value=hombres, border=True)
        col3.metric(label="Mujeres", value=mujeres, border=True)
        
    elif sel2:
        total2 = df_filterusers["Nombre"].count()
        hombres = (df_filterusers["Género"] == "M").sum()
        mujeres = (df_filterusers["Género"] == "F").sum()
        
        col1.metric(label="Total de votantes (Líder)", value=total2, border=True)
        col2.metric(label="Hombres", value=hombres, border=True)
        col3.metric(label="Mujeres", value=mujeres, border=True)
        
    else:
        total1 = df["Nombre"].count()
        hombres = (df["Género"] == "M").sum()
        mujeres = (df["Género"] == "F").sum()
        
        col1.metric(label="Total de votantes", value=total1, border=True)
        col2.metric(label="Hombres", value=hombres, border=True)
        col3.metric(label="Mujeres", value=mujeres, border=True)

    # Vista de tabla dinámica según el filtro
    st.header("Total general de votantes", divider="green", text_alignment="center")
    if sel: 
        st.dataframe(df_filter, use_container_width=True)
    elif sel2:     
        st.dataframe(df_filterusers, use_container_width=True)
    else:    
        st.dataframe(df, use_container_width=True)

    st.button("Mandar mensajes masivos por WhatsApp a los votantes", icon="💬", on_click=lambda: genai.chat.send_message(
        model="models/chat-bison-001",))


    # Procesamiento de agrupaciones para reportes gráficos
    miembros_por_usuario = df.groupby("Lider").size().reset_index(name="Total de votantes").sort_values(by="Total de votantes", ascending=False)
    top5_usuarios = df.groupby("Lider").size().reset_index(name="Votantes por coordinadores").sort_values(by="Votantes por coordinadores", ascending=False).head(5)
    miembros_por_territorio = df.groupby("Territorio").size().reset_index(name="Votantes por territorio").sort_values(by="Votantes por territorio", ascending=False)

    # Sección 1: Reportes por Territorios
    st.header("Lista de votantes por territorios", divider="green", text_alignment="center")
    st.dataframe(miembros_por_territorio, use_container_width=True)
    
    figterr = px.bar(
        miembros_por_territorio,
        x="Votantes por territorio",
        y="Territorio",
        orientation="h",
        text="Votantes por territorio",
        title="Total de votantes por territorios",
        color_discrete_sequence=["green"]
    )
    figterr.update_layout(yaxis={'categoryorder':'total ascending'})
    st.header("Votantes por territorios", divider="green", text_alignment="center")
    st.plotly_chart(figterr, use_container_width=True)

    # Sección 2: Reportes por Líderes / Usuarios
    fig = px.bar(
        top5_usuarios,
        x="Votantes por coordinadores",
        y="Lider",
        orientation="h",
        text="Votantes por coordinadores",
        title="Top 5 coordinadores con más votantes",
        color_discrete_sequence=["green"]
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.header("Votantes por coordinadores", divider="green", text_alignment="center")
    st.plotly_chart(fig, use_container_width=True)
    
    st.header("Lista de votantes por coordinadores", divider="green", text_alignment="center")
    st.dataframe(miembros_por_usuario, use_container_width=True)
 
    # Sección 3: Distribución de Género General
    df_genero = pd.DataFrame({ 
        "Género": ["Hombres", "Mujeres"], 
        "Cantidad": [hombres, mujeres] 
    })
    
    df_edades = df.groupby("Rango de edad").size().reset_index(name="Cantidad").sort_values(by="Cantidad", ascending=True)

    colu1, colu2 = st.columns(2)
    colu2.fig1 = px.bar(
        df_edades, 
        x="Cantidad", 
        y="Rango de edad",   
        title="Distribución de votantes por edad", 
        #color="Rango de edad",
        #orientation="v", 
        color_discrete_sequence=["green"],
        width=900,
        height=600
    )
    st.header("Distribución de edades", divider="green", text_alignment="center")
    st.plotly_chart(colu2.fig1, use_container_width=True)
    colu1.fig2 = px.pie(
        df_genero, 
        values="Cantidad", 
        names="Género", 
        title="Porcentaje de votantes por género", 
        color="Género", 
        color_discrete_map={"Hombres": "green", "Mujeres": "lightgreen"},
         width=900,
        height=600
    )
    st.header("Distribución de género", divider="green", text_alignment="center")
    st.plotly_chart(colu1.fig2, use_container_width=True)

    # Sección 4: Desglose Cruzado de Género por Territorio
    df_totalvotantesporgeneroenterritorio = df.groupby(["Territorio", "Género"]).size().reset_index(name="Total de votantes por género y territorio").sort_values(by="Total de votantes por género y territorio", ascending=False)
    fig3 = px.bar(
        df_totalvotantesporgeneroenterritorio,
        x="Total de votantes por género y territorio",
        y="Territorio",
        orientation="h",
        text="Total de votantes por género y territorio",
        title="Total de votantes por género y territorio",
        color_discrete_map={"M": "green", "F": "lightgreen"},
        color="Género"
    )
    fig3.update_layout(yaxis={'categoryorder':'total ascending'})
    st.header("Votantes por género y territorio", divider="green", text_alignment="center")
    st.plotly_chart(fig3, use_container_width=True)

    # Sección 5: Desglose Cruzado de Género por Líder
    df_totalvotantesporgeneroyusuario = df.groupby(["Lider", "Género"]).size().reset_index(name="Total de votantes por género y usuario").sort_values(by="Total de votantes por género y usuario", ascending=False)
    fig4 = px.bar(
        df_totalvotantesporgeneroyusuario,
        x="Total de votantes por género y usuario",
        y="Lider",
        orientation="h",
        text="Total de votantes por género y usuario",
        title="Total de votantes por género y coordinador",
        color_discrete_map={"M": "green", "F": "lightgreen"},
        color="Género"
    )
    fig4.update_layout(yaxis={'categoryorder':'total ascending'})
    st.header("Votantes por género y coordinador", divider="green", text_alignment="center")
    st.plotly_chart(fig4, use_container_width=True)

    
        