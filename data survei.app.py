import streamlit as st
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Professional Dashboard KPI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Survei Kepuasan Mahasiswa terhadap kampus umaha")

# =========================
# UPLOAD FILE
# =========================
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()

        st.success("Dataset berhasil dimuat!")

        # =========================
        # SIDEBAR FILTER
        # =========================
        st.sidebar.header("⚙️ Filter Data")

        # filter categorical columns
        cat_cols = df.select_dtypes(include="object").columns.tolist()

        filtered_df = df.copy()

        for col in cat_cols:
            unique_vals = df[col].dropna().unique().tolist()
            if len(unique_vals) > 1 and len(unique_vals) < 50:
                selected_vals = st.sidebar.multiselect(
                    f"Filter {col}",
                    unique_vals,
                    default=unique_vals
                )
                filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]

        # =========================
        # PREVIEW
        # =========================
        st.subheader("📄 Data Preview")
        st.dataframe(filtered_df, use_container_width=True)

        # =========================
        # NUMERIC & KPI
        # =========================
        numeric_cols = filtered_df.select_dtypes(include="number").columns.tolist()

        st.subheader("📊 KPI Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Data", len(filtered_df))

        if len(numeric_cols) > 0:
            kpi_col = st.selectbox("Pilih kolom KPI", numeric_cols)

            with col2:
                st.metric("Rata-rata", round(filtered_df[kpi_col].mean(), 2))

            with col3:
                st.metric("Maksimum", filtered_df[kpi_col].max())

            with col4:
                st.metric("Minimum", filtered_df[kpi_col].min())

        else:
            with col2:
                st.metric("Rata-rata", "N/A")
            with col3:
                st.metric("Max", "N/A")
            with col4:
                st.metric("Min", "N/A")

        # =========================
        # CHART SECTION
        # =========================
        st.subheader("📈 Visual Analytics")

        chart_col = st.selectbox("Pilih kolom untuk visualisasi", filtered_df.columns)

        chart_type = st.radio(
            "Jenis Chart",
            ["Bar", "Line", "Area", "Pie"]
        )

        colA, colB = st.columns(2)

        with colA:
            # numeric chart
            if pd.api.types.is_numeric_dtype(filtered_df[chart_col]):
                if chart_type == "Bar":
                    st.bar_chart(filtered_df[chart_col])
                elif chart_type == "Line":
                    st.line_chart(filtered_df[chart_col])
                elif chart_type == "Area":
                    st.area_chart(filtered_df[chart_col])
                else:
                    st.warning("Pie chart cocok untuk data kategori")
            else:
                data_counts = filtered_df[chart_col].value_counts()

                if chart_type == "Pie":
                    st.write(data_counts)
                    st.info("Pie chart simulated via bar (Streamlit limitation)")
                    st.bar_chart(data_counts)
                else:
                    st.bar_chart(data_counts)

        with colB:
            st.write("📌 Insight Otomatis")

            if len(numeric_cols) > 0:
                top_col = numeric_cols[0]

                avg = filtered_df[top_col].mean()
                mx = filtered_df[top_col].max()
                mn = filtered_df[top_col].min()

                st.info(f"""
                - Rata-rata **{top_col}**: {round(avg,2)}
                - Nilai tertinggi: {mx}
                - Nilai terendah: {mn}
                - Total data setelah filter: {len(filtered_df)}
                """)
            else:
                st.warning("Tidak ada data numerik untuk insight")

        # =========================
        # DETAIL STATISTICS
        # =========================
        st.subheader("📌 Statistik Lengkap")

        if len(numeric_cols) > 0:
            st.dataframe(filtered_df[numeric_cols].describe(), use_container_width=True)
        else:
            st.info("Tidak ada kolom numerik")

    except Exception as e:
        st.error("Terjadi error pada sistem")
        st.exception(e)

else:
    st.info("Silakan upload file CSV untuk mulai analisis")
