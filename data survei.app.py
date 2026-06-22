import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard Survei Mahasiswa",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Survei Mahasiswa (Auto Detect + KPI Profesional)")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    
    # hapus kolom kosong/unnamed
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    
    # rapikan nama kolom
    df.columns = df.columns.str.strip()
    
    return df


uploaded_file = st.file_uploader("Upload file CSV kamu", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)

    st.success("Data berhasil dimuat!")

    # =========================
    # DETEKSI KOLOM OTOMATIS
    # =========================
    skor_cols = [col for col in df.columns if "[Skor]" in col]
    
    # pastikan numeric
    for col in skor_cols + ["Total skor"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # =========================
    # KPI SECTION
    # =========================
    st.subheader("📌 KPI Utama")

    col1, col2, col3 = st.columns(3)

    with col1:
        avg_total = df["Total skor"].mean() if "Total skor" in df.columns else 0
        st.metric("Rata-rata Total Skor", f"{avg_total:.2f}")

    with col2:
        jumlah = len(df)
        st.metric("Jumlah Responden", jumlah)

    with col3:
        avg_all = df[skor_cols].mean().mean() if skor_cols else 0
        st.metric("Rata-rata Semua Skor", f"{avg_all:.2f}")

    # =========================
    # DISTRIBUSI ANGKATAN
    # =========================
    st.subheader("📊 Distribusi Angkatan")

    if "Angkatan " in df.columns:
        fig = px.histogram(df, x="Angkatan ", color="Angkatan ",
                           title="Distribusi Responden Berdasarkan Angkatan")
        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # JENIS KELAMIN
    # =========================
    st.subheader("👥 Gender Responden")

    if "Jenis kelamin" in df.columns:
        gender = df["Jenis kelamin"].value_counts().reset_index()
        gender.columns = ["Jenis Kelamin", "Jumlah"]

        fig = px.pie(gender, names="Jenis Kelamin", values="Jumlah",
                     title="Distribusi Jenis Kelamin")
        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # RATA-RATA PER INDIKATOR
    # =========================
    st.subheader("📈 Rata-rata Skor Tiap Indikator")

    if skor_cols:
        avg_scores = df[skor_cols].mean().sort_values()
        avg_df = avg_scores.reset_index()
        avg_df.columns = ["Indikator", "Rata-rata Skor"]

        fig = px.bar(avg_df, x="Rata-rata Skor", y="Indikator",
                     orientation="h",
                     title="Rata-rata Penilaian per Aspek")
        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # RAW DATA
    # =========================
    st.subheader("📄 Data Mentah")
    st.dataframe(df)

else:
    st.info("Silakan upload file CSV untuk menampilkan dashboard.")
