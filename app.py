import streamlit as st

st.set_page_config(page_title="Iterative Sizing Tool", layout="wide")
st.title("Iterative Engineering Sizing Tool")
st.info("Starter interface. Connect this UI to your tested solver after the deterministic code works.")

st.subheader("Inputs")
st.number_input("Target", value=100.0)
st.number_input("Starting value", value=1.0)
st.number_input("Tolerance", min_value=0.000001, value=0.01, format="%.6f")
st.number_input("Maximum iterations", min_value=1, value=50, step=1)

if st.button("Run calculation"):
    st.warning("Connect this button to your tested solver. Do not place all engineering logic inside app.py.")
