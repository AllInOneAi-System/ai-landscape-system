"""
AI Complete Landscape 2026
Streamlit app — embeds original HTML UI directly
"""

import streamlit as st
import pathlib

st.set_page_config(
    page_title="AI Complete Landscape 2026",
    page_icon="⚡",
    layout="wide",
)

# Hide Streamlit default UI chrome
st.markdown("""
<style>
    #MainMenu, header, footer { display: none !important; }
    .stAppDeployButton { display: none !important; }
    [data-testid="stAppViewContainer"] {
        padding: 0 !important;
    }
    [data-testid="stAppViewBlockContainer"] {
        padding: 0 !important;
        max-width: 100% !important;
    }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# Load HTML file
html_path = pathlib.Path(__file__).parent / "index.html"
html_content = html_path.read_text(encoding="utf-8")

# Embed full HTML
st.components.v1.html(html_content, height=4000, scrolling=True)
