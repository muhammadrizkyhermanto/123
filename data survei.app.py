import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Dashboard Kepuasan Mahasiswa",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Kepuasan Mahasiswa")
st.markdown("Analisis Survei Kepuasan Mahasiswa Teknik Industri")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("tugas pak gusti.csv")
    return df

df = load_data()

# Hapus kolom kosong
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# =========================
# SIDEBAR
# =========================
st.sidebar.header("Filter Data")

if "Angkatan " in df.columns:
    angkatan = st.sidebar.multiselect(
        "Pilih Angkatan",
        options=sorted(df["Angkatan "].dropna().unique()),
        default=sorted(df["Angkatan "].dropna().unique())
    )

    df = df[df["Angkatan "].isin(angkatan)]

# =========================
# METRIK
# =========================
st.subheader("Ringkasan Data")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Jumlah Responden", len(df))

with col2:
    if "Angkatan " in df.columns:
        st.metric(
            "Jumlah Angkatan",
            df["Angkatan "].nunique()
        )

with col3:
    if "Jenis kelamin" in df.columns:
        st.metric(
            "Jumlah Gender",
            df["Jenis kelamin"].nunique()
        )

# =========================
# DATA RESPONDEN
# =========================
st.subheader("Data Responden")

tampil = df[[
    "Cap waktu",
    "Angkatan ",
    "Jenis kelamin",
    "kondisi ruang kelas di kampus ",
    "kualitas akses internet (WIFI)",
    "kualitas  pengajaran dosen ",
    "Pelayanan administrasi (TU)",
    "Tingkat kepuasan secara keseluruhan terhadap fasilitas kampus"
]]

st.dataframe(tampil, use_container_width=True)

# =========================
# DISTRIBUSI ANGKATAN
# =========================
st.subheader("Distribusi Angkatan")

angkatan_chart = (
    df["Angkatan "]
    .value_counts()
    .reset_index()
)

angkatan_chart.columns = ["Angkatan", "Jumlah"]

fig = px.bar(
    angkatan_chart,
    x="Angkatan",
    y="Jumlah",
    text="Jumlah",
    title="Jumlah Responden per Angkatan"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# DISTRIBUSI GENDER
# =========================
st.subheader("Distribusi Jenis Kelamin")

gender_chart = (
    df["Jenis kelamin"]
    .value_counts()
    .reset_index()
)

gender_chart.columns = ["Jenis Kelamin", "Jumlah"]

fig2 = px.pie(
    gender_chart,
    names="Jenis Kelamin",
    values="Jumlah",
    title="Komposisi Jenis Kelamin"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# ANALISIS KEPUASAN
# =========================
st.subheader("Analisis Tingkat Kepuasan")

kolom_survei = [
    "kondisi ruang kelas di kampus ",
    "kualitas akses internet (WIFI)",
    "kualitas  pengajaran dosen ",
    "kemudahan menghubungi dosen diluar jam kuliah ",
    "kesesuaian materi dengan dunia kerja ",
    "Pelayanan administrasi (TU)",
    "Kemudahan akses informasi akademik ",
    "Tingkat kepuasan secara keseluruhan terhadap fasilitas kampus"
]

hasil = []

for kolom in kolom_survei:

    modus = df[kolom].mode()

    if len(modus) > 0:
        hasil.append({
            "Aspek": kolom,
            "Penilaian Terbanyak": modus[0]
        })

hasil_df = pd.DataFrame(hasil)

st.dataframe(
    hasil_df,
    use_container_width=True
)

# =========================
# GRAFIK SETIAP ASPEK
# =========================
st.subheader("Grafik Kepuasan per Aspek")

pilihan = st.selectbox(
    "Pilih Aspek",
    kolom_survei
)

grafik = (
    df[pilihan]
    .value_counts()
    .reset_index()
)

grafik.columns = ["Kategori", "Jumlah"]

fig3 = px.bar(
    grafik,
    x="Kategori",
    y="Jumlah",
    text="Jumlah",
    title=pilihan
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# SARAN MAHASISWA
# =========================
st.subheader("Saran dan Masukan Mahasiswa")

saran = df["saran atau masukan untuk kampus"].dropna()

for i, isi in enumerate(saran, start=1):
    st.write(f"**{i}.** {isi}")