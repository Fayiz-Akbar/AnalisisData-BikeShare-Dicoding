import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

hour_df = pd.read_csv('dashboard/all_data.csv')

season_map = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}
weather_map = {
    1: 'Clear',
    2: 'Cloudy',
    3: 'Light Snow/Rain',
    4: 'Heavy Rain/Ice Pallets'
}
hour_df['season'] = hour_df['season'].map(season_map)
hour_df['weathersit'] = hour_df['weathersit'].map(weather_map)

datetime_columns = ["dteday"]
hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)
for column in datetime_columns:
    hour_df[column] = pd.to_datetime(hour_df[column])

min_date = hour_df["dteday"].min()
max_date = hour_df["dteday"].max()

with st.sidebar:
    st.image("https://static.vecteezy.com/system/resources/previews/019/474/889/original/bike-sharing-services-isometric-icon-illustration-vector.jpg", use_container_width=True)
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date))]

st.subheader('Rata-rata Peminjaman Berdasarkan Cuaca dan Jenis Hari')
if 'day_type' in hour_df.columns:
    avg_rent_weather_daytype = hour_df.groupby(['weathersit', 'day_type'])['cnt'].mean().reset_index()
    plt.figure(figsize=(8, 6))
    sns.barplot(data=avg_rent_weather_daytype, x='weathersit', y='cnt', hue='day_type')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Rata-rata Jumlah Peminjaman')
    plt.title('Rata-rata Peminjaman Sepeda')
    st.pyplot(plt)
else:
    st.warning("Kolom 'day_type' tidak ditemukan dalam dataset.")

st.subheader('Rata-rata Peminjaman Sepeda per Jam')
avg_by_hour = hour_df.groupby('hr')['cnt'].mean()
plt.figure(figsize=(12, 6))
avg_by_hour.plot(kind='line', marker='o')
plt.title('Peminjaman Sepeda per Jam')
plt.xlabel('Jam')
plt.ylabel('Jumlah Rata-rata Peminjaman')
plt.grid(True)
plt.xticks(range(0, 24))
st.pyplot(plt)

monthly_rentals = hour_df.copy()
monthly_rentals['mnth'] = monthly_rentals['dteday'].dt.strftime('%B')  
monthly_rentals['yr'] = monthly_rentals['dteday'].dt.year.astype(str)   

monthly_rentals = monthly_rentals.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()


monthly_rentals['date'] = monthly_rentals['yr'] + '-' + monthly_rentals['mnth']
monthly_rentals['date'] = pd.to_datetime(monthly_rentals['date'], format='%Y-%B')
monthly_rentals = monthly_rentals.sort_values('date')

st.subheader('Total Penyewaan Sepeda per Bulan')
fig3, ax3 = plt.subplots(figsize=(14, 6))
ax3.plot(monthly_rentals['date'], monthly_rentals['cnt'], marker='o', label='Total Rentals (cnt)', color='skyblue')
ax3.set_title('Monthly Bike Rentals Over Two Years')
ax3.set_xlabel('Tanggal')
ax3.set_ylabel('Jumlah Peminjaman')
ax3.legend()
ax3.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig3)

st.subheader('Heatmap Penyewaan Berdasarkan Cuaca dan Jenis Hari')
if 'workingday' in hour_df.columns:
    cluster_counts = hour_df.groupby(['weathersit', 'workingday'])['cnt'].sum().reset_index()
    heatmap_data = cluster_counts.pivot(index='weathersit', columns='workingday', values='cnt')
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='magma')
    plt.xlabel('Hari Kerja (0 = Libur, 1 = Kerja)')
    plt.ylabel('Kondisi Cuaca')
    plt.title('Jumlah Penyewaan Sepeda')
    st.pyplot(plt)
else:
    st.warning("Kolom 'workingday' tidak ditemukan dalam dataset.")

st.caption('Copyright © Fayiz Akbar Daifullah 2025')
