import streamlit as st
import pandas as pd

# ==========================
# KONFIGURASI HALAMAN
# ==========================
st.set_page_config(
    page_title="Survey Kepuasan Mahasiswa UMAHA",
    page_icon="🎓",
    layout="wide"
)

# ==========================
# DATA CONTOH
# ==========================
df = pd.DataFrame({
    "Program Studi": [
        "Teknik Industri",
        "Informatika",
        "Manajemen",
        "Akuntansi",
        "Keperawatan"
    ],
    "Jumlah Responden": [120, 150, 100, 90, 80],
    "Skor Kepuasan": [4.5, 4.3, 4.4, 4.2, 4.6]
})

# ==========================
# CSS
# ==========================
st.markdown("""
<style>
.main-title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#0A4D68;
}

.subtitle{
    text-align:center;
    color:#555;
    font-size:18px;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# SIDEBAR
# ==========================
st.sidebar.title("📋 Menu")
menu = st.sidebar.radio(
    "Pilih Halaman",
    ["Dashboard", "Data Survey", "Analisis"]
)

# ==========================
# DASHBOARD
# ==========================
if menu == "Dashboard":

    st.markdown(
        '<div class="main-title">🎓 Survey Kepuasan Mahasiswa UMAHA</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Universitas Maarif Hasyim Latif</div>',
        unsafe_allow_html=True
    )

    total_responden = df["Jumlah Responden"].sum()
    rata_kepuasan = round(df["Skor Kepuasan"].mean(), 2)
    skor_tertinggi = df["Skor Kepuasan"].max()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Responden",
        total_responden
    )

    col2.metric(
        "Rata-rata Kepuasan",
        rata_kepuasan
    )

    col3.metric(
        "Skor Tertinggi",
        skor_tertinggi
    )

    st.markdown("---")

    st.subheader("📈 Skor Kepuasan per Program Studi")
    st.bar_chart(
        df.set_index("Program Studi")["Skor Kepuasan"]
    )

    st.subheader("👥 Jumlah Responden")
    st.line_chart(
        df.set_index("Program Studi")["Jumlah Responden"]
    )

# ==========================
# DATA SURVEY
# ==========================
elif menu == "Data Survey":

    st.header("📊 Data Survey")

    st.dataframe(
        df,
        use_container_width=True
    )

# ==========================
# ANALISIS
# ==========================
elif menu == "Analisis":

    st.header("📋 Analisis Kepuasan")

    prodi_terbaik = df.loc[
        df["Skor Kepuasan"].idxmax(),
        "Program Studi"
    ]

    prodi_terendah = df.loc[
        df["Skor Kepuasan"].idxmin(),
        "Program Studi"
    ]

    st.success(
        f"Program Studi dengan kepuasan tertinggi: {prodi_terbaik}"
    )

    st.warning(
        f"Program Studi dengan kepuasan terendah: {prodi_terendah}"
    )

    st.subheader("Rata-rata Kepuasan")

    st.progress(
        int(df["Skor Kepuasan"].mean() * 20)
    )

    st.write(
        f"Nilai rata-rata kepuasan mahasiswa adalah **{round(df['Skor Kepuasan'].mean(),2)} dari 5.0**"
    )
