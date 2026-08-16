from constants import FOREST, SAND, RUST, SAGE, CREAM, WHITE, MIST


def get_global_css() -> str:
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Reset & Base ── */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        -webkit-font-smoothing: antialiased;
    }}

    /* ── Hide native Streamlit sidebar ── */
    section[data-testid="stSidebar"] {{ display: none !important; }}
    section[data-testid="stSidebar"] * {{ display: none !important; }}

    /* ── App background: warm cream ── */
    .stApp,
    .main,
    .main > div,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > .main {{
        background-color: {CREAM} !important;
    }}
    .main .block-container {{
        background-color: {CREAM} !important;
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }}

    /* ── Custom sidebar column ── */
    .prepo-sidebar {{
        background: {WHITE};
        border-right: 1px solid #E8E4DC;
        min-height: 100vh;
        padding: 24px 16px;
        position: sticky;
        top: 0;
    }}

    /* ── Global text colors ── */
    .main p, .main div, .main span, .main label {{
        color: {FOREST};
    }}
    h1, h2, h3 {{ color: {FOREST}; }}

    /* ── Buttons: RESET to neutral, styled per use ── */
    .stButton > button {{
        background: transparent !important;
        color: {FOREST} !important;
        border: 1.5px solid #D8D3C8 !important;
        border-radius: 9px !important;
        font-weight: 500 !important;
        font-size: 13.5px !important;
        font-family: 'Inter', sans-serif !important;
        padding: 8px 16px !important;
        transition: all 0.18s ease !important;
        text-align: left !important;
    }}
    .stButton > button:hover {{
        background: {FOREST}08 !important;
        border-color: {FOREST}40 !important;
    }}

    /* Primary CTA button (Upload New File, submit etc.) */
    .stButton > button[kind="primary"] {{
        background: {FOREST} !important;
        color: #FEFAE0 !important;
        border: none !important;
        font-weight: 600 !important;
        text-align: center !important;
    }}
    .stButton > button[kind="primary"]:hover {{
        background: {SAGE} !important;
        opacity: 1 !important;
    }}

    /* Active/selected nav button */
    .stButton > button:disabled {{
        background: {FOREST}12 !important;
        color: {FOREST} !important;
        border-color: {FOREST}30 !important;
        opacity: 1 !important;
        font-weight: 600 !important;
    }}

    /* Sidebar column: white background via column targeting */
    [data-testid="column"]:first-child {{
        background: {WHITE};
        border-right: 1px solid #E8E4DC;
        min-height: 100vh;
        padding: 24px 12px !important;
        border-radius: 0;
    }}

    /* Suggestion chip buttons: pill style */
    [data-testid="stHorizontalBlock"] [data-testid="column"] .stButton > button {{
        background: {WHITE} !important;
        border: 1.5px solid #E0DCD4 !important;
        border-radius: 20px !important;
        font-size: 12.5px !important;
        font-weight: 400 !important;
        color: {FOREST} !important;
        padding: 6px 14px !important;
        text-align: center !important;
        white-space: nowrap !important;
    }}
    [data-testid="stHorizontalBlock"] [data-testid="column"] .stButton > button:hover {{
        background: {FOREST}08 !important;
        border-color: {FOREST}40 !important;
    }}

    /* Action card arrow buttons: small clean arrows */
    .action-arrow-btn .stButton > button {{
        background: transparent !important;
        border: none !important;
        color: {FOREST} !important;
        font-size: 18px !important;
        padding: 0 !important;
        width: auto !important;
    }}

    /* ── Chat input ── */
    .stChatInput > div {{
        border: 1.5px solid #D8D3C8 !important;
        border-radius: 12px !important;
        background: {WHITE} !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    }}
    .stChatInput textarea {{
        background: transparent !important;
        color: {FOREST} !important;
        font-size: 14px !important;
        font-family: 'Inter', sans-serif !important;
    }}
    .stChatInput button {{
        background: {FOREST} !important;
        border-radius: 8px !important;
        border: none !important;
    }}

    /* ── Text inputs ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        background: {WHITE} !important;
        border: 1.5px solid #D8D3C8 !important;
        border-radius: 9px !important;
        color: {FOREST} !important;
        font-size: 14px !important;
        font-family: 'Inter', sans-serif !important;
    }}
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {FOREST}60 !important;
        box-shadow: 0 0 0 3px {FOREST}10 !important;
    }}

    /* ── Select boxes ── */
    .stSelectbox > div > div {{
        background: {WHITE} !important;
        border: 1.5px solid #D8D3C8 !important;
        border-radius: 9px !important;
        color: {FOREST} !important;
    }}

    /* ── Radio buttons ── */
    .stRadio > div > label {{
        color: {FOREST} !important;
        font-size: 14px !important;
    }}

    /* ── File uploader ── */
    .stFileUploader {{
        background: {WHITE} !important;
        border: 2px dashed #D8D3C8 !important;
        border-radius: 14px !important;
    }}
    [data-testid="stFileUploaderDropzone"] {{
        background: {CREAM} !important;
    }}

    /* ── Slider ── */
    .stSlider > div > div > div > div {{
        background: {SAGE} !important;
    }}

    /* ── Spinner / progress ── */
    .stSpinner > div {{
        border-top-color: {FOREST} !important;
    }}
    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, {SAGE}, {FOREST}) !important;
    }}

    /* ── Alerts ── */
    .stAlert {{
        border-radius: 10px !important;
    }}

    /* ── Chat messages ── */
    [data-testid="stChatMessage"] {{
        background: {WHITE} !important;
        border: 1px solid #E8E4DC !important;
        border-radius: 12px !important;
        margin-bottom: 8px !important;
    }}

    /* ── Status widget ── */
    [data-testid="stStatusWidget"] {{
        border-radius: 12px !important;
    }}

    /* ── Dividers ── */
    hr {{
        border: none !important;
        border-top: 1px solid #E8E4DC !important;
        margin: 16px 0 !important;
    }}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {{ width: 5px; height: 5px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{
        background: #C8C4BC;
        border-radius: 3px;
    }}

    /* ── Expander ── */
    .streamlit-expanderHeader {{
        background: {WHITE} !important;
        border-radius: 10px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        color: {FOREST} !important;
    }}

    /* ── Hide Streamlit branding ── */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header {{ visibility: hidden; }}

    /* ── Micro-animations ── */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    .anim-fadein {{
        animation: fadeInUp 0.35s ease both;
    }}

    /* ── Utility classes ── */
    .section-label {{
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: #9E9B96;
        margin-bottom: 10px;
        margin-top: 20px;
    }}
    </style>
    """


# ── HTML helpers (kept for backward compatibility) ─────────────────────────────

def page_header_html(icon: str, title: str, subtitle: str = "") -> str:
    subtitle_html = (
        f'<div style="font-size:13.5px;color:{SAGE};margin-top:3px;">{subtitle}</div>'
        if subtitle else ""
    )
    return f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:28px;
                padding-bottom:16px;border-bottom:1.5px solid #E8E4DC;">
        <div style="width:42px;height:42px;background:{CREAM};border:1.5px solid #D8D3C8;
                    border-radius:11px;display:flex;align-items:center;justify-content:center;
                    font-size:20px;">{icon}</div>
        <div>
            <h1 style="font-family:'Playfair Display',serif;font-size:24px;font-weight:700;
                        color:{FOREST};margin:0;">{title}</h1>
            {subtitle_html}
        </div>
    </div>
    """


def metric_html(value: str, label: str, delta: str = "", delta_positive: bool = True) -> str:
    delta_color = SAGE if delta_positive else RUST
    delta_html = (
        f'<div style="font-size:11px;color:{delta_color};margin-top:2px;font-weight:600;">'
        f'{"▲" if delta_positive else "▼"} {delta}</div>'
        if delta else ""
    )
    return f"""
    <div style="background:{WHITE};border:1.5px solid #E8E4DC;border-radius:12px;
                padding:16px;text-align:center;box-shadow:0 2px 6px rgba(0,0,0,0.04);">
        <div style="font-family:'Playfair Display',serif;font-size:28px;font-weight:700;
                    color:{FOREST};">{value}</div>
        <div style="font-size:11px;color:#9E9B96;text-transform:uppercase;
                    letter-spacing:1px;margin-top:4px;font-weight:500;">{label}</div>
        {delta_html}
    </div>
    """


def badge_html(text: str, color: str = SAGE) -> str:
    return f"""<span style="display:inline-block;padding:3px 10px;background:{color}18;
        color:{color};border:1px solid {color}40;border-radius:20px;
        font-size:11.5px;font-weight:600;">{text}</span>"""


def info_box_html(message: str, kind: str = "info") -> str:
    palette = {
        "info":    (SAGE,      "#F0F7F0"),
        "warning": (RUST,      "#FFF8F0"),
        "success": (SAGE,      "#F0F7F0"),
        "error":   ("#C62828", "#FFF0F0"),
    }
    border_color, bg = palette.get(kind, palette["info"])
    return f"""
    <div style="padding:12px 16px;background:{bg};border-left:3px solid {border_color};
                border-radius:0 10px 10px 0;margin:10px 0;font-size:13.5px;
                color:{FOREST};line-height:1.6;">{message}</div>
    """


def stat_card_html(value: str, label: str, color: str = SAND) -> str:
    return f"""
    <div style="text-align:center;padding:10px 8px;background:#FFFFFF0C;
                border-radius:10px;border:1px solid #FFFFFF15;">
        <div style="font-size:20px;font-weight:700;color:{color};">{value}</div>
        <div style="font-size:10px;color:#FFFFFF55;text-transform:uppercase;
                    letter-spacing:0.9px;margin-top:2px;">{label}</div>
    </div>
    """