import streamlit as st

st.set_page_config(page_title="Social Media Dashboard", layout="wide")

st.title("Social Media Sentiment Analysis Dashboard")
st.write("Welcome to the dashboard!")
st.write("A dashboard that collects and analyzes social media data to visualize real-time sentiment trends and public opinion")
available_features = ["Twitter", "Reddit", "Google Trend Search"]
st.write("Currently available features:")
for i in available_features:
    st.markdown(f'<div style="margin-left: 40px; padding-bottom: 10px">&bull; &nbsp; {i}</div>', unsafe_allow_html=True)

st.info("Select a page from the sidebar.")
