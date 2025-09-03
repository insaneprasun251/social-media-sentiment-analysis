import streamlit as st

st.title("youtube")
st.write("youtube")

# Example placeholder
query = st.text_input("Enter a keyword (e.g., haldi)", "haldi")

if st.button("Fetch Trends"):
    st.success(f"Showing trends for: {query}")
    st.line_chart({"Interest": [48, 60, 70, 100, 85, 66, 54]})