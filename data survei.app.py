import streamlit as st
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard Auto Detect UMAHA",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Survei (Auto Detect Kolom)")

# =========================
# UPLOAD FILE
# =========================
st.sidebar.header("📁 Upload Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV / Excel",
    type=["csv", "xlsx"]
)

# =========================
# LOAD DATA
# =========================
def load_data(file):
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        return df
    except:
        return None

if uploaded_file:
    data = load_data(uploaded_file)
    if data is None:
        st.error("File tidak bisa dibaca")
        st.stop()
else:
    # default fallback
    data = pd.DataFrame({
        "Nama": ["A", "B", "C"],
        "Nilai": [80, 90, 85],
        "Kelas": ["TI-1", "TI-1", "TI-2"]
    })
    st.info("Menggunakan data default")

# =========================
# CLEANING KOLOM
# =========================
data.columns = data.columns.str.strip()

st.write("📌 Kolom terdeteksi:", list(data.columns))

# =========================
# AUTO-DETECT KOLOM
# =========================
def detect_column(possible_names, df_columns):
    """
    Cari kolom berdasarkan kemungkinan nama
    """
    for name in possible_names:
        for col in df_columns:
            if name.lower() in col.lower():
                return col
    return None

# detect kolom penting
col_nilai = detect_column(["nilai", "score", "skor", "value"], data.columns)
col_nama = detect_column(["nama", "name", "student", "mahasiswa"], data.columns)
col_kelas = detect_column(["kelas", "class", "group"], data.columns)

# =========================
# FILTER SIDEBAR
# =========================
st.sidebar.header("🔎 Filter")

filtered = data.copy()

if col_kelas:
    kelas_list = ["Semua"] + list(filtered[col_kelas].dropna().unique())
    kelas_pilih = st.sidebar.selectbox("Filter Kelas", kelas_list)

    if kelas_pilih != "Semua":
        filtered = filtered[filtered[col_kelas] == kelas_pilih]

# =========================
# TAMPIL DATA
# =========================
st.subheader("📋 Data Hasil")

st.dataframe(filtered, use_container_width=True)

# =========================
# STATISTIK AMAN
# =========================
st.subheader("📊 Statistik")

col1, col2, col3 = st.columns(3)

col1.metric("Jumlah Data", len(filtered))

# aman tanpa error
if col_nilai:
    col2.metric("Rata-rata", round(filtered[col_nilai].mean(), 2))
    col3.metric("Maksimum", filtered[col_nilai].max())
else:
    col2.metric("Rata-rata", "Tidak ada kolom nilai")
    col3.metric("Maksimum", "Tidak ada kolom nilai")

# =========================
# GRAFIK
# =========================
st.subheader("📊 Visualisasi")

if col_nilai and col_nama:
    chart_data = filtered[[col_nama, col_nilai]].dropna()
    chart_data = chart_data.set_index(col_nama)

    st.bar_chart(chart_data[col_nilai])
    st.line_chart(chart_data[col_nilai])
else:
    st.warning("Kolom nama/nilai tidak terdeteksi untuk grafik")

# =========================
# PIE CHART (AUTO)
# =========================
st.subheader("🥧 Distribusi Data")

if col_kelas:
    pie = filtered[col_kelas].value_counts().reset_index()
    pie.columns = ["Kategori", "Jumlah"]

    st.bar_chart(pie.set_index("Kategori"))
else:
    st.info("Tidak ada kolom kategori untuk pie chart")

# =========================
# EXPORT DATA
# =========================
st.subheader("⬇ Export Laporan")

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="laporan_dashboard.csv",
    mime="text/csv"
)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("© Dashboard Auto Detect UMAHA")
