from constants import CREAM, WHITE, FOREST, SAND, RUST, SAGE, MIST

def get_global_css() -> str:
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/*GLOBAL*/
html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif !important; }}
.stApp {{ background: {CREAM} !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}
div[data-testid="stToolbar"] {{ visibility: hidden; }}

/*SCROLLBAR*/
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {SAND}40; border-radius: 6px; }}
::-webkit-scrollbar-thumb:hover {{ background: {SAND}80; }}

/*SIDEBAR*/

[data-testid="stSidebar"] {{
    background: {FOREST} !important;
    min-width: 290px !important;
    max-width: 290px !important;
    width: 290px !important;
    display: block !important;
    visibility: visible !important;
    transform: none !important;
    border-right: none !important;
}}

[data-testid="stSidebar"] > div:first-child {{
    background: {FOREST} !important;
    padding-top: 0 !important;
}}

[data-testid="stSidebarNav"] {{
    display: none !important;
}}

[data-testid="stSidebar"] * {{
    color: {WHITE} !important;
}}

.sidebar-shell {{
    padding: 22px 16px 18px 16px;
    border-bottom: 1px solid {WHITE}14;
    margin-bottom: 10px;
}}

.sidebar-brand {{
    display: flex;
    align-items: center;
    gap: 12px;
}}

.sidebar-icon {{
    width: 46px;
    height: 46px;
    border-radius: 13px;
    background: linear-gradient(135deg, {SAND}, {RUST});
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
    box-shadow: 0 6px 18px {RUST}35;
}}

.sidebar-copy {{
    display: flex;
    flex-direction: column;
}}

.sidebar-name {{
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    font-weight: 700;
    line-height: 1.05;
    color: {CREAM} !important;
}}

.sidebar-name span {{
    color: {SAND} !important;
}}

.sidebar-tag {{
    margin-top: 4px;
    font-size: 11px;
    color: {WHITE}55 !important;
    letter-spacing: 0.4px;
}}

[data-testid="stSidebar"] hr {{
    border-color: {WHITE}12 !important;
    margin: 10px 0 !important;
}}

[data-testid="stSidebar"] .stButton > button {{
    width: 100% !important;
    background: transparent !important;
    border: 1px solid {WHITE}15 !important;
    border-radius: 10px !important;
    color: {WHITE}85 !important;
    padding: 10px 14px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}}

[data-testid="stSidebar"] .stButton > button:hover {{
    background: {WHITE}10 !important;
    border-color: {SAND}50 !important;
    color: {CREAM} !important;
    transform: translateX(2px) !important;
}}

[data-testid="stSidebar"] .stButton > button:focus {{
    box-shadow: none !important;
}}

[data-testid="stSidebar"] .nav-active button {{
    background: linear-gradient(135deg, {SAND}28, {RUST}18) !important;
    border-color: {SAND}55 !important;
    color: {CREAM} !important;
}}

/*MAIN BLOCK*/
.block-container {{
    max-width: 900px !important;
    padding: 0 2rem 2rem !important;
}}

