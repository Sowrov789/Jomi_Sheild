import json
import pandas as pd
import streamlit as st
from data_logic import load_data, get_plot, get_findings, get_dashboard_stats, get_risk_level, search_plots
from chatbot import answer_question, gemini_ready

st.set_page_config(page_title="JOMI-SHIELD | জমি যাচাই সহায়ক", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Noto+Sans+Bengali:wght@400;500;600;700&display=swap');
:root{--green:#0c6b45;--green2:#16845a;--deep:#083c2b;--mint:#e9f6ef;--ink:#18332a;--muted:#64766e;--line:#dfe9e3;--gold:#d9a441;--bg:#f5f8f6}
html,body,[class*="css"],.stApp{font-family:'Hind Siliguri','Noto Sans Bengali',sans-serif;color:var(--ink)}
.stApp{background:var(--bg)}
.block-container{max-width:1440px;padding-top:.6rem;padding-bottom:2.6rem}
#MainMenu,footer{visibility:hidden}
[data-testid="stHeader"]{background:transparent}
[data-testid="stSidebar"]{background:#fff;border-right:1px solid var(--line)}
[data-testid="stSidebar"] section{padding-top:1rem}
.govbar{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;background:#073d2b;color:#e8f6ee;padding:8px 20px;border-radius:8px 8px 0 0;font-size:13px;letter-spacing:.1px}
.brandbar{background:#fff;border:1px solid var(--line);border-top:0;border-radius:0 0 14px 14px;padding:17px 22px;display:flex;align-items:center;justify-content:space-between;gap:18px;box-shadow:0 5px 18px rgba(10,60,39,.035)}
.brand-left{display:flex;align-items:center;gap:13px}.brand-mark{width:50px;height:50px;border-radius:15px;display:flex;align-items:center;justify-content:center;font-size:26px;color:#fff;background:linear-gradient(145deg,#0d7048,#0a4934);box-shadow:0 5px 14px #0c6b4533}
.brand-title{font-weight:700;color:#133b2b;font-size:22px;line-height:1.2}.brand-sub{font-size:13px;color:#728078;margin-top:4px}.brand-quick{display:flex;align-items:center;gap:10px;color:#50665a;font-size:13px}.live-dot{display:inline-block;width:8px;height:8px;background:#2ab673;border-radius:50%;margin-right:6px}
.hero{position:relative;overflow:hidden;margin-top:20px;border-radius:20px;padding:32px 34px;background:radial-gradient(circle at 88% 10%,#367c5a 0,#367c5a00 28%),linear-gradient(115deg,#083e2b 0%,#0d6a44 60%,#147950 100%);color:#fff;box-shadow:0 12px 30px #0a57381c}
.hero:after{content:' ';position:absolute;width:250px;height:250px;border-radius:50%;right:-65px;bottom:-145px;border:36px solid #ffffff12;pointer-events:none}
.hero-kicker{display:inline-block;background:#ffffff1c;border:1px solid #ffffff30;color:#d7f5e4;padding:5px 11px;border-radius:30px;font-size:13px;margin-bottom:14px}.hero h1{font-size:clamp(26px,3.3vw,39px);line-height:1.25;color:#fff;margin:0 0 12px;font-weight:700;max-width:760px}.hero p{font-size:17px;color:#e3f5e9;margin:0;max-width:760px;line-height:1.65}.hero-note{margin-top:19px;color:#dbf2e4;font-size:13px}
.section-title{font-size:23px;font-weight:700;color:#153b2b;margin:26px 0 5px}.section-subtitle{color:#6c7b73;font-size:14px;margin-bottom:15px}
.stat-card{background:#fff;border:1px solid var(--line);border-radius:15px;padding:17px 18px;min-height:122px;box-shadow:0 3px 12px #183d2a05}.stat-top{display:flex;justify-content:space-between;align-items:center;color:#64766e;font-size:13px}.stat-icon{width:38px;height:38px;display:inline-flex;align-items:center;justify-content:center;border-radius:12px;background:var(--mint);font-size:20px}.stat-value{font-size:30px;font-weight:700;color:#163b2b;margin-top:7px;line-height:1.25}.stat-foot{color:#86948d;font-size:12px;margin-top:5px}
.service-card{height:100%;min-height:152px;background:#fff;border:1px solid var(--line);border-radius:15px;padding:19px 18px;transition:all .2s}.service-icon{font-size:24px;width:45px;height:45px;border-radius:13px;background:#eaf6ee;display:flex;align-items:center;justify-content:center;margin-bottom:14px}.service-card h4{margin:0 0 5px;color:#193e2d;font-size:17px}.service-card p{margin:0;color:#6b7d73;font-size:13px;line-height:1.5}
.info-card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px 22px;margin-bottom:14px}.mini-tag{display:inline-block;border-radius:50px;font-size:12px;padding:4px 9px;background:#eef7f0;color:#126743}.notice{border-left:4px solid #d7a33d;background:#fff9e9;color:#71551d;padding:13px 16px;border-radius:7px;font-size:13px;line-height:1.6}
.plot-card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:15px 16px;margin-bottom:10px}.plot-id{font-weight:700;font-size:17px;color:#164b34}.muted{color:#718177;font-size:13px}.status-pill{display:inline-block;padding:4px 10px;border-radius:30px;font-weight:600;font-size:12px}.risk-high{color:#a32323;background:#fff0ef}.risk-medium{color:#8b5b08;background:#fff6df}.risk-low{color:#3a5a90;background:#edf4ff}.risk-clear{color:#126743;background:#e8f6ee}
.timeline{border-left:2px solid #cbe3d3;margin:7px 0 7px 8px;padding-left:18px}.timeline-item{position:relative;padding:0 0 18px 3px}.timeline-item:before{content:'';position:absolute;left:-26px;top:5px;width:12px;height:12px;border-radius:50%;background:#198354;border:3px solid #d9f0e2}.timeline-year{font-size:12px;color:#198354;font-weight:700}.timeline-title{font-weight:600;color:#1d4430}.timeline-note{font-size:13px;color:#738078}
div[data-testid="stRadio"]>label{display:none}div[role="radiogroup"]{gap:6px;flex-wrap:wrap}div[role="radiogroup"] label{background:#fff;border:1px solid var(--line);padding:8px 13px;border-radius:9px!important;color:#456052;font-weight:600;font-size:14px}div[role="radiogroup"] label:has(input:checked){background:#e8f5ed;border-color:#8dc8a5;color:#0a633f}
.stButton>button,.stDownloadButton>button{border-radius:9px;border:1px solid #c8ddd0;font-weight:600;min-height:42px}.stButton>button[kind="primary"]{background:#0c6b45;border-color:#0c6b45;color:white}.stButton>button:hover{border-color:#0c6b45;color:#0c6b45}
.stTextInput input,.stSelectbox div[data-baseweb="select"],.stTextArea textarea{border-radius:9px!important}

/* Chat UI: enforce light, high-contrast styling regardless of browser/Streamlit theme */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] form,
[data-testid="stChatInput"] [data-baseweb="textarea"],
[data-testid="stChatInput"] [data-baseweb="base-input"],
[data-testid="stChatInput"] textarea,
[data-testid="stChatInputTextArea"],
.stChatInput textarea {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #18332a !important;
    -webkit-text-fill-color: #18332a !important;
    caret-color: #0c6b45 !important;
    color-scheme: light !important;
}
[data-testid="stChatInput"] [data-baseweb="textarea"],
[data-testid="stChatInput"] [data-baseweb="base-input"] {
    border: 1px solid #bfd9ca !important;
    border-radius: 13px !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"] [data-baseweb="textarea"]:focus-within,
[data-testid="stChatInput"] [data-baseweb="base-input"]:focus-within {
    border-color: #16845a !important;
    box-shadow: 0 0 0 3px #16845a20 !important;
}
[data-testid="stChatInput"] textarea::placeholder,
[data-testid="stChatInputTextArea"]::placeholder,
.stChatInput textarea::placeholder {
    color: #7b8e84 !important;
    -webkit-text-fill-color: #7b8e84 !important;
    opacity: 1 !important;
}
[data-testid="stChatInput"] button,
[data-testid="stChatInputSubmitButton"] {
    background: #e9f6ef !important;
    background-color: #e9f6ef !important;
    color: #0c6b45 !important;
    border: 1px solid #c8e2d2 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"] button:hover,
[data-testid="stChatInputSubmitButton"]:hover {
    background: #d9eee2 !important;
    color: #075b3a !important;
    border-color: #16845a !important;
}
[data-testid="stChatInput"] button svg,
[data-testid="stChatInputSubmitButton"] svg {
    color: #0c6b45 !important;
    fill: #0c6b45 !important;
    stroke: #0c6b45 !important;
}
/* User and assistant messages: dark readable text on light cards */
[data-testid="stChatMessage"],
.stChatMessage {
    background-color: #ffffff !important;
    color: #18332a !important;
    border: 1px solid #e1ebe4 !important;
    border-radius: 13px !important;
    padding: 12px 14px !important;
    margin-bottom: 9px !important;
}
[data-testid="stChatMessage"] *,
.stChatMessage *,
[data-testid="stChatMessageContent"] *,
[data-testid="stMarkdownContainer"] {
    color: #18332a !important;
    -webkit-text-fill-color: #18332a !important;
}
[data-testid="stChatMessage"] a,
.stChatMessage a {
    color: #0c6b45 !important;
    -webkit-text-fill-color: #0c6b45 !important;
}
/* Default/secondary buttons: light green with a green outline */
.stButton > button:not([kind="primary"]),
.stDownloadButton > button:not([kind="primary"]),
[data-testid="stBaseButton-secondary"] {
    background: #e9eeec !important;
    background-color: #e9eeec !important;
    color: #087548 !important;
    -webkit-text-fill-color: #087548 !important;
    border: 1px solid #0c6b45 !important;
    border-radius: 12px !important;
    box-shadow: none !important;
}
.stButton > button:not([kind="primary"]):hover,
.stDownloadButton > button:not([kind="primary"]):hover,
[data-testid="stBaseButton-secondary"]:hover {
    background: #dce9e2 !important;
    background-color: #dce9e2 !important;
    color: #075b3a !important;
    border-color: #0c6b45 !important;
}
.stButton > button[kind="primary"],
[data-testid="stBaseButton-primary"] {
    background: #0c6b45 !important;
    background-color: #0c6b45 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border-color: #0c6b45 !important;
}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:12px;overflow:hidden}
.footer{background:#0a3d2b;color:#e0f1e6;border-radius:15px;padding:22px 24px;margin-top:28px}.footer a{color:#fff}.footer-small{color:#afd0bd;font-size:12px;margin-top:12px}
@media(max-width:800px){.brandbar{align-items:flex-start;flex-direction:column;padding:14px}.hero{padding:24px 20px}.hero p{font-size:15px}.brand-title{font-size:19px}.govbar{font-size:11px}.block-container{padding-left:1rem;padding-right:1rem}}

/* FINAL OVERRIDES: equal-height service cards and light, readable controls */
.service-card.main-service-card {
    box-sizing: border-box !important;
    height: 218px !important;
    min-height: 218px !important;
    max-height: 218px !important;
    width: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    border-radius: 16px !important;
}
.service-icon { flex: 0 0 45px !important; }
.main-service-card h4 {
    min-height: 2.56em !important;
    max-height: 2.56em !important;
    line-height: 1.28 !important;
    overflow: hidden !important;
}
.main-service-card p {
    display: -webkit-box !important;
    -webkit-box-orient: vertical !important;
    -webkit-line-clamp: 3 !important;
    overflow: hidden !important;
}

/* Force Streamlit secondary buttons to remain light instead of black */
.stApp { color-scheme: light !important; }
.stApp div[data-testid="stButton"] button:not([kind="primary"]),
.stApp div[data-testid="stDownloadButton"] button,
.stApp div[data-testid="stLinkButton"] a,
.stApp button[data-testid="stBaseButton-secondary"],
.stApp button[kind="secondary"],
.stApp button[kind="tertiary"] {
    background: #e9eeec !important;
    background-color: #e9eeec !important;
    color: #087548 !important;
    -webkit-text-fill-color: #087548 !important;
    border: 1px solid #0c6b45 !important;
    border-radius: 12px !important;
    box-shadow: none !important;
    min-height: 48px !important;
    font-weight: 600 !important;
    color-scheme: light !important;
}
.stApp div[data-testid="stButton"] button:not([kind="primary"]):hover,
.stApp div[data-testid="stDownloadButton"] button:hover,
.stApp div[data-testid="stLinkButton"] a:hover,
.stApp button[data-testid="stBaseButton-secondary"]:hover,
.stApp button[kind="secondary"]:hover,
.stApp button[kind="tertiary"]:hover {
    background: #dce9e2 !important;
    background-color: #dce9e2 !important;
    color: #075b3a !important;
    -webkit-text-fill-color: #075b3a !important;
    border-color: #0c6b45 !important;
}
.stApp div[data-testid="stButton"] button[kind="primary"],
.stApp button[data-testid="stBaseButton-primary"],
.stApp button[kind="primary"] {
    background: #0c6b45 !important;
    background-color: #0c6b45 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 1px solid #0c6b45 !important;
    border-radius: 12px !important;
    min-height: 48px !important;
    box-shadow: none !important;
}
.stApp div[data-testid="stButton"] button[kind="primary"]:hover,
.stApp button[data-testid="stBaseButton-primary"]:hover,
.stApp button[kind="primary"]:hover {
    background: #095a3a !important;
    background-color: #095a3a !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Chat composer: white surface with visible typed text and a light send button */
.stApp [data-testid="stChatInput"],
.stApp [data-testid="stChatInput"] form,
.stApp [data-testid="stChatInput"] div[data-baseweb="textarea"],
.stApp [data-testid="stChatInput"] div[data-baseweb="base-input"],
.stApp [data-testid="stChatInput"] textarea {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #18332a !important;
    -webkit-text-fill-color: #18332a !important;
    caret-color: #0c6b45 !important;
    color-scheme: light !important;
}
.stApp [data-testid="stChatInput"] div[data-baseweb="textarea"],
.stApp [data-testid="stChatInput"] div[data-baseweb="base-input"] {
    border: 1px solid #bfd9ca !important;
    border-radius: 13px !important;
    box-shadow: none !important;
}
.stApp [data-testid="stChatInput"] textarea::placeholder {
    color: #7b8e84 !important;
    -webkit-text-fill-color: #7b8e84 !important;
    opacity: 1 !important;
}
.stApp [data-testid="stChatInput"] button,
.stApp [data-testid="stChatInputSubmitButton"] {
    background: #e9f6ef !important;
    background-color: #e9f6ef !important;
    color: #0c6b45 !important;
    -webkit-text-fill-color: #0c6b45 !important;
    border: 1px solid #c8e2d2 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
    min-height: 40px !important;
}
.stApp [data-testid="stChatInput"] button svg,
.stApp [data-testid="stChatInputSubmitButton"] svg {
    color: #0c6b45 !important;
    fill: #0c6b45 !important;
    stroke: #0c6b45 !important;
}

/* Chat message cards: high-contrast dark text on white */
.stApp [data-testid="stChatMessage"] {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #18332a !important;
    border: 1px solid #e1ebe4 !important;
    border-radius: 13px !important;
    padding: 12px 14px !important;
    margin-bottom: 9px !important;
    color-scheme: light !important;
}
.stApp [data-testid="stChatMessage"] *,
.stApp [data-testid="stChatMessageContent"] *,
.stApp [data-testid="stChatMessage"] p,
.stApp [data-testid="stChatMessage"] li,
.stApp [data-testid="stChatMessage"] strong,
.stApp [data-testid="stChatMessage"] em {
    color: #18332a !important;
    -webkit-text-fill-color: #18332a !important;
}
.stApp [data-testid="stChatMessage"] a {
    color: #0c6b45 !important;
    -webkit-text-fill-color: #0c6b45 !important;
}


/* HERO TEXT CONTRAST FIX: keep all hero text bright on the green gradient */
.stApp .hero,
.stApp .hero .hero-kicker,
.stApp .hero h1,
.stApp .hero p,
.stApp .hero .hero-note,
.stApp .hero h1 span {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    opacity: 1 !important;
}
.stApp .hero .hero-kicker {
    color: #d7f5e4 !important;
    -webkit-text-fill-color: #d7f5e4 !important;
}
.stApp .hero p {
    color: #e3f5e9 !important;
    -webkit-text-fill-color: #e3f5e9 !important;
}
.stApp .hero .hero-note,
.stApp .hero .hero-note span {
    color: #dbf2e4 !important;
    -webkit-text-fill-color: #dbf2e4 !important;
}

/* Footer text contrast fix */
.stApp .footer,
.stApp .footer * {
    color: #e0f1e6 !important;
    -webkit-text-fill-color: #e0f1e6 !important;
}

.stApp .footer > div:first-child {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

.stApp .footer .footer-small {
    color: #afd0bd !important;
    -webkit-text-fill-color: #afd0bd !important;
}

.stApp .footer a {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    text-decoration: underline;
}

</style>
""", unsafe_allow_html=True)

data = load_data()
plots = data.get("plots", [])
if not plots:
    st.error("ডেমো ডেটাসেট লোড করা যায়নি। data/demo_data.json ফাইলটি পরীক্ষা করুন।")
    st.stop()

# Persistent navigation and current demo plot selection.
if "page" not in st.session_state: st.session_state.page = "ড্যাশবোর্ড"
if "selected_plot_id" not in st.session_state: st.session_state.selected_plot_id = "JP-1001"
if "chat_history" not in st.session_state: st.session_state.chat_history = []

def jump_to(page, plot_id=None):
    # Button callbacks run before the next rerun, so updating navigation/widget
    # state here is safe and keeps the sidebar selector synchronized.
    st.session_state.page = page
    if plot_id:
        st.session_state.selected_plot_id = plot_id
        if "sidebar_plot_pick" in st.session_state:
            st.session_state.sidebar_plot_pick = plot_id

def key_exists():
    try: return bool(st.secrets.get("GEMINI_API_KEY", ""))
    except Exception: return False

# Government-portal-inspired structure, but clearly marked as an independent demo.
st.markdown("""
<div class="govbar"><span>বাংলা ভূমি তথ্য ও প্রাক-ক্রয় যাচাই সহায়ক</span><span>শিক্ষামূলক ডেমো · সরকারি ওয়েবসাইট নয়</span></div>
<div class="brandbar"><div class="brand-left"><div class="brand-mark">🛡️</div><div><div class="brand-title">জমি-শিল্ড <span style="color:#0c6b45">JOMI-SHIELD</span></div><div class="brand-sub">জমি কেনার আগে তথ্য বুঝুন, সম্ভাব্য অসংগতি শনাক্ত করুন</div></div></div><div class="brand-quick"><span><span class="live-dot"></span>ডেমো সিস্টেম প্রস্তুত</span><span style="color:#c7d8cd">|</span><a style="color:#0c6b45;text-decoration:none;font-weight:700" href="https://land.gov.bd/" target="_blank">সরকারি ভূমিসেবা ↗</a></div></div>
""", unsafe_allow_html=True)

pages = ["ড্যাশবোর্ড", "জমির প্রোফাইল", "ঝুঁকি বিশ্লেষণ", "AI সহায়ক", "যাচাই প্রতিবেদন", "ব্যবহার নির্দেশিকা"]
st.radio("প্রধান মেনু", pages, key="page", horizontal=True, label_visibility="collapsed")

with st.sidebar:
    st.markdown("### 🧭 দ্রুত প্রবেশ")
    plot_options = [p["plot_id"] for p in plots]
    current_index = plot_options.index(st.session_state.selected_plot_id) if st.session_state.selected_plot_id in plot_options else 0
    picked = st.selectbox("নমুনা জমি নির্বাচন করুন", plot_options, index=current_index, key="sidebar_plot_pick")
    st.session_state.selected_plot_id = picked
    selected = get_plot(data, picked)
    findings = get_findings(data, picked)
    st.markdown(f"<div class='info-card' style='padding:13px'><div class='muted'>নির্বাচিত ডেমো জমি</div><div class='plot-id'>{selected['plot_id']}</div><div class='muted'>দাগ {selected['dag_no']} · খতিয়ান {selected['khatian_no']}</div><div style='margin-top:9px'><span class='status-pill {get_risk_level(findings)[1]}'>{get_risk_level(findings)[0]}</span></div></div>", unsafe_allow_html=True)
    

    st.link_button("সরকারি ভূমি পোর্টাল খুলুন", "https://land.gov.bd/", use_container_width=True)

selected = get_plot(data, st.session_state.selected_plot_id)
findings = get_findings(data, selected["plot_id"])
stats = get_dashboard_stats(data)

# Common view helpers.
def section_title(title, subtitle=None):
    st.markdown(f'<div class="section-title">{title}</div>' + (f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ''), unsafe_allow_html=True)

def risk_badge(findings_arg):
    label, cls = get_risk_level(findings_arg)
    return f'<span class="status-pill {cls}">{label}</span>'

def show_findings(items):
    if not items:
        st.success("এই ডেমো রেকর্ডে সেট করা নিয়ম অনুযায়ী কোনো সতর্কতা পাওয়া যায়নি। এটি আইনগত নিরাপত্তা বা মালিকানার নিশ্চয়তা নয়।")
        return
    for f in items:
        contents = f"**{f['title']}**  \n{f['details']}  \n\n**প্রস্তাবিত পরবর্তী ধাপ:** {f['action']}"
        if f["severity"] == "উচ্চ": st.error("🔴 " + contents)
        elif f["severity"] == "মাঝারি": st.warning("🟠 " + contents)
        else: st.info("🔵 " + contents)

def plot_table_rows(row_plots, key_prefix):
    for p in row_plots:
        pfind = get_findings(data, p["plot_id"])
        with st.container(border=True):
            c1,c2,c3,c4 = st.columns([1.25,1.7,1.1,1.25])
            c1.markdown(f"<div class='plot-id'>{p['plot_id']}</div><div class='muted'>দাগ: {p['dag_no']}</div>", unsafe_allow_html=True)
            c2.markdown(f"**{p['district']} · {p['upazila']}**<div class='muted'>খতিয়ান {p['khatian_no']} · {p['area_decimal']} শতক</div>", unsafe_allow_html=True)
            c3.markdown(risk_badge(pfind), unsafe_allow_html=True)
            c4.button("বিস্তারিত দেখুন ↗", key=f"{key_prefix}_{p['plot_id']}", use_container_width=True,
                      on_click=jump_to, args=("জমির প্রোফাইল", p["plot_id"]))

def plot_report(p, pfind):
    return {
        "project": "JOMI-SHIELD educational demo", "plot_id": p["plot_id"], "dag_no": p["dag_no"],
        "khatian_no": p["khatian_no"], "area_decimal": p["area_decimal"], "district": p["district"],
        "mutation_status": p["mutation_status"], "tax_status": p["tax_status"], "case_status": p["case_status"],
        "findings": pfind,
        "disclaimer": "Fictional demo data only. Not official land verification or legal advice."
    }

if st.session_state.page == "ড্যাশবোর্ড":
    st.markdown("""
    <div class="hero"><div class="hero-kicker">জমি কেনার আগে যাচাই করুন</div><h1>ভূমির তথ্য এক জায়গায়,<br>সিদ্ধান্তের আগে সচেতন যাচাই</h1><p>জমির ডেমো প্রোফাইল, দলিলের তথ্য, নামজারির অবস্থা ও সম্ভাব্য অসংগতি সহজ বাংলায় বুঝুন। তথ্য গুছিয়ে দেখা সহজ করুন—কিন্তু চূড়ান্ত আইনি সিদ্ধান্ত নিন অফিসিয়াল যাচাইয়ের পর।</p><div class="hero-note">✓ JOMI-PASS ডিজিটাল প্রোফাইল &nbsp; · &nbsp; ✓ JOMI-SHIELD নিয়মভিত্তিক সতর্কতা &nbsp; · &nbsp; ✓ ঐচ্ছিক AI সহায়ক</div></div>
    """, unsafe_allow_html=True)
    section_title("দ্রুত জমি খুঁজুন", "প্লট আইডি, দাগ নম্বর, খতিয়ান নম্বর বা দলিল আইডি দিয়ে এই ডেমো ডেটাসেটে অনুসন্ধান করুন।")
    with st.form("portal_search", clear_on_submit=False):
        colq, colbtn = st.columns([5,1])
        query = colq.text_input("অনুসন্ধান", placeholder="যেমন: JP-1018, DAG-621, KHT-300, DEMO-D-050", label_visibility="collapsed")
        submitted = colbtn.form_submit_button("🔎 খুঁজুন", type="primary", use_container_width=True)
    if submitted:
        matches = search_plots(data, query)
        st.session_state.search_matches = [m["plot_id"] for m in matches]
        st.session_state.search_query_done = query
    if "search_matches" in st.session_state and st.session_state.get("search_query_done"):
        matches = [get_plot(data, pid) for pid in st.session_state.search_matches]
        section_title(f"অনুসন্ধানের ফলাফল · {len(matches)}টি রেকর্ড")
        if matches:
            plot_table_rows(matches, "search")
        else: st.info("কোনো মিল পাওয়া যায়নি। ডেমো আইডি/দাগ/খতিয়ান নম্বর আবার পরীক্ষা করুন।")
        if st.button("অনুসন্ধান মুছুন", key="clear_search"):
            st.session_state.search_matches=[]; st.session_state.search_query_done=""; st.rerun()
    section_title("ডেমো ডেটার সারসংক্ষেপ", "এই সংখ্যাগুলো কেবল এই প্রজেক্টে রাখা কাল্পনিক রেকর্ডের ওপর ভিত্তি করে।")
    stat_defs=[("মোট ডেমো জমি",stats["plots"],"▦","তথ্যভান্ডারের নমুনা প্লট"),("দলিল রেকর্ড",stats["deeds"],"▤","কাল্পনিক ডেমো দলিল"),("সতর্কতাযুক্ত প্লট",stats["flagged"],"⚑","নিয়মে অন্তত একটি সতর্কতা"),("চলমান নামজারি",stats["pending_mutations"],"↻","ডেমোতে চলমান হিসেবে চিহ্নিত")]
    cols=st.columns(4)
    for c,(label,value,icon,foot) in zip(cols,stat_defs):
        c.markdown(f'<div class="stat-card"><div class="stat-top"><span>{label}</span><span class="stat-icon">{icon}</span></div><div class="stat-value">{value}</div><div class="stat-foot">{foot}</div></div>',unsafe_allow_html=True)
    section_title("ভূমি তথ্যের প্রধান অংশ", "একটি জমি সম্পর্কে প্রাসঙ্গিক তথ্য একত্রে দেখার জন্য তৈরি করা হয়েছে।")
    services=[("📚","ডিজিটাল জমির প্রোফাইল","দাগ, খতিয়ান, জমির পরিমাণ, দলিল ও কাল্পনিক ইতিহাস","জমির প্রোফাইল"),("🛡️","ঝুঁকি ও অসংগতি যাচাই","দলিলের দ্বৈত এন্ট্রি, পরিমাণে অমিল ও যাচাই-বাকি তথ্য","ঝুঁকি বিশ্লেষণ"),("🤖","বাংলা AI সহায়ক","নিয়মভিত্তিক সতর্কতার অর্থ ও পরবর্তী যাচাইয়ের ধাপ বুঝুন","AI সহায়ক"),("📋","প্রাক-ক্রয় যাচাই প্রতিবেদন","পাওয়া তথ্য, সতর্কতা ও সীমাবদ্ধতার সারাংশ ডাউনলোড করুন","যাচাই প্রতিবেদন")]
    cols=st.columns(4)
    for c,(icon,title,desc,page) in zip(cols,services):
        with c:
            st.markdown(f'<div class="service-card main-service-card"><div class="service-icon">{icon}</div><h4>{title}</h4><p>{desc}</p></div>',unsafe_allow_html=True)
            st.button("খুলুন ↗",key="service_"+page,use_container_width=True,on_click=jump_to,args=(page,))
    section_title("যে বিষয়গুলো মিলিয়ে দেখা দরকার", "সরকারি ভূমিসেবায় প্রাসঙ্গিক হতে পারে এমন চারটি তথ্য-শ্রেণি—এই অ্যাপে এগুলো শুধু ডেমো তথ্য হিসেবে দেখানো হয়।")
    topics=[("🔄","নামজারি","আবেদনের অবস্থা ও রেকর্ড"),("৳","ভূমি উন্নয়ন কর","রসিদ ও পরিশোধের তথ্য"),("🗺️","রেকর্ড ও ম্যাপ","দাগ, খতিয়ান ও জমির পরিমাণ"),("⚖️","মামলা ও অধিগ্রহণ","প্রযোজ্য হলে অবস্থা যাচাই")]
    cols=st.columns(4)
    for c,(icon,title,desc) in zip(cols,topics):
        c.markdown(f'<div class="service-card" style="min-height:118px"><div style="font-size:21px;margin-bottom:9px">{icon}</div><h4>{title}</h4><p>{desc}</p></div>',unsafe_allow_html=True)
    section_title("সাম্প্রতিক নমুনা প্লট", "নমুনা তালিকা থেকে বিস্তারিত প্রোফাইল খুলুন।")
    district_choice=st.selectbox("জেলা অনুযায়ী ফিল্টার", ["সব জেলা"]+sorted({p["district"] for p in plots}), key="dashboard_district")
    risk_choice=st.selectbox("সতর্কতার অবস্থা", ["সব অবস্থা","উচ্চ সতর্কতা","মাঝারি সতর্কতা","কম সতর্কতা","সেট করা সতর্কতা নেই"],key="dashboard_risk")
    filtered=[]
    for p in plots:
        pf=get_findings(data,p["plot_id"]); lab,_=get_risk_level(pf)
        if district_choice!="সব জেলা" and p["district"]!=district_choice: continue
        if risk_choice!="সব অবস্থা" and lab!=risk_choice: continue
        filtered.append(p)
    per_page=5
    pages_count=max(1,(len(filtered)+per_page-1)//per_page)
    current_page=st.selectbox("পাতা",list(range(1,pages_count+1)),key="dashboard_page")
    plot_table_rows(filtered[(current_page-1)*per_page:current_page*per_page],"dash")

elif st.session_state.page == "জমির প্রোফাইল":
    p=selected; pf=findings
    st.markdown(f'<div class="hero"><div class="hero-kicker">JOMI-PASS · ডিজিটাল জমির প্রোফাইল</div><h1>{p["plot_id"]} <span style="font-size:17px;font-weight:500">/ কাল্পনিক ডেমো রেকর্ড</span></h1><p>{p["district"]} জেলা · {p["upazila"]} উপজেলা · {p["mouza"]} · {p["land_type"]} জমি</p><div class="hero-note">{risk_badge(pf)} &nbsp; <span style="color:#e4f5e9">দাগ {p["dag_no"]} · খতিয়ান {p["khatian_no"]}</span></div></div>',unsafe_allow_html=True)
    cols=st.columns(4)
    for c,(label,val,icon) in zip(cols,[("জমির পরিমাণ",f"{p['area_decimal']} শতক","📐"),("নামজারির অবস্থা",p["mutation_status"],"🔄"),("ভূমি উন্নয়ন কর",p["tax_status"],"৳"),("রেকর্ডের অবস্থা",p["record_status"],"📄")]):
        c.markdown(f'<div class="stat-card"><div class="stat-top">{label}<span class="stat-icon">{icon}</span></div><div style="font-size:20px;font-weight:700;margin-top:12px;color:#173b2b">{val}</div><div class="stat-foot">শুধু ডেমো তথ্য</div></div>',unsafe_allow_html=True)
    section_title("মৌলিক তথ্য", "এই প্রোফাইলের সমস্ত তথ্য কাল্পনিক এবং কোনো সরকারি উৎস থেকে যাচাই করা নয়।")
    c1,c2=st.columns([1.15,1])
    with c1:
        st.markdown('<div class="info-card"><h4>📍 জমির পরিচিতি</h4>',unsafe_allow_html=True)
        st.write(f"**প্লট আইডি:** {p['plot_id']}")
        st.write(f"**দাগ নম্বর:** {p['dag_no']}")
        st.write(f"**খতিয়ান নম্বর:** {p['khatian_no']}")
        st.write(f"**জেলা / উপজেলা:** {p['district']} / {p['upazila']}")
        st.write(f"**মৌজা:** {p['mouza']}")
        st.write(f"**জমির ধরন:** {p['land_type']}")
        st.markdown('</div>',unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="info-card"><h4>🗂️ অন্যান্য যাচাইয়ের অবস্থা</h4>',unsafe_allow_html=True)
        st.write(f"**মামলা-সংক্রান্ত তথ্য:** {p['case_status']}")
        st.write(f"**অধিগ্রহণ/খাস-সংক্রান্ত তথ্য:** {p['acquisition_status']}")
        st.write(f"**খাজনা/কর তথ্য:** {p['tax_status']}")
        st.write(f"**তথ্যের ধরন:** কাল্পনিক নমুনা")
        st.markdown('</div>',unsafe_allow_html=True)
    section_title("মালিকানা ইতিহাসের টাইমলাইন", "এটি উদাহরণভিত্তিক মালিকানা ইতিহাস; আইনগত মালিকানার প্রমাণ নয়।")
    timeline='<div class="info-card"><div class="timeline">'
    for h in p["ownership_history"]:
        timeline+=f'<div class="timeline-item"><div class="timeline-year">{h["year"]}</div><div class="timeline-title">{h["owner_label"]}</div><div class="timeline-note">রেফারেন্স: {h["source"]} · {h["note"]}</div></div>'
    timeline+='</div></div>'
    st.markdown(timeline,unsafe_allow_html=True)
    section_title("সম্পর্কিত ডেমো দলিল")
    deed_frame=pd.DataFrame(p["deeds"])
    deed_frame=deed_frame.rename(columns={"deed_id":"দলিল আইডি","year":"বছর","owner_label":"কাল্পনিক দাবিদার","status":"অবস্থা","area_decimal":"দলিলের পরিমাণ (শতক)","note":"মন্তব্য"})
    st.dataframe(deed_frame,use_container_width=True,hide_index=True)
    section_title("JOMI-SHIELD-এর সতর্কতা")
    show_findings(pf)
    st.button("এই জমির যাচাই প্রতিবেদন তৈরি করুন",type="primary",on_click=jump_to,args=("যাচাই প্রতিবেদন",p["plot_id"]))

elif st.session_state.page == "ঝুঁকি বিশ্লেষণ":
    st.markdown('<div class="hero"><div class="hero-kicker">JOMI-SHIELD · ব্যাখ্যাযোগ্য নিয়মভিত্তিক পরীক্ষা</div><h1>সম্ভাব্য অসংগতি ও সতর্কতা</h1><p>ডেমো রেকর্ডে নির্ধারিত নিয়মের সঙ্গে মেলানো ফলাফল। এটি জালিয়াতি নির্ধারণ বা আইনগত মালিকানা যাচাই করে না।</p></div>',unsafe_allow_html=True)
    section_title("সতর্কতা তালিকা", "প্রতিটি সতর্কতার পাশে কারণ এবং কী যাচাই করা যেতে পারে তা দেখানো হয়।")
    severity_filter=st.selectbox("সতর্কতার মাত্রা",["সব মাত্রা","উচ্চ","মাঝারি","কম"])
    only_flagged=st.checkbox("শুধু সতর্কতাযুক্ত প্লট দেখান",value=True)
    visible=[]
    for p in plots:
        fs=get_findings(data,p["plot_id"]); lab,_=get_risk_level(fs)
        if only_flagged and not fs: continue
        if severity_filter!="সব মাত্রা" and not any(f["severity"]==severity_filter for f in fs): continue
        visible.append((p,fs))
    st.caption(f"ফিল্টারের সঙ্গে মিলেছে {len(visible)}টি প্লট")
    for p,fs in visible:
        label,cls=get_risk_level(fs)
        with st.container(border=True):
            a,b=st.columns([4,1])
            a.markdown(f"### {p['plot_id']} · {p['district']} জেলা")
            a.caption(f"দাগ {p['dag_no']} · খতিয়ান {p['khatian_no']} · {p['area_decimal']} শতক")
            b.markdown(risk_badge(fs),unsafe_allow_html=True)
            if fs:
                for f in fs:
                    color="🔴" if f["severity"]=="উচ্চ" else "🟠" if f["severity"]=="মাঝারি" else "🔵"
                    st.markdown(f"**{color} {f['title']}** — {f['details']}")
                    st.caption("পরবর্তী ধাপ: "+f["action"])
            else: st.caption("সেট করা নিয়মে কোনো সতর্কতা পাওয়া যায়নি।")
            st.button("প্রোফাইল খুলুন",key="risk_profile_"+p["plot_id"],on_click=jump_to,args=("জমির প্রোফাইল",p["plot_id"]))

elif st.session_state.page == "AI সহায়ক":
    p=selected; pf=findings
    st.markdown('<div class="hero"><div class="hero-kicker">এআই ভূমি সহায়ক · ঐচ্ছিক Gemini</div><h1>বাংলায় জমির তথ্য বুঝে নিন</h1><p>নির্বাচিত ডেমো প্লটের তথ্য ও JOMI-SHIELD-এর rule-based findings ব্যাখ্যা করুন। AI আইনি সিদ্ধান্ত দেয় না।</p></div>',unsafe_allow_html=True)
    section_title("বর্তমান প্রসঙ্গ", "একটি ডেমো জমি নির্বাচন করুন; chatbot সেই রেকর্ডের তথ্য নিয়েই উত্তর দেবে।")
    st.markdown(f'<div class="info-card"><div class="muted">নির্বাচিত প্লট</div><div class="plot-id">{p["plot_id"]} · {p["district"]}</div><div style="margin-top:7px">{risk_badge(pf)}</div><div class="muted" style="margin-top:8px">দাগ {p["dag_no"]} · খতিয়ান {p["khatian_no"]} · {len(p["deeds"])}টি ডেমো দলিল</div></div>',unsafe_allow_html=True)
    colleft,colright=st.columns([1.3,1])
    with colright:
        st.markdown('<div class="info-card"><h4>💡 কী প্রশ্ন করতে পারেন?</h4><p>• এই সতর্কতার কারণ কী?<br>• নামজারি “চলমান” মানে কী?<br>• কোন তথ্যগুলো যাচাই করা বাকি?<br>• জমি কেনার আগে কী কী নথি দেখা দরকার?</p></div>',unsafe_allow_html=True)
        
        st.caption("AI input-এ শুধু synthetic demo record পাঠানো হয়।")
    with colleft:
        st.markdown('<div class="info-card"><h4>💬 কথোপকথন</h4>',unsafe_allow_html=True)
        hist=[m for m in st.session_state.chat_history if m.get("plot_id")==p["plot_id"]]
        for msg in hist:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])
        question=st.chat_input("আপনার প্রশ্ন বাংলায় লিখুন…")
        if question:
            st.session_state.chat_history.append({"role":"user","content":question,"plot_id":p["plot_id"]})
            with st.chat_message("user"): st.markdown(question)
            with st.chat_message("assistant"):
                with st.spinner("তথ্য ব্যাখ্যা করা হচ্ছে…"):
                    answer=answer_question(question,p,pf)
                st.markdown(answer)
            st.session_state.chat_history.append({"role":"assistant","content":answer,"plot_id":p["plot_id"]})
        if st.button("কথোপকথন মুছুন",key="clear_chat"): st.session_state.chat_history=[]; st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

elif st.session_state.page == "যাচাই প্রতিবেদন":
    p=selected; pf=findings
    st.markdown('<div class="hero"><div class="hero-kicker">প্রাক-ক্রয় যাচাই সারাংশ</div><h1>প্রাক-ক্রয় যাচাই প্রতিবেদন</h1><p>ডেমো রেকর্ডে কী তথ্য রয়েছে, কী সতর্কতা পাওয়া গেছে এবং কোন বিষয় যাচাই করা দরকার—তার সংক্ষিপ্ত সারাংশ।</p></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="info-card"><div style="display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap"><div><div class="muted">রিপোর্ট আইডি</div><div class="plot-id">DEMO-REPORT-{p["plot_id"]}</div></div><div>{risk_badge(pf)}</div></div><hr style="border:0;border-top:1px solid #e2ebe5"><div class="muted">কাল্পনিক লোকেশন</div><h3>{p["district"]} · {p["upazila"]} · {p["mouza"]}</h3><div class="muted">প্লট {p["plot_id"]} · দাগ {p["dag_no"]} · খতিয়ান {p["khatian_no"]} · {p["area_decimal"]} শতক</div></div>',unsafe_allow_html=True)
    section_title("১. ডেমোতে পাওয়া তথ্য")
    cols=st.columns(4)
    for c,(l,v) in zip(cols,[("রেকর্ড",p["record_status"]),("নামজারি",p["mutation_status"]),("খাজনা তথ্য",p["tax_status"]),("মামলার তথ্য",p["case_status"])]): c.metric(l,v)
    section_title("২. শনাক্ত সতর্কতা")
    show_findings(pf)
    section_title("৩. কেনার আগে করণীয়")
    st.markdown("""
    <div class="info-card"><p>☐ মূল দলিল ও পূর্ববর্তী দলিলের ধারাবাহিকতা যাচাই করুন।</p><p>☐ দাগ, খতিয়ান, জমির পরিমাণ ও নামজারির তথ্য মিলিয়ে দেখুন।</p><p>☐ প্রযোজ্য ক্ষেত্রে ভূমি উন্নয়ন করের রসিদ, মামলা এবং অধিগ্রহণ-সংক্রান্ত তথ্য যাচাই করুন।</p><p>☐ প্রয়োজনে উপযুক্ত ভূমি কর্মকর্তা বা আইনজীবীর সহায়তা নিন।</p></div>
    <div class="notice"><b>সতর্কতা:</b> এই প্রতিবেদন কাল্পনিক ডেটার ওপর তৈরি। নির্ধারিত সতর্কতা না থাকলেও জমির মালিকানা বা আইনগত নিরাপত্তা প্রমাণিত হয় না।</div>
    """,unsafe_allow_html=True)
    report=plot_report(p,pf)
    c1,c2=st.columns(2)
    c1.download_button("⬇️ JSON প্রতিবেদন ডাউনলোড",json.dumps(report,ensure_ascii=False,indent=2),file_name=f"{p['plot_id']}_verification_demo.json",mime="application/json",use_container_width=True)
    csv=pd.DataFrame([{"plot_id":p["plot_id"],"district":p["district"],"dag_no":p["dag_no"],"khatian_no":p["khatian_no"],"area_decimal":p["area_decimal"],"risk_level":get_risk_level(pf)[0],"finding_count":len(pf)}]).to_csv(index=False).encode("utf-8-sig")
    c2.download_button("⬇️ CSV সারাংশ ডাউনলোড",csv,file_name=f"{p['plot_id']}_summary.csv",mime="text/csv",use_container_width=True)

else: # Help and limitations
    st.markdown('<div class="hero"><div class="hero-kicker">ব্যবহার নির্দেশিকা</div><h1>JOMI-SHIELD কী করে—আর কী করে না</h1><p>জমি সম্পর্কে প্রাসঙ্গিক তথ্য খুঁজে দেখা ও সম্ভাব্য অসংগতি বোঝার জন্য একটি শিক্ষামূলক প্রোটোটাইপ।</p></div>',unsafe_allow_html=True)
    section_title("প্রস্তাবিত ব্যবহারের ধাপ")
    steps=[("১","ডেমো প্লট খুঁজুন","প্লট আইডি, দাগ বা খতিয়ান ব্যবহার করে ২০টি কাল্পনিক রেকর্ডের মধ্যে অনুসন্ধান করুন।"),("২","JOMI-PASS দেখুন","প্লটের প্রোফাইল, দলিল এবং মালিকানা ইতিহাসের ডেমো টাইমলাইন পড়ুন।"),("৩","JOMI-SHIELD-এর সতর্কতা বুঝুন","প্রতিটি warning-এর কারণ ও পরবর্তী যাচাইয়ের পরামর্শ দেখুন।"),("৪","AI সহায়ককে প্রশ্ন করুন","Gemini key থাকলে নির্বাচিত ডেমো প্লটের তথ্য সহজ বাংলায় ব্যাখ্যা করতে বলুন।"),("৫","সারাংশ ডাউনলোড করুন","ডেমো যাচাই প্রতিবেদন JSON বা CSV হিসেবে সংরক্ষণ করুন।")]
    for n,title,desc in steps:
        with st.container(border=True):
            a,b=st.columns([.45,5]); a.markdown(f'<div class="stat-icon">{n}</div>',unsafe_allow_html=True); b.markdown(f"**{title}**  \n{desc}")
    section_title("সিস্টেমের সীমাবদ্ধতা")
    st.markdown("""
    <div class="info-card"><p>✅ <b>কী করে:</b> স্থানীয় JSON-এ থাকা কাল্পনিক রেকর্ড অনুসন্ধান, কয়েকটি স্বচ্ছ rule-based check, সতর্কতার কারণ দেখানো এবং প্রাসঙ্গিক সারাংশ তৈরি।</p><p>❌ <b>কী করে না:</b> সরকারি রেকর্ডে প্রবেশ, দলিল যাচাই, প্রকৃত মালিকানা নির্ধারণ, জালিয়াতির চূড়ান্ত সিদ্ধান্ত, বা সরকারি আইনগত সনদ প্রদান।</p><p>🔒 <b>গোপনীয়তা:</b> শুধু কাল্পনিক ডেটা ব্যবহার করুন। Gemini key গোপন রাখুন এবং কখনো GitHub-এ commit করবেন না।</p></div>
    """,unsafe_allow_html=True)
    section_title("সরকারি সেবা")
    st.markdown("সরকারি ভূমি সেবা বা অফিসিয়াল তথ্যের জন্য সরাসরি [land.gov.bd](https://land.gov.bd/) ভিজিট করুন। এই ডেমো অ্যাপটি সরকারি সাইটের সঙ্গে সংযুক্ত নয় এবং কোনো সরকারি অনুমোদনের দাবি করে না।")

st.markdown("""
<div class="footer"><div style="font-size:19px;font-weight:700">🛡️ জমি-শিল্ড · JOMI-SHIELD</div><div style="margin-top:7px;line-height:1.7">জমি কেনার আগে তথ্য বুঝতে সহায়ক একটি শিক্ষামূলক প্রোটোটাইপ। এটি সরকারি ভূমি সেবা পোর্টাল নয়।</div><div class="footer-small">সব ডেটা কাল্পনিক · Rule-based alerts are illustrative only · AI output may be inaccurate · সরকারি তথ্যের জন্য <a href="https://land.gov.bd/" target="_blank">land.gov.bd</a> ব্যবহার করুন।</div></div>
""", unsafe_allow_html=True)
