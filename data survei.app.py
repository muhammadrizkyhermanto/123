import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Dashboard Analisis Kepuasan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.main-title{
    font-size:38px;
    font-weight:bold;
    color:#173F5F;
    text-align:center;
}

.metric-box{
    background:#1f4e79;
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;
}

section[data-testid="stSidebar"]{
    background-color:#f5f7fa;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("tugas pak gusti(1).csv")

df = load_data()

# =========================
# DETEKSI KOLOM SKOR
# =========================
score_cols = [col for col in df.columns if "[Skor]" in col]

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📋 Menu Navigasi")

menu = st.sidebar.radio(
    "Pilih Halaman",
    [
        "🏠 Dashboard",
        "📊 Data Responden",
        "📈 Analisis Indikator",
        "💬 Masukan Mahasiswa"
    ]
)

# =========================
# FILTER ANGKATAN
# =========================
angkatan_col = None

for col in df.columns:
    if "Angkatan" in col:
        angkatan_col = col
        break

if angkatan_col:

    daftar_angkatan = ["Semua"] + sorted(
        df[angkatan_col].dropna().astype(str).unique().tolist()
    )

    pilih_angkatan = st.sidebar.selectbox(
        "Filter Angkatan",
        daftar_angkatan
    )

    if pilih_angkatan != "Semua":
        df = df[df[angkatan_col].astype(str) == pilih_angkatan]

# =========================
# KPI
# =========================
total_responden = len(df)

rata_skor = round(
    df[score_cols].mean().mean(),
    2
)

skor_tertinggi = int(
    df[score_cols].max().max()
)

indeks_kepuasan = round(
    (rata_skor / 5) * 100,
    1
)

# =========================
# DASHBOARD
# =========================
if menu == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">🎓 Dashboard Kepuasan Mahasiswa</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Jumlah Responden",
        total_responden
    )

    col2.metric(
        "Rata-rata Skor",
        rata_skor
    )

    col3.metric(
        "Indeks Kepuasan (%)",
        indeks_kepuasan
    )

    col4.metric(
        "Skor Tertinggi",
        skor_tertinggi
    )

    st.markdown("---")

    # =========================
    # RATA-RATA PER INDIKATOR
    # =========================
    rata_indikator = (
        df[score_cols]
        .mean()
        .sort_values(ascending=False)
    )

    fig_bar = px.bar(
        x=rata_indikator.values,
        y=[
            i.replace("[Skor]", "")
            for i in rata_indikator.index
        ],
        orientation="h",
        title="Rata-rata Kepuasan per Indikator"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

    # =========================
    # PIE CHART
    # =========================
    fig_pie = go.Figure(
        data=[
            go.Pie(
                labels=[
                    i.replace("[Skor]", "")
                    for i in rata_indikator.index
                ],
                values=rata_indikator.values,
                hole=0.45
            )
        ]
    )

    fig_pie.update_layout(
        title="Distribusi Kepuasan"
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

# =========================
# DATA RESPONDEN
# =========================
elif menu == "📊 Data Responden":

    st.subheader("📊 Data Responden")

    st.dataframe(
        df,
        use_container_width=True
    )

# =========================
# ANALISIS INDIKATOR
# =========================
elif menu == "📈 Analisis Indikator":

    st.subheader("📈 Analisis Detail Indikator")

    indikator = st.selectbox(
        "Pilih Indikator",
        score_cols
    )

    distribusi = (
        df[indikator]
        .value_counts()
        .sort_index()
    )

    fig = px.bar(
        x=distribusi.index.astype(str),
        y=distribusi.values,
        labels={
            "x": "Skor",
            "y": "Jumlah"
        },
        title=indikator
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.metric(
        "Rata-rata Indikator",
        round(df[indikator].mean(), 2)
    )

# =========================
# MASUKAN MAHASISWA
# =========================
elif menu == "💬 Masukan Mahasiswa":

    st.subheader("💬 Masukan dan Saran Mahasiswa")

    masukan_cols = [
        c for c in df.columns
        if "[Masukan]" in c
    ]

    if len(masukan_cols) == 0:

        st.warning(
            "Tidak ditemukan kolom [Masukan] pada data."
        )

    else:

        for col in masukan_cols:

            st.markdown(
                f"### {col.replace('[Masukan]', '')}"
            )

            data_masukan = (
                df[col]
                .dropna()
                .astype(str)
            )

            data_masukan = data_masukan[
                data_masukan.str.strip() != ""
            ]

            for teks in data_masukan:

                st.info(teks)
