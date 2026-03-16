"""
AI Complete Landscape 2026
Streamlit app — iframe embed + modal viewport fix
"""

import streamlit as st
import pathlib

st.set_page_config(
    page_title="AI Complete Landscape 2026",
    page_icon="⚡",
    layout="wide",
)

st.markdown("""
<style>
    #MainMenu, header, footer,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    .stAppDeployButton { display: none !important; }
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"],
    .block-container { padding: 0 !important; max-width: 100% !important; }
</style>
""", unsafe_allow_html=True)

html_path = pathlib.Path(__file__).parent / "index.html"
html = html_path.read_text(encoding="utf-8")

# Fix: modal uses position:fixed relative to iframe viewport
modal_fix = """
<style>
.modal-overlay {
    position: fixed !important;
    top: 0 !important; left: 0 !important;
    right: 0 !important; bottom: 0 !important;
    z-index: 9999 !important;
}
</style>
"""
html = html.replace("</head>", modal_fix + "</head>")

st.components.v1.html(html, height=5200, scrolling=True)
