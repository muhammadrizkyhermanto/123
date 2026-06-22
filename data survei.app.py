import streamlit as st
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard Survei UMAHA",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Survei Mahasiswa UMAHA")

# =========================
# UPLOAD FILE (CSV / EXCEL)
# =========================
st.sidebar.header("📁 Upload Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV / Excel",
    type=["csv", "xlsx"]
)

# =========================
# DATA DEFAULT
# =========================
def load_default():
    return pd.DataFrame({
        "Nama": ["A", "B", "C", "D", "E"],
        "Nilai": [80, 90, 85, 70, 95],
        "Kelas": ["TI-1", "TI-1", "TI-2", "TI-2", "TI-1"],
        "Jenis_Kelamin": ["L", "P", "L", "P", "L"]
    })

# =========================
# LOAD DATA
# =========================
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        st.success("File berhasil diupload")
    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
        data = load_default()
else:
    data = load_default()
    st.info("Menggunakan data default")

# =========================
# SIDEBAR FILTER MULTI KOLOM
# =========================
st.sidebar.header("🔎 Filter Data")

filtered_data = data.copy()

# Filter Kelas
if "Kelas" in data.columns:
    kelas = st.sidebar.selectbox(
        "Filter Kelas",
        ["Semua"] + list(data["Kelas"].unique())
    )
    if kelas != "Semua":
        filtered_data = filtered_data[filtered_data["Kelas"] == kelas]

# Filter Jenis Kelamin
if "Jenis_Kelamin" in data.columns:
    jk = st.sidebar.selectbox(
        "Filter Jenis Kelamin",
        ["Semua"] + list(data["Jenis_Kelamin"].unique())
    )
    if jk != "Semua":
        filtered_data = filtered_data[filtered_data["Jenis_Kelamin"] == jk]

# =========================
# TAMPILKAN DATA
# =========================
st.subheader("📋 Data Hasil Filter")
st.dataframe(filtered_data, use_container_width=True)

# =========================
# STATISTIK
# =========================
st.subheader("📊 Statistik")

col1, col2, col3 = st.columns(3)

col1.metric("Jumlah Data", len(filtered_data))
col2.metric("Rata-rata Nilai", round(filtered_data["Nilai"].mean(), 2))
col3.metric("Nilai Tertinggi", filtered_data["Nilai"].max())

# =========================
# BAR CHART
# =========================
st.subheader("📊 Bar Chart Nilai")

chart_data = filtered_data.set_index("Nama")
st.bar_chart(chart_data["Nilai"])

# =========================
# LINE CHART
# =========================
st.subheader("📈 Line Chart Nilai")
st.line_chart(chart_data["Nilai"])

# =========================
# PIE CHART (KOMPOSISI KELAS)
# =========================
st.subheader("🥧 Pie Chart Distribusi Kelas")

if "Kelas" in filtered_data.columns:
    pie_data = filtered_data["Kelas"].value_counts().reset_index()
    pie_data.columns = ["Kelas", "Jumlah"]

    st.bar_chart(pie_data.set_index("Kelas"))  # streamlit tidak punya pie native stabil
else:
    st.info("Kolom Kelas tidak tersedia")

# =========================
# EXPORT LAPORAN
# =========================
st.subheader("⬇ Export Data")

csv = filtered_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV Hasil Filter",
    data=csv,
    file_name="laporan_survei.csv",
    mime="text/csv"
)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("© 2026 Dashboard UMAHA")
