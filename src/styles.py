from constants import FOREST, SAND, RUST, SAGE, CREAM, WHITE, MIST


def get_global_css() -> str:
    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {{
        background: {FOREST} !important;
        border-right: 1px solid #FFFFFF12;
    }}
    section[data-testid="stSidebar"] * {{
        color: {CREAM};
    }}

    /* Nav buttons inside sidebar */
    div[data-testid="stSidebar"] button {{
        background: transparent !important;
        border: none !important;
        color: #FFFFFFB0 !important;
        text-align: left !important;
        font-size: 13.5px !important;
        padding: 9px 14px !important;
        border-radius: 9px !important;
        margin-bottom: 4px !important;
        transition: background 0.2s, color 0.2s;
    }}
    div[data-testid="stSidebar"] button:hover {{
        background: #FFFFFF12 !important;
        color: {CREAM} !important;
    }}

    /* ── Main area ── */
    .stApp {{
        background-color: {CREAM} !important;
    }}
    .main, .main > div, [data-testid="stAppViewContainer"] {{
        background-color: {CREAM} !important;
    }}
    [data-testid="stAppViewContainer"] > .main {{
        background-color: {CREAM} !important;
    }}
    .main .block-container {{
        background-color: {CREAM} !important;
        padding-top: 2rem;
        max-width: 1100px;
    }}
    /* Force text colors for main area */
    .main p, .main div, .main span, .main label {{
        color: {FOREST};
    }}

    /* ── Reusable card ── */
    .prepo-card {{
        background: {WHITE};
        border: 1.5px solid {SAND}28;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }}

    /* ── Streamlit widget tweaks ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        background: {WHITE} !important;
        border: 1.5px solid {SAND}40 !important;
        border-radius: 9px !important;
        color: {FOREST} !important;
        font-size: 14px !important;
    }}
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {SAND} !important;
        box-shadow: 0 0 0 2px {SAND}25 !important;
    }}

    .stSelectbox > div > div {{
        background: {WHITE} !important;
        border: 1.5px solid {SAND}40 !important;
        border-radius: 9px !important;
        color: {FOREST} !important;
    }}

    /* Primary buttons */
    .stButton > button[kind="primary"],
    .stButton > button {{
        background: linear-gradient(135deg, {SAGE}, {FOREST}) !important;
        color: {CREAM} !important;
        border: none !important;
        border-radius: 9px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 9px 20px !important;
        transition: opacity 0.2s, transform 0.1s;
    }}
    .stButton > button:hover {{
        opacity: 0.88 !important;
        transform: translateY(-1px);
    }}
    .stButton > button:active {{
        transform: translateY(0);
    }}

    /* File uploader */
    .stFileUploader {{
        background: {WHITE} !important;
        border: 2px dashed {SAND}50 !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }}

    /* Metrics */
    [data-testid="stMetric"] {{
        background: {WHITE};
        border: 1px solid {SAND}28;
        border-radius: 12px;
        padding: 14px 18px;
    }}

    /* Slider */
    .stSlider > div > div > div > div {{
        background: {SAND} !important;
    }}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{
        background: {SAND}60;
        border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: {SAND};
    }}

    /* ── Misc ── */
    hr {{
        border: none;
        border-top: 1px solid #FFFFFF18;
        margin: 10px 0;
    }}
    a {{
        color: {RUST};
        text-decoration: none;
    }}
    a:hover {{
        text-decoration: underline;
    }}
    </style>
    """


def sidebar_logo_html() -> str:
    return f"""
    <div style="
        padding: 18px 16px 10px 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    ">
        <div style="
            width: 38px; height: 38px;
            background: linear-gradient(135deg, {SAGE}, {FOREST});
            border-radius: 10px;
            border: 2px solid #FFFFFF25;
            display: flex; align-items: center; justify-content: center;
            font-size: 20px; flex-shrink: 0;
        ">🌿</div>
        <div>
            <div style="
                font-family: 'Playfair Display', serif;
                font-size: 18px; font-weight: 700;
                color: {CREAM}; line-height: 1.1;
            ">Prepo<span style="color:{SAND};">AI</span></div>
            <div style="
                font-size: 10px; color: #FFFFFF50;
                letter-spacing: 1.2px; text-transform: uppercase;
            ">Study Smarter</div>
        </div>
    </div>
    """


def page_header_html(icon: str, title: str, subtitle: str = "") -> str:
    subtitle_html = (
        f'<div style="font-size:13.5px;color:{SAGE};margin-top:3px;line-height:1.4;">{subtitle}</div>'
        if subtitle else ""
    )
    return f"""
    <div style="
        display: flex; align-items: center; gap: 12px;
        margin-bottom: 28px;
        padding-bottom: 16px;
        border-bottom: 2px solid {SAND}30;
    ">
        <div style="
            width: 44px; height: 44px;
            background: linear-gradient(135deg, {SAND}30, {RUST}20);
            border-radius: 12px;
            border: 1.5px solid {SAND}40;
            display: flex; align-items: center; justify-content: center;
            font-size: 22px; flex-shrink: 0;
        ">{icon}</div>
        <div>
            <h1 style="
                font-family: 'Playfair Display', serif;
                font-size: 26px; font-weight: 700;
                color: {FOREST}; margin: 0; line-height: 1.2;
            ">{title}</h1>
            {subtitle_html}
        </div>
    </div>
    """


def metric_html(value: str, label: str, delta: str = "", delta_positive: bool = True) -> str:
    """Stat/metric card for dashboard rows."""
    delta_color = SAGE if delta_positive else RUST
    delta_html = (
        f'<div style="font-size:11.5px;color:{delta_color};margin-top:3px;font-weight:600;">'
        f'{"▲" if delta_positive else "▼"} {delta}</div>'
        if delta else ""
    )
    return f"""
    <div style="
        background: {WHITE};
        border: 1.5px solid {SAND}28;
        border-radius: 13px;
        padding: 18px 16px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    ">
        <div style="
            font-family: 'Playfair Display', serif;
            font-size: 30px; font-weight: 700;
            color: {FOREST}; line-height: 1.1;
        ">{value}</div>
        <div style="
            font-size: 11px; color: {SAGE};
            text-transform: uppercase; letter-spacing: 1px;
            margin-top: 5px; font-weight: 500;
        ">{label}</div>
        {delta_html}
    </div>
    """


def stat_card_html(value: str, label: str, color: str = SAND) -> str:
    """Small stat card used in dashboards/sidebars."""
    return f"""
    <div style="
        text-align: center; padding: 10px 8px;
        background: #FFFFFF0C;
        border-radius: 10px;
        border: 1px solid #FFFFFF15;
    ">
        <div style="font-size: 20px; font-weight: 700; color: {color}; line-height: 1.2;">{value}</div>
        <div style="font-size: 10px; color: #FFFFFF55; text-transform: uppercase; letter-spacing: 0.9px; margin-top: 2px;">{label}</div>
    </div>
    """


def badge_html(text: str, color: str = SAGE) -> str:
    """Inline pill badge."""
    return f"""<span style="
        display: inline-block;
        padding: 3px 10px;
        background: {color}22;
        color: {color};
        border: 1px solid {color}50;
        border-radius: 20px;
        font-size: 11.5px;
        font-weight: 600;
        letter-spacing: 0.4px;
    ">{text}</span>"""


def info_box_html(message: str, kind: str = "info") -> str:
    """Coloured info / warning / success box."""
    palette = {
        "info":    (SAGE,  "#E8F5E9"),
        "warning": (RUST,  "#FFF3E0"),
        "success": (SAGE,  "#F1F8E9"),
        "error":   ("#C62828", "#FFEBEE"),
    }
    border_color, bg = palette.get(kind, palette["info"])
    return f"""
    <div style="
        padding: 13px 16px;
        background: {bg};
        border-left: 4px solid {border_color};
        border-radius: 0 10px 10px 0;
        margin: 10px 0;
        font-size: 13.5px;
        color: {FOREST};
        line-height: 1.6;
    ">{message}</div>
    """