import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    df_day = pd.read_csv("day.csv")  # Data harian
    df_hour = pd.read_csv("hour.csv")  # Data per jam
    df_day["dteday"] = pd.to_datetime(df_day["dteday"])  # Konversi ke datetime
    return df_day, df_hour

df_day, df_hour = load_data()

# Cek apakah kolom yang diperlukan ada
def check_columns(df, required_cols):
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"Kolom yang hilang: {missing_cols}")
        return False
    return True

# Mapping nilai numerik ke nama bulan dan tahun
mapping_yr = {0: '2011', 1: '2012'}
mapping_mnth = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
df_day['yr'] = df_day['yr'].map(mapping_yr)
df_day['mnth'] = df_day['mnth'].map(mapping_mnth)

# Sidebar Navigation
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman:", ["EDA", "Visualisasi Data", "Analisis Lanjutan"], key="main_page_selector")

# EDA Page
if page == "EDA":
    st.title("📊 Eksplorasi Data (EDA)")
    st.write("Tampilkan sekilas data mentah serta ringkasan statistiknya.")
    
    if st.checkbox("Tampilkan Data Mentah"):
        st.write(df_day)
    
    st.write("### Statistik Data Harian")
    st.write(df_day.describe(include='all'))
    st.markdown("""
    **Penjelasan:**
    Dataset ini terdiri dari **731 entri** yang mencakup informasi penggunaan fasilitas berdasarkan hari. Setelah dilakukan analisis statistik deskriptif, ditemukan bahwa **suhu rata-rata adalah 0.49**, dengan nilai minimum **0.05** dan maksimum **0.86**. **Kelembapan** cenderung tinggi dengan rata-rata **0.62**, sementara **kecepatan angin** memiliki nilai rata-rata **0.19**, menunjukkan bahwa dalam sebagian besar hari, kondisi angin relatif tenang.
    """)
    
    st.write("### Statistik Data Per Jam")
    st.write(df_hour.describe(include='all'))
    st.markdown("""
    **Penjelasan:**
    Dataset ini memiliki ukuran yang lebih besar dibandingkan dataset harian, dengan **17.379 entri**, yang merepresentasikan pola penggunaan fasilitas berdasarkan jam. Dari segi waktu, data menunjukkan bahwa **aktivitas penggunaan fasilitas cenderung meningkat pada siang hari**, dengan median jam penggunaan berada pada **pukul 12:00 siang**. Namun, terdapat juga variasi yang cukup besar tergantung pada faktor **hari kerja dan musim**.
    
    Dari segi cuaca, **suhu rata-rata dalam dataset ini mirip dengan dataset harian**, yaitu sekitar **0.49**, dengan kelembapan rata-rata **0.62** dan kecepatan angin **0.19**. Kondisi ini menunjukkan tren yang konsisten antara data harian dan per jam terkait kondisi lingkungan.
    
    Dari segi **hari kerja**, dataset menunjukkan bahwa sekitar **68% hari merupakan hari kerja**, yang berarti penggunaan fasilitas kemungkinan lebih banyak terjadi pada hari-hari kerja dibandingkan akhir pekan. Pola musiman juga tampak jelas dengan perbedaan penggunaan di setiap musim. Secara umum, dataset ini memberikan gambaran yang baik tentang bagaimana faktor-faktor lingkungan dan kalender dapat memengaruhi penggunaan fasilitas secara harian.
    """)
    
    st.write("### Analisis Penggunaan Fasilitas Berdasarkan Musim")
    seasonal_analysis = df_hour.groupby("season").aggregate(
        dteday_nunique=("dteday", "nunique"),
        cnt_max=("cnt", "max"),
        cnt_min=("cnt", "min"),
        cnt_mean=("cnt", "mean"),
        cnt_std=("cnt", "std")
    )
    st.write(seasonal_analysis)
    st.markdown("""
    **Penjelasan:**
    Setelah saya perhatikan, berdasarkan musim terlihat bahwa **jumlah penggunaan fasilitas bervariasi di setiap musim**. Contohnya, pada **musim ketiga (musim panas), penggunaan fasilitas memiliki rata-rata tertinggi sekitar 236 pengguna per jam**, sementara musim lainnya menunjukkan angka yang lebih rendah. Berarti faktor **cuaca dan musim memiliki pengaruh signifikan terhadap pola penggunaan fasilitas**.
    """)
    
