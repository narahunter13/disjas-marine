import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as plt
from PIL import Image

data = pd.read_csv('data.csv')
data['TIMESTAMP_UTC'] = data['TIMESTAMP_UTC'].apply(lambda x : pd.to_datetime(x, unit = 's').strftime('%d-%m-%Y'))

by_timestamp = pd.DataFrame(data.groupby('TIMESTAMP_UTC').size().reset_index(name = 'Frekuensi'))
by_timestamp.columns = ['Tanggal', 'Frekuensi']
by_timestamp = by_timestamp.set_index('Tanggal')

origin_name = pd.DataFrame(data[['TIMESTAMP_UTC','FROM_PORT_NAME']]).fillna('TIDAK DIKETAHUI')

orig_17 = pd.DataFrame(origin_name.loc[lambda x : x['TIMESTAMP_UTC'] == '17-12-2021', 'FROM_PORT_NAME'].value_counts().reset_index(name = 'JUMLAH'))
orig_17.columns = ['ASAL PELABUHAN', 'JUMLAH']
fig1 = plt.pie(orig_17, 'ASAL PELABUHAN', 'JUMLAH')

orig_18 = pd.DataFrame(origin_name.loc[lambda x : x['TIMESTAMP_UTC'] == '18-12-2021', 'FROM_PORT_NAME'].value_counts().reset_index(name = 'JUMLAH'))
orig_18.columns = ['ASAL PELABUHAN', 'JUMLAH']
fig2 = plt.pie(orig_18, 'ASAL PELABUHAN', 'JUMLAH')

arr_df_17 = pd.DataFrame(data.loc[lambda x : x['TIMESTAMP_UTC'] == '17-12-2021', 'MOVE_TYPE_NAME'].value_counts().reset_index(name = 'JUMLAH'))
arr_df_17.columns = ['JENIS PERGERAKAN', 'JUMLAH']
arr_df_17['JENIS PERGERAKAN'] = arr_df_17['JENIS PERGERAKAN'].apply(lambda x : 'KEBERANGKATAN' if x=='DEPARTURE' else 'KEDATANGAN')
arr_df_17.insert(0, 'TANGGAL', ['17-12-2021','17-12-2021'])

arr_df_18 = pd.DataFrame(data.loc[lambda x : x['TIMESTAMP_UTC'] == '18-12-2021', 'MOVE_TYPE_NAME'].value_counts().reset_index(name = 'JUMLAH'))
arr_df_18.columns = ['JENIS PERGERAKAN', 'JUMLAH']
arr_df_18['JENIS PERGERAKAN'] = arr_df_18['JENIS PERGERAKAN'].apply(lambda x : 'KEBERANGKATAN' if x=='DEPARTURE' else 'KEDATANGAN')
arr_df_18.insert(0, 'TANGGAL', ['18-12-2021','18-12-2021'])

arr_dep = pd.concat([arr_df_17, arr_df_18])

fig3 = plt.bar(arr_dep, 'TANGGAL', 'JUMLAH', 'JENIS PERGERAKAN')

most_ship = pd.DataFrame(data.groupby('SHIPNAME').size().reset_index(name = 'JUMLAH'))
most_ship.columns = ['NAMA KAPAL', 'FREKUENSI']
most_ship = most_ship[:5]

st.sidebar.header('Tugas Individu Statistik Distribusi dan Jasa')
option = st.sidebar.selectbox(
    'Pilih Menu:',
    ('Dashboard', 'Author')
)


if option == 'Dashboard' or option == '':
    st.title("Visualisasi Data Marine Traffic (17 Desember - 18 Desember 2021)")
    st.header("Jumlah Kapal di Pelabuhan (Menurut Hari)")
    st.bar_chart(by_timestamp)
    st.header("Asal Kapal yang Datang (17 Desember 2021)")
    st.plotly_chart(fig1)
    st.header("Asal Kapal yang Datang (18 Desember 2021)")
    st.plotly_chart(fig2)
    st.header('Jenis dan Jumlah Pergerakan Kapal (Menurut Hari)')
    st.plotly_chart(fig3)
    st.header('5 Kapal Paling Sering di Pelabuhan')
    st.table(most_ship)
elif option == 'Author':
    st.title("Author")
    st.markdown("Tugas ini dibuat untuk memenuhi tugas mata kuliah Statistik Distribusi dan Jasa. Tugas ini bertujuan untuk melakukan visualisasi data kemaritiman Pelabuhan Batu Ampar. Data yang ada diperoleh dari website **_marinetraffic.com_** sebanyak 168 data dengan periode yang terbatas, yaitu dari tanggal 17 Desember 2021 - 18 Desember 2021.")
    st.markdown("""
        <style>
        .big-font {
            font-size:1rem !important;
            font-weight: bold;
            margin-bottom: 0;
        }
        .image-profile {
            width: 70% !important;
            height: auto !important;
        }
        </style>
        """, unsafe_allow_html=True)
    st.markdown('<p class="big-font">DOSEN PENGAMPU:</p>', unsafe_allow_html=True)
    st.markdown('DR. IR. SASMITO HADI WIBOWO, M.SC.')
    st.markdown('<p class="big-font">DATA MAHASISWA:</p>', unsafe_allow_html=True)
    image = Image.open('foto.jpg')
    st.image(image, width = 256)
    st.markdown('M. RIFKY NARATAMA SUSANTO<BR>221810473<BR>4SI2', unsafe_allow_html=True)