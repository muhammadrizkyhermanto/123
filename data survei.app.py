import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Survei Mahasiswa UMAHA",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Survei Mahasiswa UMAHA")

file = st.file_uploader(
    "Upload File CSV",
    type=["csv"]
)

if file is not None:

    try:
        df = pd.read_csv(file)

        st.success("Data berhasil dimuat")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Jumlah Responden", len(df))

        with col2:
            st.metric("Jumlah Kolom", len(df.columns))

        with col3:
            st.metric("Data Kosong", int(df.isna().sum().sum()))

        st.subheader("Data Responden")
        st.dataframe(df, use_container_width=True)

        kolom_filter = st.selectbox(
            "Pilih Kolom Analisis",
            df.columns
        )

        distribusi = (
            df[kolom_filter]
            .astype(str)
            .value_counts()
            .reset_index(name="Jumlah")
        )

        distribusi.columns = ["Kategori", "Jumlah"]

        st.subheader("Distribusi Data")

        st.bar_chart(
            distribusi.set_index("Kategori")["Jumlah"]
        )

        st.dataframe(
            distribusi,
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("Silakan upload file CSV terlebih dahulu.")
except Exception as e:
    st.warning(f"Tidak dapat membuat grafik: {e}")
    )
