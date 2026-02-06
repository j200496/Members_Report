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
   top5_usuarios = df.groupby("Inscrito por").size().reset_index(name="Miembros por usuarios").sort_values(by="Miembros por usuarios",ascending=True).tail(5)
   miembros_por_terrotorio = df.groupby("Territorio").size().reset_index(name="Miembros por territorio").sort_values(by="Miembros por territorio",ascending=False)






#st.plotly_chart(fig, use_container_width=True)

if data is not None:
 fig = px.bar(
    top5_usuarios,
    x="Miembros por usuarios",
    y="Inscrito por",
    text="Miembros por usuarios",
    title="Top 5 usuarios con más miembros",
    color="Miembros por usuarios"
)
 st.title("Total de miembros por territorios")
 st.dataframe(miembros_por_terrotorio)
 st.title("5 Usuarios con mas miembros")
 st.plotly_chart(fig, use_container_width=True)
 st.title("Total de miembros por usuarios")
 st.dataframe(miembros_por_usuario)
