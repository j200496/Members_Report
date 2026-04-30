import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

st.set_page_config(layout="wide")

a,b = st.columns(2)
b.image("Images/logofupu.png",caption="La fuerza del pueblo",width=100)
st.title("Reporte de votantes inscritos")

data = st.file_uploader("Sube el archivo excel",type=["xlsx"])

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

   if sel:
    total = df_filter["Nombre"].count()
    col1.metric(label="Total de miembros",value=total,border=True)
    hombres = (df_filter["Género"] == "M").sum()
    col2.metric(label="Hombres",value=hombres,border=True)
    mujeres = (df_filter["Género"] == "F").sum()
    col3.metric("Mujeres",value=mujeres,border=True)
   elif sel2:
       total2 = df_filterusers["Nombre"].count()
       col1.metric(label="Total de miembros",value=total2,border=True)
       hombres = (df_filterusers["Género"] == "M").sum()
       col2.metric(label="Hombres",value=hombres,border=True)
       mujeres = (df_filterusers["Género"] == "F").sum()
       col3.metric(label="Mujeres",value=mujeres,border=True)
   else:
     total1 = df["Nombre"].count()
     col1.metric(label="Total de miembros",value=total1,border=True)
     col2.metric(label="Hombres",value=hombres,border=True)
     col3.metric(label="Mujeres",value=mujeres,border=True)

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
    color="Votantes por usuarios"
)
 st.title("Total de votantes por territorios")
 st.dataframe(miembros_por_terrotorio)
 st.title("Votantes por usuarios")
 st.plotly_chart(fig, use_container_width=True)
 st.title("Total de votantes por usuarios")
 st.dataframe(miembros_por_usuario)
