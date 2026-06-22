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

st.title("📊 Dashboard Survei Mahasiswa (Auto Detect + Anti Error)")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)

    # bersihkan nama kolom
    df.columns = df.columns.str.strip()

    # hapus unnamed column
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    return df


uploaded_file = st.file_uploader("Upload file CSV kamu", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)
    st.success("Data berhasil dimuat!")

    # =========================
    # DETEKSI KOLOM AMAN
    # =========================
    def find_col(keywords):
        for col in df.columns:
            if any(k.lower() in col.lower() for k in keywords):
                return col
        return None

    col_total = find_col(["total skor", "total", "skor total"])
    col_gender = find_col(["jenis kelamin", "gender", "kelamin"])
    col_angkatan = find_col(["angkatan"])

    skor_cols = [col for col in df.columns if "skor" in col.lower() and col != col_total]

    # ubah numeric aman
    for col in skor_cols + ([col_total] if col_total else []):
        if col:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # =========================
    # KPI
    # =========================
    st.subheader("📌 KPI Utama")

    col1, col2, col3 = st.columns(3)

    with col1:
        avg_total = df[col_total].mean() if col_total else 0
        st.metric("Rata-rata Total Skor", f"{avg_total:.2f}")

    with col2:
        st.metric("Jumlah Responden", len(df))

    with col3:
        avg_all = df[skor_cols].mean().mean() if skor_cols else 0
        st.metric("Rata-rata Semua Skor", f"{avg_all:.2f}")

    # =========================
    # ANGKATAN
    # =========================
    st.subheader("📊 Distribusi Angkatan")

    if col_angkatan:
        fig = px.histogram(df, x=col_angkatan, color=col_angkatan)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Kolom Angkatan tidak ditemukan")

    # =========================
    # GENDER
    # =========================
    st.subheader("👥 Gender Responden")

    if col_gender:
        gender = df[col_gender].value_counts().reset_index()
        gender.columns = ["Kategori", "Jumlah"]

        fig = px.pie(gender, names="Kategori", values="Jumlah")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Kolom Gender tidak ditemukan")

    # =========================
    # RATA-RATA INDIKATOR
    # =========================
    st.subheader("📈 Rata-rata Skor per Indikator")

    if skor_cols:
        avg_scores = df[skor_cols].mean().sort_values()
        avg_df = avg_scores.reset_index()
        avg_df.columns = ["Indikator", "Rata-rata"]

        fig = px.bar(avg_df, x="Rata-rata", y="Indikator", orientation="h")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Tidak ada kolom skor ditemukan")

    # =========================
    # DATA
    # =========================
    st.subheader("📄 Data Mentah")
    st.dataframe(df)

else:
    st.info("Silakan upload file CSV terlebih dahulu")
