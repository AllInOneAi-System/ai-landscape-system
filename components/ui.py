"""
UI Components Layer
Reusable Streamlit UI building blocks
"""

import streamlit as st
from data.tools import TIERS


TIER_COLORS = {
    "t1": "#7C6FE0",
    "t2": "#3DAF82",
    "t3": "#E09040",
    "t4": "#6090D0",
    "t5": "#D06080",
}

TIER_BG = {
    "t1": "rgba(124,111,224,0.12)",
    "t2": "rgba(61,175,130,0.12)",
    "t3": "rgba(224,144,64,0.12)",
    "t4": "rgba(96,144,208,0.12)",
    "t5": "rgba(208,96,128,0.12)",
}


def render_api_card(tool_key: str, tool: dict) -> bool:
    """Render a clickable API card. Returns True if clicked."""
    color = TIER_COLORS.get(tool["tier"], "#7C6FE0")
    bg = TIER_BG.get(tool["tier"], "rgba(124,111,224,0.12)")

    chips_html = "".join([
        f'<span style="font-size:10px;padding:2px 8px;border-radius:4px;'
        f'border:1px solid {color};color:{color};margin-right:4px;">{c}</span>'
        for c in tool["chips"][:3]
    ])

    st.markdown(f"""
    <div style="
        background:#16161A;border:1px solid {color}40;border-radius:10px;
        padding:14px 15px;margin-bottom:4px;cursor:pointer;
        transition:all .2s;
    ">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
            <span style="font-size:20px;">{tool['icon']}</span>
            <span style="font-family:'Syne',sans-serif;font-size:13px;
                font-weight:700;color:{color};">{tool['title']}</span>
        </div>
        <p style="font-size:11.5px;color:#888780;margin-bottom:8px;line-height:1.5;">
            {tool['subtitle']}</p>
        <div style="margin-bottom:8px;">{chips_html}</div>
        <span style="display:inline-flex;align-items:center;gap:4px;
            font-size:10px;color:{color};background:{bg};
            border:1px solid {color}40;border-radius:4px;padding:2px 8px;">
            ⚡ ใช้งานได้เลย
        </span>
    </div>
    """, unsafe_allow_html=True)

    return st.button(
        f"เปิด {tool['title']}",
        key=f"btn_{tool_key}",
        use_container_width=True,
        type="secondary",
    )


def render_no_api_card(tool: dict):
    """Render a no-API info card with external links."""
    chips_html = "".join([
        f'<span style="font-size:10px;padding:2px 8px;border-radius:4px;'
        f'border:1px solid #444;color:#888;margin-right:4px;">{c}</span>'
        for c in tool["chips"][:3]
    ])

    links_html = "".join([
        f'<a href="{url}" target="_blank" style="display:inline-block;'
        f'font-size:11px;color:#888;border:1px solid #333;border-radius:4px;'
        f'padding:2px 8px;margin-right:4px;text-decoration:none;">{name} ↗</a>'
        for name, url in tool["links"]
    ])

    st.markdown(f"""
    <div style="background:#16161A;border:1px solid #28282E;
        border-radius:10px;padding:14px 15px;margin-bottom:4px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
            <span style="font-size:20px;">{tool['icon']}</span>
            <span style="font-size:13px;font-weight:700;color:#E8E6E0;">{tool['title']}</span>
        </div>
        <p style="font-size:11.5px;color:#888780;margin-bottom:8px;line-height:1.5;">
            {tool['desc']}</p>
        <div style="margin-bottom:8px;">{chips_html}</div>
        <div>{links_html}</div>
    </div>
    """, unsafe_allow_html=True)


