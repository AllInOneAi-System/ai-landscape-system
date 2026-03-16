"""
AI Complete Landscape 2026
Streamlit app — injects HTML/CSS/JS directly into page (no iframe)
Modal จะ render ถูกต้อง ไม่ต้อง scroll หา
"""

import streamlit as st
import pathlib
import re

st.set_page_config(
    page_title="AI Complete Landscape 2026",
    page_icon="⚡",
    layout="wide",
)

# ── Load HTML ──────────────────────────────────────────────────────────────
html_path = pathlib.Path(__file__).parent / "index.html"
raw = html_path.read_text(encoding="utf-8")

# ── Extract <style> blocks ─────────────────────────────────────────────────
styles = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", raw, re.DOTALL))

# ── Extract <body> content ─────────────────────────────────────────────────
body_match = re.search(r"<body[^>]*>(.*?)</body>", raw, re.DOTALL)
body = body_match.group(1) if body_match else ""

# ── Extract <script> blocks ────────────────────────────────────────────────
scripts = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", raw, re.DOTALL))

# ── Hide ALL Streamlit chrome ──────────────────────────────────────────────
st.markdown("""
<style>
    #MainMenu, header, footer,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    .stAppDeployButton { display: none !important; }

    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"],
    .block-container,
    .main > div {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Inject CSS ─────────────────────────────────────────────────────────────
st.markdown(f"<style>{styles}</style>", unsafe_allow_html=True)

# ── Inject Body HTML ───────────────────────────────────────────────────────
st.markdown(body, unsafe_allow_html=True)

# ── Inject JS ─────────────────────────────────────────────────────────────
st.markdown(f"<script>{scripts}</script>", unsafe_allow_html=True)
