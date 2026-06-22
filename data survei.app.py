import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Survei",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Hasil Survei Mahasiswa")

# =========================
# LOAD FILE
# =========================
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.read_csv("/mnt/data/tugas pak gusti.csv")

# =========================
# CLEAN KOLOM
# =========================
data.columns = data.columns.str.strip()

st.write("📌 Kolom tersedia:", list(data.columns))

# =========================
# AMBIL KOLOM SESUAI FILE KAMU
# =========================
col_nama = "Nama "
col_skor = "Total skor"
col_kelas = "Angkatan "

# =========================
# FILTER
# =========================
st.sidebar.header("Filter")

filtered = data.copy()

if col_kelas in data.columns:
    pilihan = st.sidebar.selectbox(
        "Angkatan",
        ["Semua"] + list(data[col_kelas].dropna().unique())
    )

    if pilihan != "Semua":
        filtered = filtered[filtered[col_kelas] == pilihan]

# =========================
# STATISTIK
# =========================
st.subheader("Statistik")

col1, col2, col3 = st.columns(3)

col1.metric("Jumlah Responden", len(filtered))

if col_skor in filtered.columns:
    col2.metric("Rata-rata Skor", round(filtered[col_skor].mean(), 2))
    col3.metric("Skor Tertinggi", filtered[col_skor].max())
else:
    col2.metric("Rata-rata", "Tidak ada data")
    col3.metric("Max", "Tidak ada data")

# =========================
# GRAFIK
# =========================
st.subheader("Grafik Skor")

if col_nama in filtered.columns and col_skor in filtered.columns:
    chart = filtered[[col_nama, col_skor]].set_index(col_nama)
    st.bar_chart(chart[col_skor])
    st.line_chart(chart[col_skor])

# =========================
# DISTRIBUSI ANGKATAN
# =========================
st.subheader("Distribusi Angkatan")

if col_kelas in filtered.columns:
    dist = filtered[col_kelas].value_counts()
    st.bar_chart(dist)

# =========================
# DOWNLOAD
# =========================
csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Data",
    data=csv,
    file_name="hasil_survei.csv",
    mime="text/csv"
