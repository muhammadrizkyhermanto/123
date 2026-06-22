import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard Survei Mahasiswa umaha",
    page_icon="📊",
    layout="wide"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>
.main{
    padding-top:20px;
}
.kpi{
    background-color:#f0f2f6;
    padding:20px;
    border-radius:15px;
    text-align:center;
}
h1{
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("📊 Dashboard Survei Mahasiswa")
st.caption("Analisis Data Kepuasan Mahasiswa")

# =========================
# UPLOAD FILE
# =========================
file = st.file_uploader(
    "Upload File CSV",
    type=["csv"]
)

if file:

    try:
        df = pd.read_csv(file)

        # Hapus kolom kosong
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

        st.success("Data berhasil dimuat")

        # =========================
        # KPI
        # =========================
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Jumlah Responden",
                len(df)
            )

        with col2:
            st.metric(
                "Jumlah Kolom",
                len(df.columns)
            )

        with col3:
            st.metric(
                "Data Kosong",
                int(df.isna().sum().sum())
            )

        st.divider()

        # =========================
        # FILTER
        # =========================
        st.subheader("🔍 Filter Data")

        kolom_filter = st.selectbox(
            "Pilih Kolom",
            df.columns
        )

        st.divider()

        # =========================
        # DISTRIBUSI DATA
        # =========================
        st.subheader("📈 Distribusi Data")

        distribusi = (
            df[kolom_filter]
            .astype(str)
            .value_counts()
            .reset_index()
        )

        distribusi.columns = [
            "Kategori",
            "Jumlah"
        ]

        col1, col2 = st.columns([2,1])

        with col1:
            st.bar_chart(
                distribusi.set_index("Kategori")
            )

        with col2:
            st.dataframe(
                distribusi,
                use_container_width=True
            )

        st.divider()

        # =========================
        # DATA RESPONDEN
        # =========================
        st.subheader("📋 Data Responden")

        st.dataframe(
            df,
            use_container_width=True,
            height=500
        )

        st.divider()

        # =========================
        # SARAN & MASUKAN
        # =========================
        for col in df.columns:

            nama = str(col).lower()

            if "saran" in nama or "masukan" in nama:

                st.subheader("💡 Saran dan Masukan")

                data_saran = df[col].dropna()

                for i, isi in enumerate(data_saran, start=1):
                    st.write(f"**{i}.** {isi}")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

else:
    st.info("Silakan upload file CSV terlebih dahulu.")

    st.bar_chart(
        distribusi.set_index("Kategori")
    )
