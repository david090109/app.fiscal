import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

data = pd.read_csv("munis.csv")

st.title("Mi primera app")

munis = data["entidad"].unique().tolist()

mun = st.selectbox("Selecciones un municipio:", 
             munis)

filtro = data[data["entidad"]==mun]

st.dataframe(filtro)

gen = (filtro
       .groupby("clas_gen")["total_recaudo"]
       .sum())
total_gen = gen.sum()

gen = (gen/total_gen).round(2)


det = (filtro
       .groupby("clasificacion_ofpuj")["total_recaudo"]
       .sum())
total_det = det.sum()

det = (det/total_det).round(3)

st.dataframe(gen) # clasificación general

st.dataframe(det) #clasificación detallada

# Grafico de torta

fig, ax = plt.subplots(1, 1, figsize=(10, 6))
ax.pie(det.values, labels=det.index)

st.pyplot(fig)

fig, ax = plt.subplots(1, 1, figsize=(10, 6))
ax.pie(gen.values, labels=gen.index)

st.pyplot(fig)

# treemap

fin = (filtro
       .groupby(["clas_gen",
                  "clasificacion_ofpuj"])
                  ["total_recaudo"]
                  .sum()
                  .reset_index())
st.dataframe(fin)

fig = px.treemap(fin, path=[px.Constant("total"),
                            "clas_gen",
                            "clasificacion_ofpuj"],
                            values="total_recaudo")

st.plotly_chart(fig)

