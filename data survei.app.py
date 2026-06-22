import streamlit as st
import pandas as pd

st.title("Dashboard Data Survei")

uploaded_file = st.file_uploader(
    "Upload File CSV",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("Data berhasil dimuat")

    st.subheader("Data Responden")
    st.dataframe(df)

    st.subheader("Statistik")

    st.write("Jumlah Responden :", len(df))
    st.write("Jumlah Kolom :", len(df.columns))

    kolom = st.selectbox(
        "Pilih Kolom",
        df.columns
    )

    st.subheader("Distribusi Data")

    distribusi = (
        df[kolom]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    distribusi.columns = ["Kategori", "Jumlah"]

    st.dataframe(distribusi)

    st.bar_chart(
        distribusi.set_index("Kategori")
    )
