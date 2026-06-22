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
# JUDUL DASHBOARD
# =========================
st.title("📊 Dashboard Survei Mahasiswa UMAHA")
st.markdown("Dashboard ini digunakan untuk menampilkan hasil survei mahasiswa secara interaktif.")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("📁 Pengaturan Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload file CSV kamu",
    type=["csv"]
)

# =========================
# DATA DEFAULT (JIKA TIDAK UPLOAD)
# =========================
def load_default_data():
    data = pd.DataFrame({
        "Nama": ["A", "B", "C", "D", "E"],
        "Nilai": [80, 90, 85, 70, 95],
        "Kelas": ["TI-1", "TI-1", "TI-2", "TI-2", "TI-1"]
    })
    return data

# =========================
# LOAD DATA
# =========================
try:
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.success("File berhasil diupload!")
    else:
        data = load_default_data()
        st.info("Menggunakan data default karena belum ada file upload.")

except Exception as e:
    st.error(f"Gagal membaca data: {e}")
    data = load_default_data()

# =========================
# TAMPILKAN DATA MENTAH
# =========================
st.subheader("📋 Data Mentah")
st.dataframe(data, use_container_width=True)

# =========================
# FILTER DI SIDEBAR
# =========================
if "Kelas" in data.columns:
    kelas_pilih = st.sidebar.selectbox(
        "Filter Kelas",
        options=["Semua"] + list(data["Kelas"].unique())
    )

    if kelas_pilih != "Semua":
        data = data[data["Kelas"] == kelas_pilih]

# =========================
# STATISTIK DASAR
# =========================
st.subheader("📊 Statistik Ringkasan")

try:
    col1, col2, col3 = st.columns(3)

    col1.metric("Jumlah Data", len(data))
    col2.metric("Rata-rata Nilai", round(data["Nilai"].mean(), 2))
    col3.metric("Nilai Tertinggi", data["Nilai"].max())

except Exception as e:
    st.warning(f"Statistik tidak dapat ditampilkan: {e}")

# =========================
# GRAFIK BAR CHART
# =========================
st.subheader("📊 Grafik Nilai Mahasiswa (Bar Chart)")

try:
    chart_data = data.copy()
    chart_data = chart_data.set_index("Nama")

    st.bar_chart(chart_data["Nilai"])

except Exception as e:
    st.warning(f"Gagal membuat bar chart: {e}")

# =========================
# GRAFIK LINE CHART
# =========================
st.subheader("📈 Grafik Tren Nilai (Line Chart)")

try:
    st.line_chart(chart_data["Nilai"])

except Exception as e:
    st.warning(f"Gagal membuat line chart: {e}")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("© 2026 Dashboard Survei Mahasiswa UMAHA")
    st.warning(f"Tidak dapat membuat grafik: {e}")
except Exception as e:
    st.warning(f"Tidak dapat membuat grafik: {e}")
