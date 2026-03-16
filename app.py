"""
AI Complete Landscape 2026
Main Streamlit Application Entry Point

Architecture:
    UI Layer         → app.py (this file)
    Component Layer  → components/ui.py
    Service Layer    → services/claude_service.py
    Data Layer       → data/tools.py
"""

import streamlit as st
from components.ui import (
    apply_global_styles,
    render_summary_bar,
    render_tier_header,
    render_api_card,
    render_no_api_card,
    render_chat_message,
    render_info_grid,
    TIER_COLORS,
)
from data.tools import TIERS, API_TOOLS, NO_API_TOOLS, SUMMARY_STATS
from services.claude_service import stream_response, validate_api_key

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Complete Landscape 2026",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_styles()


# ── SESSION STATE ────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "api_key": "",
        "api_key_valid": False,
        "active_tool": None,
        "chat_histories": {},   # {tool_key: [{"role": ..., "content": ...}]}
        "selected_tier": "all",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()


# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:12px 0 20px;">
        <div style="font-size:10px;color:#7C6FE0;font-family:'DM Mono',monospace;
            letter-spacing:.1em;margin-bottom:6px;">// AI LANDSCAPE 2026</div>
        <div style="font-size:20px;font-weight:800;font-family:'Syne',sans-serif;">
            ⚡ AI มีกี่หมวด<br>จริงๆ?</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # API Key Section
    st.markdown('<p style="font-size:11px;color:#888780;font-family:monospace;">// Anthropic API Key</p>', unsafe_allow_html=True)

    api_key_input = st.text_input(
        label="API Key",
        type="password",
        placeholder="sk-ant-...",
        value=st.session_state.api_key,
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("บันทึก Key", use_container_width=True):
            is_valid, msg = validate_api_key(api_key_input)
            if is_valid:
                st.session_state.api_key = api_key_input
                st.session_state.api_key_valid = True
                st.success(msg)
            else:
                st.session_state.api_key_valid = False
                st.error(msg)
    with col2:
        if st.button("ล้าง", use_container_width=True):
            st.session_state.api_key = ""
            st.session_state.api_key_valid = False
            st.rerun()

    if st.session_state.api_key_valid:
        st.markdown('<p style="font-size:11px;color:#3DAF82;">✓ API key พร้อมใช้งาน</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="font-size:11px;color:#888780;">ยังไม่ได้ใส่ key</p>', unsafe_allow_html=True)

    st.divider()

    # Tier Filter
    st.markdown('<p style="font-size:11px;color:#888780;font-family:monospace;">// กรองตาม Tier</p>', unsafe_allow_html=True)
    tier_options = {"all": "🔍 ทั้งหมด"}
    for t in TIERS:
        tier_options[t["id"]] = f"{t['label']} — {t['title']}"

    selected = st.selectbox(
        "Tier",
        options=list(tier_options.keys()),
        format_func=lambda x: tier_options[x],
        label_visibility="collapsed",
    )
    st.session_state.selected_tier = selected

    st.divider()

    # Stats
    st.markdown("""
    <div style="font-size:10px;color:#444;font-family:monospace;line-height:2;">
        // AI Complete Landscape<br>
        // 44 หมวด · 5 ระดับ<br>
        // March 2026<br>
        // Powered by Claude Sonnet
    </div>
    """, unsafe_allow_html=True)


# ── MAIN CONTENT ─────────────────────────────────────────────────────────────

# Hero Section
st.markdown("""
<div style="padding:40px 0 24px;">
    <div style="font-size:11px;color:#7C6FE0;font-family:monospace;
        letter-spacing:.12em;margin-bottom:12px;">// AI Complete Landscape · March 2026</div>
    <h1 style="font-family:'Syne',sans-serif;font-size:clamp(28px,4vw,44px);
        font-weight:800;line-height:1.1;letter-spacing:-.02em;margin-bottom:10px;">
        AI มีกี่หมวด <span style="color:#7C6FE0;">จริงๆ?</span>
    </h1>
    <p style="font-size:14px;color:#888780;max-width:520px;line-height:1.7;margin-bottom:20px;">
        ภาพรวมครบทุกหมวดของ AI ใน 5 ระดับ — card ที่มีไฟสีม่วงสามารถกดใช้งานได้เลยผ่าน Claude API
    </p>
    <div style="display:inline-flex;align-items:center;gap:5px;
        background:rgba(61,175,130,.12);border:1px solid rgba(61,175,130,.3);
        border-radius:20px;padding:6px 14px;font-size:11px;color:#3DAF82;font-family:monospace;">
        ⚡ กด card สีม่วง → ใช้งานได้เลยผ่าน Claude
    </div>
</div>
""", unsafe_allow_html=True)

# Summary Stats
render_summary_bar(SUMMARY_STATS)
st.markdown("<br>", unsafe_allow_html=True)


# ── TOOL MODAL (Dialog) ───────────────────────────────────────────────────────
@st.dialog("🤖 AI Tool", width="large")
def open_tool_dialog(tool_key: str):
    tool = API_TOOLS[tool_key]
    color = TIER_COLORS.get(tool["tier"], "#7C6FE0")

    # Header
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
        <span style="font-size:28px;">{tool['icon']}</span>
        <div>
            <div style="font-size:18px;font-weight:700;color:{color};
                font-family:'Syne',sans-serif;">{tool['title']}</div>
            <div style="font-size:12px;color:#888780;">{tool['subtitle']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_use, tab_prompts, tab_info = st.tabs(["💬 ใช้งาน", "📋 Prompt Templates", "ℹ️ ข้อมูล Tool"])

    # ── TAB: USE ──
    with tab_use:
        if not st.session_state.api_key:
            st.warning("⚠️ ยังไม่ได้ใส่ Anthropic API key — ใส่ใน Sidebar ด้านซ้าย แล้วกด 'บันทึก Key'")

        # Chat history display
        if tool_key not in st.session_state.chat_histories:
            st.session_state.chat_histories[tool_key] = []

        history = st.session_state.chat_histories[tool_key]

        chat_container = st.container(height=300)
        with chat_container:
            if not history:
                st.markdown(f'<p style="color:#444;font-size:12px;text-align:center;padding-top:40px;">เริ่มพิมพ์เพื่อใช้งาน {tool["title"]}</p>', unsafe_allow_html=True)
            for msg in history:
                render_chat_message(msg["role"], msg["content"])

        # Input
        user_input = st.text_area(
            "พิมพ์คำถามหรือ prompt",
            placeholder="พิมพ์คำถามหรือ prompt ที่นี่... (Ctrl+Enter เพื่อส่ง)",
            height=80,
            label_visibility="collapsed",
            key=f"input_{tool_key}",
        )

        col_send, col_clear = st.columns([3, 1])
        with col_send:
            send_clicked = st.button("ส่ง →", key=f"send_{tool_key}", type="primary", use_container_width=True)
        with col_clear:
            if st.button("ล้าง", key=f"clear_{tool_key}", use_container_width=True):
                st.session_state.chat_histories[tool_key] = []
                st.rerun()

        if send_clicked and user_input.strip():
            if not st.session_state.api_key:
                st.error("กรุณาใส่ API key ก่อน")
            else:
                history.append({"role": "user", "content": user_input.strip()})
                render_chat_message("user", user_input.strip())

                with st.spinner("Claude กำลังคิด..."):
                    try:
                        full_reply = ""
                        reply_placeholder = st.empty()
                        for chunk in stream_response(
                            api_key=st.session_state.api_key,
                            system_prompt=tool["system"],
                            messages=history,
                        ):
                            full_reply += chunk
                            reply_placeholder.markdown(
                                f'<div style="background:#1E1E24;border:1px solid #28282E;'
                                f'border-radius:8px;padding:12px;font-size:13px;'
                                f'line-height:1.6;color:#E8E6E0;white-space:pre-wrap;">'
                                f'<span style="font-size:10px;color:#3DAF82;display:block;'
                                f'margin-bottom:6px;">Claude ✦</span>{full_reply}▌</div>',
                                unsafe_allow_html=True
                            )

                        history.append({"role": "assistant", "content": full_reply})
                        st.session_state.chat_histories[tool_key] = history
                        st.rerun()

                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {str(e)}")
                        history.pop()

    # ── TAB: PROMPTS ──
    with tab_prompts:
        st.markdown('<p style="font-size:11px;color:#888780;font-family:monospace;margin-bottom:12px;">เลือก template แล้วแก้ไขได้</p>', unsafe_allow_html=True)
        for prompt in tool["prompts"]:
            with st.expander(f"📌 {prompt['label']}"):
                st.code(prompt["text"], language=None)
                if st.button(f"ใช้ template นี้", key=f"tpl_{tool_key}_{prompt['label']}"):
                    st.session_state[f"input_{tool_key}"] = prompt["text"]
                    st.rerun()

    # ── TAB: INFO ──
    with tab_info:
        render_info_grid(tool["info"])
        st.markdown('<p style="font-size:11px;color:#888780;font-family:monospace;margin:12px 0 8px;">ลิงก์ tool หลัก</p>', unsafe_allow_html=True)
        for name, url in tool["links"]:
            st.markdown(f'<a href="{url}" target="_blank" style="display:block;padding:9px 12px;background:#1E1E24;border:1px solid #28282E;border-radius:8px;text-decoration:none;color:#E8E6E0;font-size:13px;margin-bottom:6px;">{name} <span style="color:#888;font-size:11px;float:right;">↗ เปิดเว็บ</span></a>', unsafe_allow_html=True)


# ── CARD GRID ─────────────────────────────────────────────────────────────────
selected_tier = st.session_state.selected_tier

for tier in TIERS:
    # Filter by selected tier
    if selected_tier != "all" and selected_tier != tier["id"]:
        continue

    render_tier_header(tier)

    # Get tools for this tier
    tier_api_tools = {k: v for k, v in API_TOOLS.items() if v["tier"] == tier["id"]}
    tier_no_api_tools = [t for t in NO_API_TOOLS if t["tier"] == tier["id"]]

    all_tier_tools = list(tier_api_tools.items()) + [(None, t) for t in tier_no_api_tools]

    if not all_tier_tools:
        continue

    # 3-column grid
    cols = st.columns(3)
    for i, item in enumerate(all_tier_tools):
        with cols[i % 3]:
            if item[0] is not None:
                # API Tool
                tool_key, tool = item
                clicked = render_api_card(tool_key, tool)
                if clicked:
                    open_tool_dialog(tool_key)
            else:
                # No-API Tool
                render_no_api_card(item[1])

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

# Footer
st.markdown("""
<div style="text-align:center;padding:24px 0;color:#444;font-size:11px;font-family:monospace;">
    // AI Complete Landscape · 44 หมวด · 5 ระดับ · March 2026<br>
    // Powered by Claude Sonnet · Anthropic
</div>
""", unsafe_allow_html=True)
