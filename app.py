import pickle
import streamlit as st
import pandas as pd
import pydeck as pdk
import random as np
import datetime
import sqlite3

# Carrega o arquivo Pickle eportado pelo notebook
#with open('df_position_02_03', 'rb') as file:
#    df_position = pickle.load(file)

# connection from Data Base
conn = sqlite3.connect('tracker.db')
cursor = conn.cursor()

# Select and convertion to Data Frame
df_position = pd.DataFrame(cursor.execute('select * from positions').fetchall(), 
    columns=['id', 'placa', 'dataEquipamento',  'lat', 
    'lon', 'endereco', 'date_request', 'time_request'])   
conn.close()

# Exporting pickle from data to test dataframe
#with open('df_position_from_app.pkl', 'wb') as file:
#    pickle.dump(df_position, file)

# Mensagem no título e corpo da página
st.title("Veículos SegTruck")
st.write(f"""
## Posições dos Veículos
""")

# Menu filter
range_time = df_position['time_request'].unique()
minimum = int(range_time.min())
maximum = int(range_time.max())
placa = st.sidebar.text_input('Digite a Placa.') # recebe a digitacao da placa
date = st.sidebar.date_input('Selecione uma Data.') # Seleciona a data
time = st.sidebar.slider('Escolha o Horário.', minimum, maximum)


if placa:
    data = df_position[(
        df_position['placa'] == str(placa)) & (
        df_position['date_request'] == str(date)) & (
        df_position['time_request'] == int(time))]
    f"""{data.shape[0]} Veículos no mapa."""
    st.map(data)
else:
    data = df_position[(
        df_position['date_request'] == str(date)) & (
        df_position['time_request'] == int(time))].copy()
    # Mostra a quantidade de veículos aparecendo no mapa
    f"""{data.shape[0]} Veículos no mapa."""
    st.map(data)


'Data Selecionada:', date, placa

# Mostra todas as localizacoes sem filtro
if st.checkbox('Rotas mais Utilizadas acumulados'):
    st.map(df_position)