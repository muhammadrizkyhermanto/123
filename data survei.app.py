import streamlit as st
import pandas as pd

# =========================
# CONFIG HALAMAN
# =========================
st.set_page_config(
    page_title="Dashboard Survei Mahasiswa UMAHA",
    page_icon="📊",
    layout="wide"
)

# =========================
# JUDUL
# =========================
st.title("📊 Dashboard Survei Mahasiswa UMAHA")
st.markdown("Dashboard untuk menampilkan data survei mahasiswa secara interaktif.")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("📁 Upload Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload file CSV",
    type=["csv"]
)

# =========================
# DATA DEFAULT
# =========================
def get_default_data():
    return pd.DataFrame({
        "Nama": ["A", "B", "C", "D", "E"],
        "Nilai": [80, 90, 85, 70, 95],
        "Kelas": ["TI-1", "TI-1", "TI-2", "TI-2", "TI-1"]
    })

# =========================
# LOAD DATA (AMAN)
# =========================
if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        st.success("File berhasil diupload")
    except Exception as e:
        st.error(f"File tidak bisa dibaca: {e}")
        data = get_default_data()
else:
    data = get_default_data()
    st.info("Menggunakan data default")

# =========================
# TAMPILKAN DATA
# =========================
st.subheader("📋 Data Mahasiswa")
st.dataframe(data, use_container_width=True)

# =========================
# FILTER KELAS
# =========================
if "Kelas" in data.columns:
    kelas = st.sidebar.selectbox(
        "Filter Kelas",
        ["Semua"] + list(data["Kelas"].unique())
    )

    if kelas != "Semua":
        data = data[data["Kelas"] == kelas]

# =========================
# STATISTIK
# =========================
st.subheader("📊 Statistik Data")

col1, col2, col3 = st.columns(3)

col1.metric("Jumlah Data", len(data))
col2.metric("Rata-rata Nilai", round(data["Nilai"].mean(), 2))
col3.metric("Nilai Tertinggi", data["Nilai"].max())

# =========================
# GRAFIK
# =========================
st.subheader("📊 Grafik Nilai Mahasiswa")

chart_data = data.set_index("Nama")

st.bar_chart(chart_data["Nilai"])
st.line_chart(chart_data["Nilai"])

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("© 2026 Dashboard UMAHA")
    st.warning(f"Tidak dapat membuat grafik: {e}")
