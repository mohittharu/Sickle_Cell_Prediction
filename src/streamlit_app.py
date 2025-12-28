import streamlit as st
import pandas as pd
import sys
import os

# Import main.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import predict_sickle_cell

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Sickle Cell Predictor",
    page_icon="🩸",
    layout="wide",
)

# ---------- BEAUTIFUL CSS ----------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #f7f9fc 0%, #eef3f8 100%);
    font-family: 'Segoe UI', sans-serif;
}

/* Animated Gradient Title */
.gradient-title {
    font-size: 55px;
    font-weight: 900;
    background: linear-gradient(90deg, #8b0000, #c62828, #ff5252);
    -webkit-background-clip: text;
    color: transparent;
    animation: glow 3s infinite alternate;
    text-align: center;
}
@keyframes glow {
    from { text-shadow: 0px 0px 10px rgba(240,0,0,0.4); }
    to { text-shadow: 0px 0px 25px rgba(255,0,0,0.8); }
}

/* Sub-heading */
.sub-head {
    font-size: 22px;
    text-align: center;
    color: #444;
    margin-top: -10px;
}

/* Stylish Card */
.input-card {
    background: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.13);
    border: 2px solid #ececec;
    transition: 0.3s;
}
.input-card:hover {
    transform: scale(1.01);
    box-shadow: 0px 12px 35px rgba(0,0,0,0.18);
}

/* Result Boxes */
.result-positive {
    background: #ffdde0;
    padding: 20px;
    border-radius: 15px;
    border-left: 10px solid #b71c1c;
    font-size: 22px;
    color: #7f0000;
    font-weight: 600;
}
.result-negative {
    background: #d6f5d6;
    padding: 20px;
    border-radius: 15px;
    border-left: 10px solid #1b5e20;
    font-size: 22px;
    color: #0b3d0b;
    font-weight: 600;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #b71c1c, #ff5252);
    color: white;
    padding: 12px 20px;
    border-radius: 12px;
    font-size: 18px;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #d50000, #ff1744);
}

</style>
""", unsafe_allow_html=True)


# ---------- TITLE ----------
st.markdown("<div class='gradient-title'>🩸 SICKLE CELL PREDICTION</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-head'>AI-powered Medical Diagnostic Assistant</div>", unsafe_allow_html=True)

st.write("") ; st.write("")

# ---------- MODE SELECTION ----------
mode = st.radio("Select Prediction Mode:", ["Single Prediction", "Multiple Predictions"], horizontal=True)

# ========================================================================
# 1️⃣ SINGLE PREDICTION MODE
# ========================================================================
if mode == "Single Prediction":

    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)

        st.markdown("### 🧬 Enter Patient Details")

        gender = st.selectbox("Gender", ["Male", "Female"])
        hemoglobin = st.number_input("Hemoglobin (g/dL)", 0.1, 30.0, 12.0)
        mch = st.number_input("MCH (pg)", 0.1, 50.0, 25.0)
        mchc = st.number_input("MCHC (g/dL)", 0.1, 50.0, 32.0)
        mcv = st.number_input("MCV (fL)", 0.1, 150.0, 90.0)

        submit = st.button("🔍 Predict Now")

        st.markdown("</div>", unsafe_allow_html=True)

    if submit:
        result = predict_sickle_cell(gender, hemoglobin, mch, mchc, mcv)

        st.markdown("---")

        if result == "Positive":
            st.markdown("""
            <div class="result-positive">
                🩸 <strong>Sickle Cell Detected (Positive)</strong><br>  
                Immediate medical evaluation recommended.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-negative">
                🟢 <strong>No Sickle Cell Detected (Negative)</strong><br>
                Patient appears within a normal range.
            </div>
            """, unsafe_allow_html=True)


# ========================================================================
# 2️⃣ MULTIPLE PREDICTIONS MODE
# ========================================================================
else:

    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("### 📥 Upload CSV or Enter Multiple Patients")

    uploaded = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.write("### 📊 Preview Data", df)

    else:
        rows = st.number_input("How many patient entries?", 1, 50, 1)

        form_data = []

        for i in range(rows):
            st.markdown(f"### 🧍 Patient {i+1}")
            c1, c2, c3, c4, c5 = st.columns(5)

            with c1: g = st.selectbox(f"Gender {i}", ["Male", "Female"], key=f"g{i}")
            with c2: h = st.number_input(f"HB {i}", 0.1, 30.0, 12.0, key=f"h{i}")
            with c3: m1 = st.number_input(f"MCH {i}", 0.1, 50.0, 25.0, key=f"m1{i}")
            with c4: m2 = st.number_input(f"MCHC {i}", 0.1, 50.0, 32.0, key=f"m2{i}")
            with c5: mv = st.number_input(f"MCV {i}", 0.1, 150.0, 90.0, key=f"mv{i}")

            form_data.append([g, h, m1, m2, mv])

        df = pd.DataFrame(form_data, columns=["Gender", "Hemoglobin", "MCH", "MCHC", "MCV"])

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔍 Predict All Patients", use_container_width=True):
        results = []

        for _, row in df.iterrows():
            results.append(
                predict_sickle_cell(
                    row["Gender"], row["Hemoglobin"], row["MCH"], row["MCHC"], row["MCV"]
                )
            )

        df["Prediction"] = results

        st.success("✔ Predictions Completed")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download Results CSV", csv, "sickle_predictions.csv", "text/csv")

