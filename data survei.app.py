# =========================
# DISTRIBUSI DATA
# =========================
st.subheader("📈 Distribusi Data")

try:

    distribusi = (
        df[kolom_filter]
        .fillna("Kosong")
        .astype(str)
        .value_counts()
        .reset_index(name="Jumlah")
    )

    distribusi.columns = ["Kategori", "Jumlah"]

    col1, col2 = st.columns([2,1])

    with col1:
        st.bar_chart(
            distribusi.set_index("Kategori")["Jumlah"]
        )

    with col2:
        st.dataframe(
            distribusi,
            use_container_width=True
        )

except Exception as e:
    st.warning(f"Tidak dapat membuat grafik: {e}")
    )
