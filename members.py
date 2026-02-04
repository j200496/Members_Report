import pandas as pd
import streamlit as st

a,b = st.columns(2)
b.image("Images/logofupu.png",caption="La fuerza del pueblo",width=100)
st.title("Reporte de miembros")

data = st.file_uploader("Sube el archivo excel",type=["xlsx"])

if data is not None:
   df = pd.read_excel(data)
   prov = df["Provincia"].unique()
   sel = st.selectbox(
    "Filtrar por terrotorio",
    options=prov,
    index=None,
    placeholder="Selecciona una territorio"
)
   df_filter = df[df["Provincia"] == sel]

   if sel:
    total = df_filter["Nombre"].count()
    st.metric(label="Total de miembros",value=total)
   else:
     total1 = df["Nombre"].count()
     st.metric(label="Total de miembros",value=total1)

   if sel: 
    st.dataframe(df_filter)
   else:
    st.dataframe(df)

