import streamlit as st
import pandas as pd

# ==========================
# KONFIGURASI HALAMAN
# ==========================
st.set_page_config(
    page_title="Dashboard Survei Mahasiswa",
    page_icon="📊",
    layout="wide"
)

# ==========================
# HEADER
# ==========================
st.markdown("""
<div style='text-align:center;padding:20px'>
    <h1>📊 Dashboard Survei Mahasiswa</h1>
    <p>Analisis Data Kepuasan Mahasiswa</p>
</div>
""", unsafe_allow_html=True)

# ==========================
# UPLOAD FILE
# ==========================
file = st.file_uploader(
    "Upload File CSV",
    type=["csv"]
)

if file is not None:

    try:

        df = pd.read_csv(file)

        st.success("✅ Data berhasil dimuat")

        # ==========================
        # METRIK
        # ==========================
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Jumlah Responden",
            len(df)
        )

        col2.metric(
            "Jumlah Kolom",
            len(df.columns)
        )

        col3.metric(
            "Data Kosong",
            int(df.isna().sum().sum())
        )

        st.divider()

        # ==========================
        # DATA MENTAH
        # ==========================
        st.subheader("📋 Data Responden")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.divider()

        # ==========================
        # ANALISIS
        # ==========================
        st.subheader("📈 Analisis Data")

        kolom = st.selectbox(
            "Pilih Kolom",
            df.columns
        )

        hasil = (
            df[kolom]
            .astype(str)
            .value_counts()
            .reset_index()
        )

        hasil.columns = [
            "Kategori",
            "Jumlah"
        ]

        st.write("Distribusi Data")

        st.dataframe(
            hasil,
            use_container_width=True
        )

        st.bar_chart(
            hasil.set_index("Kategori")
        )

        st.divider()

        # ==========================
        # SARAN DAN MASUKAN
        # ==========================
        for c in df.columns:

            nama = str(c).lower()

            if "saran" in nama or "masukan" in nama:

                st.subheader("💡 Saran dan Masukan")

                data_saran = df[c].dropna()

                for i, isi in enumerate(data_saran, start=1):
                    st.write(f"{i}. {isi}")

    except Exception as e:

        st.error(f"Error membaca file: {e}")

else:

    st.info("Silakan upload file CSV terlebih dahulu.")

    st.bar_chart(
        distribusi.set_index("Kategori")
    )
