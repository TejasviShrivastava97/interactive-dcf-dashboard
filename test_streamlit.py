import streamlit as st
import pandas as pd

st.title("🎉 Streamlit Test App")

# Slider
number = st.slider("Pick a number", 0, 100, 50)
st.write(f"You picked: {number}")

# Sample CSV table
data = {"Company": ["A", "B", "C"], "Revenue": [100, 200, 300]}
df = pd.DataFrame(data)
st.subheader("Sample Table")
st.dataframe(df)

# File uploader
uploaded_file = st.file_uploader("Upload CSV")
if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)
    st.write("Uploaded CSV:")
    st.dataframe(uploaded_df)
