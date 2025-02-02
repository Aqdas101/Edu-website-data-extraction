import streamlit as st
from main import main
import json

# Set page configuration
st.set_page_config(page_title="Website Data Viewer", layout="wide")

# Main page heading
st.title("Course Data Extraction")

# Sidebar input
with st.sidebar:
    website_url = st.text_input("Enter website URL:", placeholder="https://example.com")
    if st.button('Extract'):
        data = main(website_url)
        st.write(data)
        

