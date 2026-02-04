import pandas as pd
import streamlit as st
import plotly.express as px

a,b = st.columns(2)
#b.image("Images/logofupu.png",caption="La fuerza del pueblo",width=100)
st.title("Reporte de miembros")

data = st.file_uploader("Sube el archivo excel",type=["xlsx"])

if data is not None:
   df = pd.read_excel(data)
   prov = df["Territorio"].unique()
   sel = st.selectbox(
    "Filtrar por terrotorio",
    options=prov,
    index=None,
    placeholder="Selecciona una territorio"
)
   df_filter = df[df["Territorio"] == sel]
   
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
   else:
     total1 = df["Nombre"].count()
     col1.metric(label="Total de miembros",value=total1,border=True)
     col2.metric(label="Hombres",value=hombres,border=True)
     col3.metric(label="Mujeres",value=mujeres,border=True)

   if sel: 
    st.dataframe(df_filter)
   else:
    st.dataframe(df)

   miembros_por_usuario = df.groupby("Inscrito por").size().reset_index(name="Total de miembros").sort_values(by="Total de miembros",ascending=False)
   top5_usuarios = df.groupby("Inscrito por").size().reset_index(name="Miembros por usuarios").sort_values(by="Miembros por usuarios",ascending=False).head(5)
   st.title("5 usuarios con mas miembros")
   fig = px.bar(
    miembros_por_usuario,
    x="Inscrito por",
    y="Total de miembros",
    title="Miembros por usuario",
    text="Total de miembros",
    color="Total de miembros"
)

st.plotly_chart(fig, use_container_width=True)
st.title("Cantidad de miembros por usuarios")
st.dataframe(miembros_por_usuario)