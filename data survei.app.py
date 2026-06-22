import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Survei Mahasiswa UMAHA",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Survei Mahasiswa")

# Contoh data
data = pd.DataFrame({
    "Nama": ["A", "B", "C"],
    "Nilai": [80, 90, 85]
})

st.dataframe(data)

# aman pakai try-except
try:
    st.bar_chart(data.set_index("Nama"))
except Exception as e:
    st.warning(f"Tidak dapat membuat grafik: {e}")
except Exception as e:
    st.warning(f"Tidak dapat membuat grafik: {e}")