# Visualisasi Data Page
elif page == "Visualisasi Data":
    st.title("📈 Visualisasi Data")
    
    # 1. Tren Penyewaan Sepeda Perbulan
    st.markdown("### Tren Penyewaan Sepeda Perbulan (2011 vs 2012)")
    order_months = list(mapping_mnth.values())
    df_day["mnth"] = pd.Categorical(df_day["mnth"], categories=order_months, ordered=True)
    
    def plot_monthly_rentals(data):
        if check_columns(data, ["yr", "mnth", "cnt"]):
            monthly_trend = data.groupby(["yr", "mnth"])['cnt'].sum().reset_index()
            plt.figure(figsize=(12, 6))
            sns.lineplot(data=monthly_trend, x='mnth', y='cnt', hue='yr', marker='o', linewidth=2)
            plt.title('Tren Penyewaan Sepeda Per Bulan (2011 vs 2012)', fontsize=14)
            plt.xlabel('Bulan', fontsize=12)
            plt.ylabel('Jumlah Penyewaan', fontsize=12)
            plt.xticks(rotation=45)
            plt.legend(title='Tahun')
            plt.grid(True, linestyle='--', alpha=0.6)
            st.pyplot(plt)
    
    plot_monthly_rentals(df_day)
    
    # Penjelasan
    st.markdown("#### Penjelasan")
    st.markdown("""
    *1. Peningkatan Penyewaan di Tahun 2012*
    - Secara keseluruhan, jumlah penyewaan sepeda di tahun 2012 lebih tinggi dibandingkan tahun 2011 di setiap bulan.
    - Hal ini menunjukkan adanya peningkatan permintaan terhadap layanan penyewaan sepeda.
    
    *2. Pola Musiman dalam Penyewaan*
    - Penyewaan sepeda cenderung meningkat dari Januari hingga puncaknya di Juni hingga September, sebelum menurun kembali pada akhir tahun.
    - Tren ini terjadi di kedua tahun, menunjukkan bahwa musim dan cuaca berpengaruh terhadap jumlah penyewaan.
    """)
    
    # 2. Penyewaan Berdasarkan Musim
    st.markdown("### Musim dengan Penyewaan Tertinggi")
    season_mapping = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    df_day['season'] = df_day['season'].map(season_mapping)
    
    def peak_season_analysis(data):
        if check_columns(data, ["season", "cnt"]):
            seasonal_counts = data.groupby('season')['cnt'].sum().sort_values(ascending=False)
            colors = {'Winter': 'lightskyblue', 'Spring': 'lightgreen', 'Summer': 'gold', 'Fall': 'lightcoral'}
            
            plt.figure(figsize=(10, 6))
            plt.bar(seasonal_counts.index, seasonal_counts.values, color=[colors[season] for season in seasonal_counts.index], edgecolor='black')
            plt.xlabel('Musim')
            plt.ylabel('Total Penyewaan')
            plt.title('Total Penyewaan Sepeda Berdasarkan Musim')
            
            for i, value in enumerate(seasonal_counts.values):
                plt.text(i, value + 500, str(value), ha='center', va='bottom')
            
            st.pyplot(plt)
    
    peak_season_analysis(df_day)
    
    # Penjelasan
    st.markdown("#### Penjelasan")
    st.markdown("""
    Musim panas memiliki jumlah penyewaan tertinggi dengan *1.061.129 penyewaan*.
    
    Hal ini kemungkinan besar disebabkan oleh:
    - Cuaca yang lebih mendukung untuk aktivitas luar ruangan.
    - Hari yang lebih panjang.
    - Liburan musim panas yang meningkatkan mobilitas masyarakat.
    """)

# Analisis Lanjutan Page
elif page == "Analisis Lanjutan":
    st.title("🔍 Analisis Lanjutan")
    st.markdown("### Heatmap Penyewaan Sepeda berdasarkan Hari dan Jam")
    if check_columns(df_hour, ["weekday", "hr", "cnt"]):
        clustering = df_hour.groupby(['weekday', 'hr'])['cnt'].sum().unstack()
        
        def plot_heatmap(data):
            plt.figure(figsize=(12, 8))
            sns.heatmap(data, cmap="YlGnBu", annot=False, fmt=".0f")
            plt.title('Heatmap Penyewaan Sepeda berdasarkan Hari Kerja dan Jam')
            plt.xlabel('Jam')
            plt.ylabel('Hari')
            st.pyplot(plt)
        
        plot_heatmap(clustering)
    
    # Penjelasan
    st.markdown("#### Penjelasan")
    st.markdown("""
    1. Puncak penyewaan terjadi pada jam *7-9 pagi* dan *17-19 sore* di hari kerja (Senin-Jumat).
    2. Pada akhir pekan (Sabtu-Minggu), pola penyewaan lebih tersebar merata sepanjang hari, dengan peningkatan aktivitas pada siang hingga sore hari.
    """)
