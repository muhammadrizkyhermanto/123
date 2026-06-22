import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =====================================
# KONFIGURASI HALAMAN
# =====================================
st.set_page_config(
    page_title="Dashboard Survei Mahasiswa",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Survei Kepuasan Mahasiswa")

# =====================================
# UPLOAD FILE CSV
# =====================================
uploaded_file = st.file_uploader(
    "Upload File CSV",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)

        st.success("Data berhasil dimuat!")

        # Hapus kolom kosong jika ada
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

        # =====================================
        # DATA MENTAH
        # =====================================
        st.subheader("Data Responden")
        st.dataframe(df)

        # =====================================
        # INFORMASI UMUM
        # =====================================
        st.subheader("Ringkasan Data")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Jumlah Responden", len(df))

        with col2:
            st.metric("Jumlah Kolom", len(df.columns))

        with col3:
            st.metric("Jumlah Data Kosong", df.isnull().sum().sum())

        # =====================================
        # PILIH KOLOM UNTUK ANALISIS
        # =====================================
        st.subheader("Analisis Data")

        kolom = st.selectbox(
            "Pilih Kolom",
            df.columns
        )

        # =====================================
        # VALUE COUNTS
        # =====================================
        data_chart = (
            df[kolom]
            .astype(str)
            .value_counts()
        )

        st.write("Distribusi Data")

        fig, ax = plt.subplots(figsize=(8, 4))

        data_chart.plot(
            kind="bar",
            ax=ax
        )

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

        # =====================================
        # TABEL DISTRIBUSI
        # =====================================
        st.subheader("Tabel Distribusi")

        distribusi = pd.DataFrame({
            "Kategori": data_chart.index,
            "Jumlah": data_chart.values
        })

        st.dataframe(distribusi)

        # =====================================
        # SARAN DAN MASUKAN
        # =====================================
        for col in df.columns:

            if "saran" in col.lower() or "masukan" in col.lower():

                st.subheader("Saran dan Masukan")

                saran = df[col].dropna()

                for i, isi in enumerate(saran, start=1):
                    st.write(f"{i}. {isi}")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

else:
    st.info("Silakan upload file CSV terlebih dahulu.")
