import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard Kepuasan Mahasiswa",
    page_icon="📊",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("tugas pak gusti.csv")

    # hapus kolom kosong
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    return df

df = load_data()

# =========================
# HEADER
# =========================
st.title("🎓 Dashboard Kepuasan Mahasiswa")
st.markdown("---")

# =========================
# KPI
# =========================
col1, col2, col3 = st.columns(3)

jumlah_responden = len(df)

if "Total skor" in df.columns:
    avg_skor = pd.to_numeric(
        df["Total skor"],
        errors="coerce"
    ).mean()
else:
    avg_skor = 0

if "Jenis kelamin" in df.columns:
    gender = df["Jenis kelamin"].nunique()
else:
    gender = 0

with col1:
    st.metric(
        "Jumlah Responden",
        jumlah_responden
    )

with col2:
    st.metric(
        "Rata-rata Skor",
        f"{avg_skor:.2f}"
    )

with col3:
    st.metric(
        "Kategori Gender",
        gender
    )

st.markdown("---")

# =========================
# FILTER
# =========================
if "Angkatan " in df.columns:

    angkatan_list = sorted(
        df["Angkatan "]
        .dropna()
        .astype(str)
        .unique()
    )

    selected = st.selectbox(
        "Pilih Angkatan",
        ["Semua"] + angkatan_list
    )

    if selected != "Semua":
        df = df[
            df["Angkatan "].astype(str) == selected
        ]

# =========================
# DATA TABLE
# =========================
st.subheader("📋 Data Responden")

st.dataframe(
    df,
    use_container_width=True
)

# =========================
# ANALISIS SKOR
# =========================
st.subheader("📈 Statistik Skor")

if "Total skor" in df.columns:

    skor = pd.to_numeric(
        df["Total skor"],
        errors="coerce"
    )

    st.write(
        skor.describe()
    )

# =========================
# DISTRIBUSI GENDER
# =========================
if "Jenis kelamin" in df.columns:

    st.subheader("👥 Distribusi Jenis Kelamin")

    gender_count = (
        df["Jenis kelamin"]
        .value_counts()
    )

    st.bar_chart(gender_count)

# =========================
# ANALISIS ANGKATAN
# =========================
if "Angkatan " in df.columns:

    st.subheader("🎓 Distribusi Angkatan")

    angkatan_count = (
        df["Angkatan "]
        .astype(str)
        .value_counts()
    )

    st.bar_chart(angkatan_count)

# =========================
# KEPUASAN FASILITAS
# =========================
target = "Tingkat kepuasan secara keseluruhan terhadap fasilitas kampus"

if target in df.columns:

    st.subheader("🏫 Kepuasan Fasilitas Kampus")

    kepuasan = (
        df[target]
        .astype(str)
        .value_counts()
    )

    st.bar_chart(kepuasan)

# =========================
# DOWNLOAD DATA
# =========================
st.markdown("---")

csv = df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="hasil_survei.csv",
    mime="text/csv"
)
