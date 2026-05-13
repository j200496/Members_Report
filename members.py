import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

st.set_page_config(layout="wide")

left, center, right = st.columns([2, 3, 2])

with center:
    st.image("Images/logofupu.png", 
             caption="Plataforma de reportes de la fuerza del pueblo",width=50, 
             use_container_width=True)  

st.header("Reporte de votantes inscritos", divider="green", text_alignment="center")

data = st.file_uploader("Sube el archivo excel",type=["xlsx"])

hombres = 0
mujeres = 0

if data is not None:
   df = pd.read_excel(data)
   prov = df["Territorio"].unique()
   sel = st.selectbox(
    "Filtrar por terrotorio",
    options=prov,
    index=None,
    placeholder="Buscar una territorio"
)
   sel2 = st.selectbox(
    "Filtrar por usuario",
    options=df["Inscrito por"].unique(),
    index=None,
    placeholder="Buscar un usuario"
)
   df_filter = df[df["Territorio"] == sel]
   df_filterusers = df[df["Inscrito por"] == sel2]

   hombres = (df["Género"] == "M").sum()
   mujeres = (df["Género"] == "F").sum()

   col1,col2,col3 = st.columns(3)
   c1, c2 = st.columns(2)  

   if sel:
    total = df_filter["Nombre"].count()
    col1.metric(label="Total de votantes",value=total,border=True)
    hombres = (df_filter["Género"] == "M").sum()
    col2.metric(label="Hombres",value=hombres,border=True)
    mujeres = (df_filter["Género"] == "F").sum()
    col3.metric("Mujeres",value=mujeres,border=True)
   elif sel2:
       total2 = df_filterusers["Nombre"].count()
       col1.metric(label="Total de votantes",value=total2,border=True)
       hombres = (df_filterusers["Género"] == "M").sum()
       col2.metric(label="Hombres",value=hombres,border=True)
       mujeres = (df_filterusers["Género"] == "F").sum()
       col3.metric(label="Mujeres",value=mujeres,border=True)
   else:
     total1 = df["Nombre"].count()
     col1.metric(label="Total de votantes",value=total1,border=True)
     col2.metric(label="Hombres",value=hombres,border=True)
     col3.metric(label="Mujeres",value=mujeres,border=True)

   #if sel:
     #votos = (df_filter["Estatus"] == "Ha votado").sum()
     #sinvotos = (df_filter["Estatus"] == "No ha votado").sum()
     #c1.metric(label="Total de personas que han votado",value=votos,border=True, delta=votos - sinvotos)
     #c2.metric(label="Total de personas que no han votado",value=sinvotos,border=True, delta=sinvotos - votos)
   #elif sel2:
        #votos2 = (df_filterusers["Estatus"] == "Ha votado").sum()
        #sinvotos2 = (df_filterusers["Estatus"] == "No ha votado").sum()
        #c1.metric(label="Total de personas que han votado",value=votos2,border=True,delta=votos2 - sinvotos2)
        #c2.metric(label="Total de personas que no han votado",value=sinvotos2,border=True, delta=sinvotos2 - votos2)
   #else:
       # votos1 = (df["Estatus"] == "Ha votado").sum()
        #votos2 = (df["Estatus"] == "No ha votado").sum()
        #total = df_filter["Nombre"].count()
       # c1.metric(label="Total de personas que han votado",value=votos1,border=True,delta=total - votos2)

   st.header("Total general de votantes", divider="green", text_alignment="center")
   if sel: 
    st.dataframe(df_filter)
   elif sel2:     
    st.dataframe(df_filterusers)
   else:    
    st.dataframe(df)

   miembros_por_usuario = df.groupby("Inscrito por").size().reset_index(name="Total de votantes").sort_values(by="Total de votantes",ascending=False)
   top5_usuarios = df.groupby("Inscrito por").size().reset_index(name="Votantes por usuarios").sort_values(by="Votantes por usuarios",ascending=False)
   miembros_por_terrotorio = df.groupby("Territorio").size().reset_index(name="Votantes por territorio").sort_values(by="Votantes por territorio",ascending=False)


#st.plotly_chart(fig, use_container_width=True)

if data is not None:
 fig = px.bar(
    top5_usuarios,
    x="Votantes por usuarios",
    y="Inscrito por",
    text="Votantes por usuarios",
    title="Total de votantes por usuarios",
    color_discrete_sequence=["lime"]
)
 st.header("Lista de votantes por territorios", divider="green", text_alignment="center")
 st.dataframe(miembros_por_terrotorio)
 
 if data is not None:
   figterr = px.bar(
    miembros_por_terrotorio,
    x="Votantes por territorio",
    y="Territorio",
    text="Votantes por territorio",
    title="Total de votantes por territorios",
    color_discrete_sequence=["lime"]
   )
 st.header("Votantes por territorios", divider="green", text_alignment="center")
 st.plotly_chart(figterr, use_container_width=True)



 st.header("Votantes por usuarios", divider="green", text_alignment="center")
 st.plotly_chart(fig, use_container_width=True)
 st.header("Lista de votantes por usuarios", divider="green", text_alignment="center")
 st.dataframe(miembros_por_usuario)
 
 
if data is not None:
    df_genero = pd.DataFrame({ 
        "Género": ["Hombres", "Mujeres"], 
        "Cantidad": [hombres, mujeres] 
    })

    fig2 = px.pie(
        df_genero, 
        values="Cantidad", 
        names="Género", 
        title="Porcentage de votantes por género", 
        color="Género", 
        width=600,
        height=600,
        color_discrete_map={"Hombres": "green", "Mujeres": "lime"}
    )

    st.header("Distribución de género", divider="green")
    st.plotly_chart(fig2, use_container_width=True)

    
if data is not None:
  df_totalvotantesporgeneroenterritorio = df.groupby(["Territorio", "Género"]).size().reset_index(name="Total de votantes por género y territorio").sort_values(by="Total de votantes por género y territorio",ascending=False)
  fig3 = px.bar(
    df_totalvotantesporgeneroenterritorio,
    x="Total de votantes por género y territorio",
    y="Territorio",
    text="Total de votantes por género y territorio",
    title="Total de votantes por género y territorio",
    color_discrete_map={"M": "green", "F": "lime"},
    color="Género"
  )
  st.header("Votantes por género y territorio", divider="green", text_alignment="center")
  st.plotly_chart(fig3, use_container_width=True)




if data is not None:
  df_totalvotantesporgeneroyusuario = df.groupby(["Inscrito por", "Género"]).size().reset_index(name="Total de votantes por género y usuario").sort_values(by="Total de votantes por género y usuario",ascending=False)
  fig4 = px.bar(
    df_totalvotantesporgeneroyusuario,
    x="Total de votantes por género y usuario",
    y="Inscrito por",
    text="Total de votantes por género y usuario",
    title="Total de votantes por género y usuario",
    color_discrete_map={"M": "green", "F": "lime"},
    color="Género"
  )
  st.header("Votantes por género y usuario", divider="green", text_alignment="center")
  st.plotly_chart(fig4, use_container_width=True)