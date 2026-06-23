import streamlit as st
import pandas as pd

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="Dashboard Kepuasan Mahasiswa",
    page_icon="🎓",
    layout="wide"
)

# ==========================
# CSS
# ==========================
st.markdown("""
<style>
.main-title{
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#12355B;
}

.card{
    background:#12355B;
    color:white;
    padding:20px;
    border-radius:15px;
    text-align:center;
}

section[data-testid="stSidebar"]{
    background-color:#F5F7FA;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# LOAD DATA
# ==========================
@st.cache_data
def load_data():
    return pd.read_csv("tugas pak gusti(1).csv")

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal membaca file CSV: {e}")
    st.stop()

# ==========================
# DETEKSI KOLOM SKOR
# ==========================
score_cols = [c for c in df.columns if "[Skor]" in c]

# ==========================
# SIDEBAR
# ==========================
st.sidebar.title("📋 Navigasi")

menu = st.sidebar.radio(
    "Pilih Halaman",
    [
        "Dashboard",
        "Data",
        "Analisis",
        "Masukan"
    ]
)

# ==========================
# KPI
# ==========================
if len(score_cols) > 0:
    rata = round(df[score_cols].mean().mean(), 2)
    tertinggi = int(df[score_cols].max().max())
else:
    rata = 0
    tertinggi = 0

# ==========================
# DASHBOARD
# ==========================
if menu == "Dashboard":

    st.markdown(
        '<div class="main-title">🎓 Dashboard Kepuasan Mahasiswa</div>',
        unsafe_allow_html=True
    )

    c1,c2,c3 = st.columns(3)

    c1.metric(
        "Jumlah Responden",
        len(df)
    )

    c2.metric(
        "Rata-rata Skor",
        rata
    )

    c3.metric(
        "Skor Tertinggi",
        tertinggi
    )

    st.markdown("---")

    if len(score_cols) > 0:

        st.subheader("Rata-rata Tiap Indikator")

        rata_indikator = (
            df[score_cols]
            .mean()
            .sort_values(ascending=False)
        )

        st.bar_chart(rata_indikator)

# ==========================
# DATA
# ==========================
elif menu == "Data":

    st.subheader("Data Responden")

    st.dataframe(
        df,
        use_container_width=True
    )

# ==========================
# ANALISIS
# ==========================
elif menu == "Analisis":

    st.subheader("Analisis Indikator")

    if len(score_cols) == 0:
        st.warning("Kolom [Skor] tidak ditemukan")
    else:

        indikator = st.selectbox(
            "Pilih Indikator",
            score_cols
        )

        distribusi = (
            df[indikator]
            .value_counts()
            .sort_index()
        )

        st.bar_chart(distribusi)

        st.metric(
            "Rata-rata",
            round(df[indikator].mean(),2)
        )

# ==========================
# MASUKAN
# ==========================
elif menu == "Masukan":

    st.subheader("Masukan Mahasiswa")

    masukan_cols = [
        c for c in df.columns
        if "[Masukan]" in c
    ]

    if len(masukan_cols) == 0:
        st.info("Tidak ditemukan kolom masukan")
    else:

        for col in masukan_cols:

            st.markdown(f"### {col}")

            isi = (
                df[col]
                .dropna()
                .astype(str)
            )

            for item in isi:
                if item.strip():
                    st.info(item)
