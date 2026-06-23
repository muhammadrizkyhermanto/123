import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Survey Kepuasan Mahasiswa UMAHA",
    layout="wide"
)

# ================= CSS =================
st.markdown("""
<style>

.main-title{
    color:#1f4268;
    font-size:40px;
    font-weight:bold;
}

.card{
    background:#245785;
    padding:20px;
    border-radius:12px;
    text-align:center;
    color:white;
}

.sidebar-title{
    font-size:28px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
st.sidebar.markdown(
    "<div class='sidebar-title'>📋 Menu Navigasi</div>",
    unsafe_allow_html=True
)

menu = st.sidebar.radio(
    "Pilih Halaman",
    [
        "🏠 Home",
        "📊 Data Survey",
        "📈 Analisis",
        "⚠️ FMEA"
    ]
)

# ================= DATA DUMMY =================
responden = 150
kepuasan = 92.4
rata_skor = 4.62
saran = 87

# ================= HOME =================
if menu == "🏠 Home":

    st.markdown(
        "<div class='main-title'>🏫 Dashboard Survey Kepuasan Mahasiswa UMAHA</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class='card'>
        <h1>{responden}</h1>
        Total Responden
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='card'>
        <h1>{kepuasan}%</h1>
        Tingkat Kepuasan
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class='card'>
        <h1>{rata_skor}</h1>
        Rata-rata Skor
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class='card'>
        <h1>{saran}</h1>
        Jumlah Saran
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    st.subheader("📈 Tren Kepuasan Mahasiswa")

    chart_data = pd.DataFrame({
        "Bulan":[
            "Jan","Feb","Mar","Apr",
            "Mei","Jun","Jul","Agu",
            "Sep","Okt","Nov","Des"
        ],
        "Skor":[
            4.1,4.2,4.3,4.4,
            4.5,4.5,4.6,4.7,
            4.6,4.7,4.8,4.8
        ]
    })

    st.line_chart(
        chart_data.set_index("Bulan")
    )

# ================= DATA =================
elif menu == "📊 Data Survey":

    st.subheader("Data Survey")

    df = pd.DataFrame({
        "Program Studi":[
            "Teknik Industri",
            "Informatika",
            "Manajemen",
            "Akuntansi"
        ],
        "Skor":[4.6,4.7,4.5,4.4]
    })

    st.dataframe(df, use_container_width=True)

# ================= ANALISIS =================
elif menu == "📈 Analisis":

    st.subheader("Analisis Kepuasan")

    data = pd.DataFrame({
        "Aspek":[
            "Pelayanan",
            "Fasilitas",
            "Akademik",
            "Administrasi"
        ],
        "Nilai":[92,88,95,90]
    })

    st.bar_chart(
        data.set_index("Aspek")
    )

# ================= FMEA =================
elif menu == "⚠️ FMEA":

    st.subheader("Analisis Risiko")

    severity = st.slider("Severity",1,10,5)
    occurrence = st.slider("Occurrence",1,10,5)
    detection = st.slider("Detection",1,10,5)

    rpn = severity*occurrence*detection

    st.metric(
        "Risk Priority Number",
        rpn
    )
