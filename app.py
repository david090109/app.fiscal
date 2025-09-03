import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd

data = pd.read_csv("munis.csv")
gdf = gpd.read_parquet("munis.parquet")

st.title("Mi primera app")

munis = data["entidad"].unique().tolist()

mun = st.selectbox("Selecciones un municipio:", 
             munis)

filtro = data[data["entidad"]==mun]



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





# Grafico de torta

fig, ax = plt.subplots(1, 1, figsize=(10, 6))
ax.pie(det.values, labels=det.index)

fig = px.pie(names=gen.index, 
             values=gen.values,
             title="distribucion general de recursos",
             color_discrete_sequence=["#639FAB","#BBCDE5","#1C5D99"])

st.plotly_chart(fig)
fig, ax = plt.subplots(1, 1, figsize=(10, 6))
ax.pie(gen.values, labels=gen.index)

colores_personalizados = ["#639FAB","#BBCDE5","#1C5D99" ]



# treemap

fin = (filtro
       .groupby(["clas_gen",
                  "clasificacion_ofpuj"])
                  ["total_recaudo"]
                  .sum()
                  .reset_index())


fig = px.treemap(fin, path=[px.Constant("total"),
                            "clas_gen",
                            "clasificacion_ofpuj"],
                            values="total_recaudo",
                            color_discrete_sequence=["#639FAB","#BBCDE5","#1C5D99"])

st.plotly_chart(fig)

# mapa
filtro2 = gdf[gdf["entidad"]==mun][["codigo_alt", "geometry"]]

fig, ax = plt.subplots(1, 1)

filtro2.plot(ax=ax)

ax.set_axis_off()

st.pyplot(fig)