def render_tier_header(tier: dict):
    """Render a tier section header."""
    color = tier["color"]
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;
        padding:16px;background:#16161A;border-radius:10px;
        border-left:3px solid {color};">
        <span style="background:{color}20;color:{color};font-size:11px;
            padding:4px 10px;border-radius:4px;font-weight:600;white-space:nowrap;">
            {tier['label']}
        </span>
        <div>
            <div style="font-size:17px;font-weight:700;color:{color};">
                {tier['title']}</div>
            <div style="font-size:12px;color:#888780;">{tier['subtitle']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_summary_bar(stats: dict):
    """Render the stats summary bar."""
    cols = st.columns(4)
    items = [
        ("5", "ระดับหลัก", "#7C6FE0"),
        ("44", "หมวดย่อย", "#3DAF82"),
        ("10", "tool ใช้งานได้เลย", "#E09040"),
        ("150+", "เครื่องมือในตลาด", "#888780"),
    ]
    for col, (num, label, color) in zip(cols, items):
        with col:
            st.markdown(f"""
            <div style="text-align:center;padding:16px;background:#16161A;
                border-radius:8px;border:1px solid #28282E;">
                <div style="font-size:28px;font-weight:800;color:{color};
                    font-family:'Syne',sans-serif;">{num}</div>
                <div style="font-size:11px;color:#888780;">{label}</div>
            </div>
            """, unsafe_allow_html=True)


def render_chat_message(role: str, content: str):
    """Render a single chat message bubble."""
    if role == "user":
        st.markdown(f"""
        <div style="display:flex;justify-content:flex-end;margin-bottom:10px;">
            <div style="max-width:80%;background:rgba(124,111,224,0.12);
                border:1px solid rgba(124,111,224,0.25);border-radius:10px;
                padding:12px 14px;">
                <div style="font-size:10px;color:#7C6FE0;margin-bottom:4px;">คุณ</div>
                <div style="font-size:13px;line-height:1.6;color:#E8E6E0;
                    white-space:pre-wrap;">{content}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display:flex;justify-content:flex-start;margin-bottom:10px;">
            <div style="max-width:80%;background:#1E1E24;
                border:1px solid #28282E;border-radius:10px;
                padding:12px 14px;">
                <div style="font-size:10px;color:#3DAF82;margin-bottom:4px;">Claude ✦</div>
                <div style="font-size:13px;line-height:1.6;color:#E8E6E0;
                    white-space:pre-wrap;">{content}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_info_grid(info: dict):
    """Render tool info key-value grid."""
    items = list(info.items())
    cols = st.columns(2)
    for i, (key, val) in enumerate(items):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background:#1E1E24;border:1px solid #28282E;
                border-radius:8px;padding:12px;margin-bottom:8px;">
                <div style="font-size:10px;color:#888780;margin-bottom:3px;
                    text-transform:uppercase;letter-spacing:.05em;">{key}</div>
                <div style="font-size:13px;color:#E8E6E0;font-weight:500;">{val}</div>
            </div>
            """, unsafe_allow_html=True)


def apply_global_styles():
    """Inject global CSS for dark theme."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Noto+Sans+Thai:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0E0E10 !important;
        color: #E8E6E0 !important;
        font-family: 'Noto Sans Thai', 'Syne', sans-serif !important;
    }
    [data-testid="stSidebar"] {
        background-color: #16161A !important;
        border-right: 1px solid #28282E !important;
    }
    [data-testid="stSidebar"] * { color: #E8E6E0 !important; }
    .stButton > button {
        background: #16161A !important;
        border: 1px solid #28282E !important;
        color: #E8E6E0 !important;
        border-radius: 8px !important;
        font-size: 12px !important;
    }
    .stButton > button:hover {
        border-color: #7C6FE0 !important;
        color: #7C6FE0 !important;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #1E1E24 !important;
        border: 1px solid #28282E !important;
        color: #E8E6E0 !important;
        border-radius: 8px !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #7C6FE0 !important;
        box-shadow: 0 0 0 1px #7C6FE040 !important;
    }
    .stSelectbox > div > div {
        background: #1E1E24 !important;
        border: 1px solid #28282E !important;
        color: #E8E6E0 !important;
    }
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        color: #E8E6E0 !important;
        font-family: 'Syne', sans-serif !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #888780 !important;
        font-size: 12px !important;
    }
    .stTabs [aria-selected="true"] {
        color: #7C6FE0 !important;
    }
    div[data-testid="stExpander"] {
        background: #16161A !important;
        border: 1px solid #28282E !important;
        border-radius: 8px !important;
    }
    hr { border-color: #28282E !important; }
    .stAlert { background: #1E1E24 !important; border: 1px solid #28282E !important; }
    </style>
    """, unsafe_allow_html=True)