/*PAGE HEADER*/
.page-header {{
    background: {WHITE};
    border-bottom: 1px solid {MIST};
    padding: 16px 28px;
    margin: -1rem -2rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.page-title {{
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 700;
    color: {FOREST};
}}
.page-title span {{ color: {RUST}; }}

/*CARDS*/
.card {{
    background: {WHITE};
    border: 1.5px solid {SAND}28;
    border-radius: 14px;
    padding: 20px;
    transition: all 0.2s;
}}
.card:hover {{ border-color: {SAND}60; box-shadow: 0 6px 24px {SAND}18; }}
.card-accent {{
    background: linear-gradient(135deg, {CREAM}, {WHITE});
    border: 1.5px solid {SAND}35;
    border-radius: 14px;
    padding: 20px;
}}

/*METRIC CARDS*/
.metric-card {{
    background: {WHITE};
    border: 1.5px solid {SAND}28;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}}
.metric-value {{
    font-family: 'Playfair Display', serif;
    font-size: 32px;
    font-weight: 700;
    color: {RUST};
}}
.metric-label {{
    font-size: 12px;
    color: {SAGE};
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 2px;
}}

/*BUTTONS*/
.stButton > button {{
    background: {CREAM} !important;
    border: 1.5px solid {SAND}50 !important;
    color: {FOREST} !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 8px 18px !important;
    transition: all 0.2s !important;
}}
.stButton > button:hover {{
    border-color: {SAND} !important;
    background: {WHITE} !important;
    box-shadow: 0 4px 14px {SAND}25 !important;
    transform: translateY(-1px) !important;
}}
.stButton > button:active {{ transform: translateY(0) !important; }}

/* Primary button override via container class */
.btn-primary > .stButton > button {{
    background: linear-gradient(135deg, {SAND}, {RUST}) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px {RUST}35 !important;
}}
.btn-primary > .stButton > button:hover {{
    box-shadow: 0 6px 20px {RUST}50 !important;
    transform: translateY(-2px) !important;
}}

/*INPUTS*/
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {{
    background: {CREAM} !important;
    border: 1.5px solid {SAND}40 !important;
    border-radius: 10px !important;
    color: {FOREST} !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {{
    border-color: {SAND} !important;
    box-shadow: 0 0 0 3px {SAND}18 !important;
    outline: none !important;
}}

/*SELECT/SLIDER*/
.stSelectbox [data-baseweb="select"] {{
    background: {CREAM} !important;
    border-color: {SAND}40 !important;
    border-radius: 10px !important;
}}
.stSlider [data-baseweb="slider"] {{ accent-color: {SAND}; }}

/*FILE UPLOADER*/
[data-testid="stFileUploader"] {{
    background: {WHITE} !important;
    border: 2px dashed {SAND}50 !important;
    border-radius: 14px !important;
    padding: 8px !important;
    transition: border-color 0.2s !important;
}}
[data-testid="stFileUploader"]:hover {{ border-color: {SAND} !important; }}
[data-testid="stFileUploader"] label {{ color: {SAGE} !important; font-size: 14px !important; }}

/*CHAT*/
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stChatMessageContent {{
    background: {SAGE} !important;
    color: white !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 12px 16px !important;
    max-width: 78% !important;
    font-size: 14.5px !important;
    margin-left: auto !important;
    box-shadow: 0 3px 12px {SAGE}30 !important;
}}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stChatMessageContent {{
    background: {CREAM} !important;
    color: {FOREST} !important;
    border-radius: 18px 18px 18px 4px !important;
    border: 1px solid {SAND}22 !important;
    padding: 14px 18px !important;
    max-width: 82% !important;
    font-size: 14.5px !important;
    line-height: 1.65 !important;
}}
[data-testid="stChatInput"] textarea {{
    background: {CREAM} !important;
    border: 1.5px solid {SAND}40 !important;
    border-radius: 14px !important;
    color: {FOREST} !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}}
[data-testid="stChatInput"] textarea:focus {{
    border-color: {SAND} !important;
    box-shadow: 0 0 0 3px {SAND}18 !important;
}}
[data-testid="stChatInput"] button {{
    background: linear-gradient(135deg, {SAND}, {RUST}) !important;
    border-radius: 10px !important;
    border: none !important;
}}

/*RADIO (question options) */
.stRadio [data-testid="stMarkdownContainer"] p {{ font-size: 14.5px !important; color: {FOREST} !important; }}
.stRadio label {{ cursor: pointer !important; }}

/*PROGRESS*/
.stProgress > div > div {{ background: linear-gradient(90deg, {SAND}, {RUST}) !important; border-radius: 4px !important; }}

/*ALERTS*/
.stAlert {{ background: {CREAM} !important; border-radius: 10px !important; border-left-color: {SAND} !important; }}
.stSuccess {{ border-left-color: {SAGE} !important; background: #F0F4EC !important; }}
.stError {{ border-left-color: {RUST} !important; }}

/*EXPANDER*/
[data-testid="stExpander"] {{
    background: {WHITE} !important;
    border: 1.5px solid {SAND}28 !important;
    border-radius: 12px !important;
}}
[data-testid="stExpander"] summary {{ font-weight: 500 !important; }}

/*DIVIDER*/
hr {{ border-color: {MIST} !important; }}

/*SPINNER*/
.stSpinner > div {{ border-top-color: {SAND} !important; }}

/*TABS*/
.stTabs [data-baseweb="tab-list"] {{ background: transparent !important; gap: 4px !important; }}
.stTabs [data-baseweb="tab"] {{
    background: {CREAM} !important;
    border-radius: 8px 8px 0 0 !important;
    color: {SAGE} !important;
    font-weight: 500 !important;
    border-bottom: 2px solid transparent !important;
}}
.stTabs [aria-selected="true"] {{
    color: {RUST} !important;
    border-bottom-color: {RUST} !important;
    background: {WHITE} !important;
}}

/*CUSTOM COMPONENTS*/
.badge {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    line-height: 1.6;
}}
.badge-sand {{ background: {SAND}25; color: {RUST}; border: 1px solid {SAND}50; }}
.badge-sage {{ background: {SAGE}20; color: {SAGE}; border: 1px solid {SAGE}40; }}
.badge-forest {{ background: {FOREST}15; color: {FOREST}; border: 1px solid {FOREST}30; }}

.question-card {{
    background: {WHITE};
    border: 1.5px solid {SAND}28;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 16px;
    position: relative;
}}
.question-card .q-number {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: {SAND};
    margin-bottom: 8px;
}}
.question-card .q-text {{
    font-size: 16px;
    font-weight: 500;
    color: {FOREST};
    line-height: 1.5;
    margin-bottom: 16px;
}}
.question-card .q-topic {{
    font-size: 11px;
    color: {SAGE};
    background: {SAGE}15;
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-block;
}}

.result-card-excellent {{ background: linear-gradient(135deg, #F0F9F4, {WHITE}); border: 1.5px solid {SAGE}50; border-radius: 14px; padding: 20px; }}
.result-card-good {{ background: linear-gradient(135deg, {CREAM}, {WHITE}); border: 1.5px solid {SAND}60; border-radius: 14px; padding: 20px; }}
.result-card-needs-work {{ background: linear-gradient(135deg, #FFF8F5, {WHITE}); border: 1.5px solid {RUST}40; border-radius: 14px; padding: 20px; }}

.score-circle {{
    width: 110px; height: 110px;
    border-radius: 50%;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    margin: 0 auto 12px;
    font-family: 'Playfair Display', serif;
}}
.score-circle.excellent {{ background: conic-gradient({SAGE} 0%, {SAGE} var(--pct), #E8F0EC var(--pct)); box-shadow: 0 4px 20px {SAGE}30; }}
.score-circle.good {{ background: conic-gradient({SAND} 0%, {SAND} var(--pct), {CREAM} var(--pct)); box-shadow: 0 4px 20px {SAND}30; }}
.score-circle.poor {{ background: conic-gradient({RUST} 0%, {RUST} var(--pct), #FFF0EC var(--pct)); box-shadow: 0 4px 20px {RUST}20; }}

.upload-success-item {{
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px;
    background: {WHITE};
    border: 1px solid {SAND}30;
    border-radius: 10px;
    margin-bottom: 8px;
    font-size: 13.5px;
    color: {FOREST};
}}
.upload-success-item .file-icon {{ font-size: 18px; }}
.upload-success-item .file-name {{ font-weight: 500; flex: 1; }}
.upload-success-item .file-size {{ color: {SAGE}; font-size: 12px; }}
.upload-success-item .file-ok {{ color: {SAGE}; font-weight: 600; }}
</style>
"""

def sidebar_logo_html() -> str:
    return f"""
<div style="padding:22px 16px 16px;border-bottom:1px solid #FFFFFF14;margin-bottom:6px;">
    <div style="display:flex;align-items:center;gap:10px;">
        <div style="width:40px;height:40px;background:linear-gradient(135deg,{SAND},{RUST});border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:20px;box-shadow:0 4px 14px #BC6C2540;flex-shrink:0;">🌿</div>
        <div>
            <div style="font-family:'Playfair Display',serif;font-size:22px;font-weight:700;color:{CREAM};letter-spacing:-0.3px;line-height:1.1;">Prepo<span style="color:{SAND};">AI</span></div>
            <div style="font-size:10.5px;color:#FFFFFF45;letter-spacing:0.3px;">Interview Prep Assistant</div>
        </div>
    </div>
</div>
"""

def page_header_html(icon: str, title: str, subtitle: str = "") -> str:
    return f"""
<div style="background:{WHITE};border-bottom:1px solid {MIST};padding:16px 28px;margin:-1rem -2rem 1.5rem -2rem;">
    <div style="display:flex;align-items:center;gap:12px;">
        <span style="font-size:24px;">{icon}</span>
        <div>
            <div style="font-family:'Playfair Display',serif;font-size:22px;font-weight:700;color:{FOREST};">{title}</div>
            {"" if not subtitle else f'<div style="font-size:13px;color:{SAGE};margin-top:1px;">{subtitle}</div>'}
        </div>
    </div>
</div>
"""

def metric_html(value: str, label: str, color: str = None) -> str:
    c = color or RUST
    return f"""
<div style="background:{WHITE};border:1.5px solid {SAND}28;border-radius:12px;padding:16px;text-align:center;">
    <div style="font-family:'Playfair Display',serif;font-size:30px;font-weight:700;color:{c};">{value}</div>
    <div style="font-size:11.5px;color:{SAGE};text-transform:uppercase;letter-spacing:0.8px;margin-top:3px;">{label}</div>
</div>
"""
