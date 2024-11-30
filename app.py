import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Pengaturan halaman
st.set_page_config(page_title="Bike Sharing Analysis", layout="wide")

# Judul Aplikasi
st.title("Analisis Data Bike Sharing")
st.markdown("Sebuah aplikasi untuk menganalisis pengaruh cuaca dan hari kerja terhadap jumlah peminjaman sepeda.")

# Sidebar
st.sidebar.header("Navigasi")
page = st.sidebar.radio("Pilih Halaman:", ["Dataframe", "EDA", "Analisis Lanjutan", "Kesimpulan"])

# Load Dataset
@st.cache_data
def load_data():
    day_df = pd.read_csv("https://raw.githubusercontent.com/nursaiid154/Bike-sharing-dataset/refs/heads/main/day.csv")
    return day_df

day_df = load_data()

# Halaman Dataframe
if page == "Dataframe":
    st.subheader("Dataset Bike Sharing")
    st.write("Berikut adalah cuplikan data Bike Sharing:")
    st.dataframe(day_df.head())

    st.write("**Statistik Deskriptif Dataset:**")
    st.write(day_df.describe())

# Halaman EDA
elif page == "EDA":
    st.subheader("Exploratory Data Analysis (EDA)")

    # Visualisasi Pengaruh Cuaca
    st.write("**Pengaruh Cuaca terhadap Jumlah Peminjaman Sepeda**")
    fig1, ax1 = plt.subplots()
    sns.boxplot(x='weathersit', y='cnt', data=day_df, ax=ax1)
    ax1.set_title("Pengaruh Cuaca terhadap Jumlah Peminjaman")
    ax1.set_xlabel("Kondisi Cuaca (1: Baik, 4: Buruk)")
    ax1.set_ylabel("Jumlah Peminjaman")
    st.pyplot(fig1)

    # Visualisasi Hari Kerja
    st.write("**Peminjaman Sepeda Berdasarkan Hari Kerja**")
    fig2, ax2 = plt.subplots()
    sns.barplot(x='workingday', y='cnt', data=day_df, ci=None, ax=ax2)
    ax2.set_title("Peminjaman Sepeda pada Hari Kerja vs Hari Libur")
    ax2.set_xlabel("Hari Kerja (1=Ya, 0=Tidak)")
    ax2.set_ylabel("Jumlah Peminjaman")
    st.pyplot(fig2)

# Halaman Analisis Lanjutan
elif page == "Analisis Lanjutan":
    st.subheader("Analisis Lanjutan: RFM Analysis")
    st.write("Melakukan analisis kebiasaan pengguna dengan metrik seperti Recency, Frequency, dan Monetary.")

    # Data Agregasi
    rfm_data = day_df[['dteday', 'casual', 'registered', 'cnt']].copy()
    rfm_data['dteday'] = pd.to_datetime(rfm_data['dteday'])
    current_date = rfm_data['dteday'].max()
    rfm_summary = rfm_data.groupby('dteday').agg({
        'cnt': 'sum', 'casual': 'sum', 'registered': 'sum'
    }).reset_index()
    rfm_summary['Recency'] = (current_date - rfm_summary['dteday']).dt.days

    # Distribusi Recency
    st.write("**Distribusi Recency**")
    fig3, ax3 = plt.subplots()
    sns.histplot(rfm_summary['Recency'], bins=30, kde=True, ax=ax3)
    ax3.set_title("Distribusi Recency (Baru/Berkala)")
    ax3.set_xlabel("Hari sejak peminjaman terakhir")
    ax3.set_ylabel("Jumlah Hari")
    st.pyplot(fig3)

    # Frequency vs Monetary
    st.write("**Frequency vs Monetary**")
    fig4, ax4 = plt.subplots()
    sns.scatterplot(x=rfm_summary['casual'], y=rfm_summary['cnt'], label='Casual Users', ax=ax4)
    sns.scatterplot(x=rfm_summary['registered'], y=rfm_summary['cnt'], label='Registered Users', color='orange', ax=ax4)
    ax4.set_title("Frequency vs Monetary")
    ax4.set_xlabel("Frequency")
    ax4.set_ylabel("Monetary (Total Peminjaman)")
    ax4.legend()
    st.pyplot(fig4)

# Halaman Kesimpulan
elif page == "Kesimpulan":
    st.subheader("Kesimpulan")
    st.write("""
    **Pertanyaan 1:** Cuaca buruk secara signifikan menurunkan jumlah peminjaman sepeda, sedangkan cuaca baik meningkatkan jumlah peminjaman.

    **Pertanyaan 2:** Peminjaman sepeda lebih banyak terjadi pada hari kerja dibandingkan hari libur.

    **Insight Tambahan:**
    - Pengguna terdaftar cenderung memiliki pola peminjaman yang lebih konsisten dibandingkan pengguna casual.
    - Data recency menunjukkan bahwa sepeda sering digunakan sebagai transportasi rutin oleh mayoritas pengguna.
    """)