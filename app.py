import streamlit as st
import plotly.express as px
import pandas as pd

# Leer los datos del archivo
df_cars = pd.read_csv('vehicles_us.csv')

# Crear encabezado
st.header('Dashboard de precio de vehículos')

# Checkbox para la tabla de datos
show_data = st.checkbox('Mostrar tabla de datos')

# crear un slider para seleccionar el rango de años
min_year = df_cars['model_year'].min()
max_year = df_cars['model_year'].max()

year_range = st.slider(
    'Selecciona un rango de modelo/año',
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year))

# Dataframe filtrado por el rango de años seleccionado
df_filtered = df_cars[(df_cars['model_year'] >= year_range[0]) & (
    df_cars['model_year'] <= year_range[1])]

#creación del multiselect para seleccionar el tipo de modelo
model_list = list(df_cars['model'].unique())
select_model = st.multiselect('Selecciona el tipo de modelo', model_list)

#Filtrado de los datos según el modelo seleccionado
if select_model:
    df_filtered_model = df_filtered[df_filtered['model'].isin(select_model)]
else:
    df_filtered_model = df_filtered
#Mostrar el resultado del filtrado
st.write(f"Mostrando {len(df_filtered_model)} resultados basados en el modelo seleccionado")

# crear un slider para seleccionar el rango de precio
min_price = df_cars['price'].min()
max_price = df_cars['price'].max()

price_range = st.slider(
    'Selecciona un rango de precio',
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price))

# Dataframe filtrado según el rango de precio seleccionado
df_filtered_price = df_filtered_model[(df_filtered_model['price'] >= price_range[0]) & (df_filtered_model['price'] <= price_range[1])]

#Mostrar el resultado del filtrado
st.write(f"Mostrando {len(df_filtered_price)} resultados basados en el rango de precio seleccionado")

if show_data:
    st.write('Tabla de datos')
    st.dataframe(df_filtered_price)


# Gráfico de Dispersión de precios vs año
fig = px.scatter(df_filtered_price, x='model_year', y='price',
                 title='Relación entre año y precio')
st.plotly_chart(fig)

# Casilla de verificación para mostrar el histograma de precio
show_histogram = st.checkbox('Mostrar histograma de precio')

if show_histogram:
    fig_1 = px.histogram(df_filtered_price, x='price', nbins=50,
                         title='Distribución del precio')
    st.plotly_chart(fig_1)
