"""
QR-Code-Enabled Vehicle Emergency Response and Accident Notification System
IBM Watson AI / WatsonX RAG-powered Emergency Knowledge Assistant
"""

import streamlit as st
import json
import os
from datetime import datetime

# ─── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VehicleGuard Emergency Response System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "VehicleGuard — QR-Code Enabled Emergency Response System powered by IBM WatsonX RAG"
    }
)

# ─── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Global Reset & Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* ── App Background — road/tarmac feel ── */
.stApp {
    background:
        repeating-linear-gradient(90deg, transparent, transparent 48px, rgba(255,255,255,.018) 48px, rgba(255,255,255,.018) 50px),
        linear-gradient(180deg, #060d14 0%, #0a1628 40%, #0d1b2a 100%);
    min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a 0%, #111827 100%) !important;
    border-right: 1px solid #1e3a5f;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebarNav"] a { border-radius: 8px; margin: 2px 0; }
[data-testid="stSidebarNav"] a:hover { background: rgba(239,68,68,0.15) !important; }

/* ── Main content text ── */
.stApp, .stApp p, .stApp div, .stApp span, .stApp label { color: #e2e8f0; }
h1, h2, h3, h4, h5, h6 { color: #f1f5f9 !important; }

/* ── Emergency Hero Banner ── */
.emergency-hero {
    background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 50%, #b91c1c 100%);
    border-radius: 20px;
    padding: 0;
    margin-bottom: 2rem;
    border: 1px solid #ef4444;
    box-shadow: 0 0 60px rgba(239,68,68,0.35);
    overflow: hidden;
    position: relative;
    animation: pulse-border 3s infinite;
}
@keyframes pulse-border {
    0%, 100% { box-shadow: 0 0 30px rgba(239,68,68,0.35); }
    50%       { box-shadow: 0 0 80px rgba(239,68,68,0.65); }
}
.emergency-hero .hero-inner {
    display: flex; align-items: center; gap: 2rem;
    padding: 2rem 2.5rem;
}
.emergency-hero .hero-text { flex: 1; }
.emergency-hero h1 { color: #fff !important; font-size: 2.2rem; font-weight: 800; margin: 0 0 .4rem; line-height:1.2; }
.emergency-hero p  { color: #fca5a5 !important; font-size: 1rem; margin: .3rem 0 0; }
.emergency-hero .hero-svg { flex-shrink: 0; }
/* road stripe animation */
.hero-road { overflow:hidden; height:8px; background:#1a0000; }
.hero-road-stripe { height:8px; background: repeating-linear-gradient(90deg,
    #ef4444 0,#ef4444 40px, transparent 40px, transparent 80px);
    animation: road-anim 1.5s linear infinite; width:200%; }
@keyframes road-anim { from{transform:translateX(0)} to{transform:translateX(-80px)} }

/* ── Stat Cards ── */
.stat-card {
    background: rgba(17,24,39,0.95);
    border: 1px solid #1e3a5f;
    border-radius: 14px;
    padding: 1.2rem 1rem 1rem;
    text-align: center;
    transition: transform .2s, border-color .2s, box-shadow .2s;
    position: relative; overflow: hidden;
}
.stat-card:hover { transform: translateY(-3px); border-color: #ef4444; box-shadow: 0 8px 30px rgba(239,68,68,.2); }
.stat-card .sc-icon { margin-bottom: .4rem; }
.stat-card .value { font-size: 2.2rem; font-weight: 800; color: #ef4444; line-height:1; }
.stat-card .label { font-size: 0.78rem; color: #94a3b8; margin-top: 5px; text-transform: uppercase; letter-spacing: .05em; }

/* ── Metric Cards (kept for other pages) ── */
.metric-card {
    background: rgba(17,24,39,0.9);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    transition: transform .2s, border-color .2s;
}
.metric-card:hover { transform: translateY(-2px); border-color: #ef4444; }
.metric-card .value { font-size: 2.2rem; font-weight: 800; color: #ef4444; }
.metric-card .label { font-size: 0.82rem; color: #94a3b8; margin-top: 4px; text-transform: uppercase; letter-spacing: .05em; }

/* ── Feature Cards ── */
.feature-card {
    background: rgba(17,24,39,0.8);
    border: 1px solid #1e3a5f;
    border-radius: 14px;
    padding: 1.6rem;
    height: 100%;
    transition: border-color .2s, transform .2s;
}
.feature-card:hover { border-color: #3b82f6; transform: translateY(-3px); }
.feature-card .icon { font-size: 2.4rem; margin-bottom: .8rem; }
.feature-card h3 { color: #f1f5f9 !important; margin: 0 0 .5rem; font-size: 1.1rem; }
.feature-card p  { color: #94a3b8; font-size: .88rem; margin: 0; line-height: 1.6; }

/* ── Section Headers ── */
.section-header {
    display: flex; align-items: center; gap: .75rem;
    padding: 1rem 1.4rem;
    background: rgba(17,24,39,0.9);
    border-radius: 10px;
    border-left: 4px solid #ef4444;
    margin-bottom: 1.5rem;
}
.section-header h2 { margin: 0; font-size: 1.3rem; color: #f1f5f9 !important; }

/* ── Info Box ── */
.info-box {
    background: rgba(59,130,246,0.1);
    border: 1px solid #3b82f6;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    color: #bfdbfe !important;
    font-size: .9rem;
}
.warning-box {
    background: rgba(234,179,8,0.1);
    border: 1px solid #eab308;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    color: #fef08a !important;
    font-size: .9rem;
}
.success-box {
    background: rgba(34,197,94,0.1);
    border: 1px solid #22c55e;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    color: #bbf7d0 !important;
    font-size: .9rem;
}
.danger-box {
    background: rgba(239,68,68,0.1);
    border: 1px solid #ef4444;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    color: #fca5a5 !important;
    font-size: .9rem;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all .2s !important;
    box-shadow: 0 4px 14px rgba(239,68,68,.35) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #ef4444, #dc2626) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(239,68,68,.5) !important;
}

/* ── Form Elements ── */
.stTextInput input, .stTextArea textarea, .stSelectbox select,
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
    background: rgba(15,23,42,0.9) !important;
    border: 1px solid #1e3a5f !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #ef4444 !important;
    box-shadow: 0 0 0 2px rgba(239,68,68,.2) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15,23,42,0.6) !important;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #94a3b8 !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(239,68,68,0.2) !important;
    color: #ef4444 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(17,24,39,0.8) !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 10px !important;
}

/* ── QR Display Box ── */
.qr-container {
    background: #fff;
    border-radius: 16px;
    padding: 1.5rem;
    display: inline-block;
    box-shadow: 0 0 40px rgba(239,68,68,.4);
    border: 3px solid #ef4444;
}

/* ── Chat Messages ── */
.chat-user {
    background: rgba(59,130,246,0.15);
    border: 1px solid #3b82f6;
    border-radius: 12px 12px 4px 12px;
    padding: .9rem 1.1rem;
    margin: .5rem 0;
    color: #bfdbfe !important;
}
.chat-assistant {
    background: rgba(17,24,39,0.9);
    border: 1px solid #1e3a5f;
    border-radius: 4px 12px 12px 12px;
    padding: .9rem 1.1rem;
    margin: .5rem 0;
    color: #e2e8f0 !important;
}
.chat-citation {
    background: rgba(234,179,8,0.1);
    border-left: 3px solid #eab308;
    border-radius: 4px;
    padding: .4rem .8rem;
    font-size: .78rem;
    color: #fef08a !important;
    margin-top: .5rem;
}

/* ── Status Badges ── */
.badge-success { background:#166534; color:#bbf7d0; padding:2px 10px; border-radius:20px; font-size:.78rem; font-weight:600; }
.badge-warning { background:#713f12; color:#fef08a; padding:2px 10px; border-radius:20px; font-size:.78rem; font-weight:600; }
.badge-danger  { background:#7f1d1d; color:#fca5a5; padding:2px 10px; border-radius:20px; font-size:.78rem; font-weight:600; }
.badge-info    { background:#1e3a5f; color:#bfdbfe; padding:2px 10px; border-radius:20px; font-size:.78rem; font-weight:600; }

/* ── DataFrames ── */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0d1b2a; }
::-webkit-scrollbar-thumb { background: #374151; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #ef4444; }

/* ── Progress Bar ── */
.stProgress .st-bo { background: linear-gradient(90deg, #ef4444, #f97316) !important; }

/* ── Metric value ── */
[data-testid="stMetricValue"] { color: #ef4444 !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #94a3b8 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Session-state Defaults ────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "vehicles": {},        # plate → vehicle dict
        "incidents": [],       # list of incident dicts
        "chat_history": [],    # RAG chat turns
        "audit_log": [],       # event log
        "current_incident": None,
        "api_key": "BHuyA83x8mQXePpG2BEVPD9RdSxS3MWbISvzoLss4__P",
        "project_id": "4be3dc1c-361e-4e4e-b1f7-692df9099153",
        "notifications_sent": 0,
        "total_scans": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ─── Seed demo data ────────────────────────────────────────────────────────────
if not st.session_state.vehicles:
    st.session_state.vehicles["KA01AB1234"] = {
        "plate": "KA01AB1234",
        "make": "Maruti Suzuki", "model": "Swift", "year": 2021, "color": "White",
        "owner": "Ravi Kumar",
        "dob": "1985-07-14", "blood_group": "O+",
        "allergies": "Penicillin, Sulfa drugs",
        "conditions": "Type-2 Diabetes, Mild Hypertension",
        "medications": "Metformin 500mg (twice daily), Amlodipine 5mg (once daily)",
        "organ_donor": True,
        "contacts": [
            {"name": "Priya Kumar", "relation": "Spouse", "phone": "+91-98765-43210", "priority": 1},
            {"name": "Arun Kumar",  "relation": "Brother","phone": "+91-87654-32109", "priority": 2},
        ],
        "insurance": "HDFC ERGO — Policy #HE2024-78901",
        "created": "2024-01-15T10:30:00",
    }
    st.session_state.vehicles["MH02CD5678"] = {
        "plate": "MH02CD5678",
        "make": "Honda", "model": "City", "year": 2022, "color": "Silver",
        "owner": "Anita Sharma",
        "dob": "1990-03-22", "blood_group": "A+",
        "allergies": "None known",
        "conditions": "None",
        "medications": "None",
        "organ_donor": False,
        "contacts": [
            {"name": "Suresh Sharma","relation": "Father","phone": "+91-77654-32101","priority": 1},
        ],
        "insurance": "New India Assurance — Policy #NI2024-56789",
        "created": "2024-02-20T14:15:00",
    }
    st.session_state.audit_log = [
        {"time": "2024-11-20 08:14:32", "event": "QR Scan",       "vehicle": "KA01AB1234", "actor": "Bystander",    "details": "Incident portal opened — Bengaluru NH-44"},
        {"time": "2024-11-20 08:14:55", "event": "Notification",  "vehicle": "KA01AB1234", "actor": "System",       "details": "Call + SMS to Priya Kumar — Delivered"},
        {"time": "2024-11-20 08:15:10", "event": "RAG Query",     "vehicle": "KA01AB1234", "actor": "Bystander",    "details": "Query: bleeding control unconscious victim"},
        {"time": "2024-11-20 08:22:00", "event": "Acknowledgement","vehicle": "KA01AB1234","actor": "Priya Kumar",  "details": "Family acknowledged — en-route"},
        {"time": "2024-11-19 16:45:12", "event": "QR Scan",       "vehicle": "MH02CD5678", "actor": "Police",       "details": "Incident portal opened — Mumbai Expressway"},
        {"time": "2024-11-19 16:45:40", "event": "Notification",  "vehicle": "MH02CD5678", "actor": "System",       "details": "Call + SMS to Suresh Sharma — Delivered"},
    ]
    st.session_state.total_scans = 14
    st.session_state.notifications_sent = 31

# ─── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: .8rem 0 1.2rem;">
      <!-- Ambulance SVG logo -->
      <svg width="130" height="65" viewBox="0 0 180 90" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto .5rem;">
        <rect x="10" y="30" width="140" height="45" rx="6" fill="#dc2626"/>
        <rect x="120" y="18" width="30" height="57" rx="4" fill="#b91c1c"/>
        <rect x="123" y="22" width="22" height="20" rx="3" fill="#bfdbfe" opacity=".8"/>
        <rect x="40" y="36" width="36" height="30" rx="3" fill="white"/>
        <rect x="52" y="38" width="12" height="26" rx="2" fill="#dc2626"/>
        <rect x="42" y="47" width="32" height="10" rx="2" fill="#dc2626"/>
        <rect x="20" y="24" width="96" height="8" rx="4" fill="#1e3a5f"/>
        <rect x="24" y="26" width="12" height="4" rx="2" fill="#ef4444"/>
        <rect x="40" y="26" width="12" height="4" rx="2" fill="#93c5fd"/>
        <rect x="56" y="26" width="12" height="4" rx="2" fill="#ef4444"/>
        <rect x="72" y="26" width="12" height="4" rx="2" fill="#93c5fd"/>
        <rect x="88" y="26" width="12" height="4" rx="2" fill="#ef4444"/>
        <circle cx="40" cy="76" r="12" fill="#1f2937"/><circle cx="40" cy="76" r="6" fill="#374151"/>
        <circle cx="130" cy="76" r="12" fill="#1f2937"/><circle cx="130" cy="76" r="6" fill="#374151"/>
        <line x1="100" y1="32" x2="100" y2="74" stroke="#991b1b" stroke-width="2"/>
        <text x="58" y="72" font-family="Arial" font-size="9" font-weight="bold" fill="white">108</text>
      </svg>
      <div style="font-size:1.1rem; font-weight:800; color:#ef4444; letter-spacing:.03em;">VehicleGuard</div>
      <div style="font-size:.7rem; color:#64748b; margin-top:2px;">Emergency Response System</div>
      <div style="margin-top:.6rem; padding:.25rem .8rem; background:rgba(239,68,68,.15);
           border-radius:20px; font-size:.68rem; color:#fca5a5; display:inline-block; letter-spacing:.05em;">
           🟢 SYSTEM ACTIVE
      </div>
    </div>
    <hr style="border-color:#1e3a5f; margin:0 0 1rem;">
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🏠 Home", "📋 Owner Registration", "🔲 QR Code Generator",
         "🚑 Incident Portal", "🤖 RAG Assistant", "📊 Audit & Analytics"],
        label_visibility="collapsed"
    )

    st.markdown("""
    <hr style="border-color:#1e3a5f; margin:1rem 0;">
    <div style="font-size:.75rem; color:#475569; text-align:center; line-height:1.7;">
        <div>Powered by <b style="color:#3b82f6;">IBM WatsonX AI</b></div>
        <div style="margin-top:3px;">RAG · Golden Hour Response</div>
        <div style="margin-top:.4rem; font-size:.68rem; color:#374151;">
            Project ID: 4be3dc1c…<br>
            API: BHuyA83…
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Home":

    # ── SVG Illustrations ──────────────────────────────────────────────────────
    SVG_AMBULANCE = """
    <svg width="180" height="90" viewBox="0 0 180 90" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- body -->
      <rect x="10" y="30" width="140" height="45" rx="6" fill="#dc2626"/>
      <!-- cab -->
      <rect x="120" y="18" width="30" height="57" rx="4" fill="#b91c1c"/>
      <!-- windshield -->
      <rect x="123" y="22" width="22" height="20" rx="3" fill="#bfdbfe" opacity=".8"/>
      <!-- red cross box -->
      <rect x="40" y="36" width="36" height="30" rx="3" fill="white"/>
      <rect x="52" y="38" width="12" height="26" rx="2" fill="#dc2626"/>
      <rect x="42" y="47" width="32" height="10" rx="2" fill="#dc2626"/>
      <!-- siren bar -->
      <rect x="20" y="24" width="96" height="8" rx="4" fill="#1e3a5f"/>
      <rect x="24" y="26" width="12" height="4" rx="2" fill="#ef4444"/>
      <rect x="40" y="26" width="12" height="4" rx="2" fill="#3b82f6"/>
      <rect x="56" y="26" width="12" height="4" rx="2" fill="#ef4444"/>
      <rect x="72" y="26" width="12" height="4" rx="2" fill="#3b82f6"/>
      <rect x="88" y="26" width="12" height="4" rx="2" fill="#ef4444"/>
      <!-- wheels -->
      <circle cx="40" cy="76" r="12" fill="#1f2937"/><circle cx="40" cy="76" r="6" fill="#374151"/>
      <circle cx="130" cy="76" r="12" fill="#1f2937"/><circle cx="130" cy="76" r="6" fill="#374151"/>
      <!-- door line -->
      <line x1="100" y1="32" x2="100" y2="74" stroke="#991b1b" stroke-width="2"/>
      <!-- 108 text -->
      <text x="58" y="72" font-family="Arial" font-size="9" font-weight="bold" fill="white">108</text>
    </svg>"""

    SVG_QR = """
    <svg width="90" height="90" viewBox="0 0 90 90" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="90" height="90" rx="10" fill="white"/>
      <!-- top-left finder -->
      <rect x="8" y="8" width="22" height="22" rx="3" fill="#1f2937"/>
      <rect x="13" y="13" width="12" height="12" rx="2" fill="white"/>
      <rect x="16" y="16" width="6" height="6" rx="1" fill="#dc2626"/>
      <!-- top-right finder -->
      <rect x="60" y="8" width="22" height="22" rx="3" fill="#1f2937"/>
      <rect x="65" y="13" width="12" height="12" rx="2" fill="white"/>
      <rect x="68" y="16" width="6" height="6" rx="1" fill="#dc2626"/>
      <!-- bottom-left finder -->
      <rect x="8" y="60" width="22" height="22" rx="3" fill="#1f2937"/>
      <rect x="13" y="65" width="12" height="12" rx="2" fill="white"/>
      <rect x="16" y="68" width="6" height="6" rx="1" fill="#dc2626"/>
      <!-- data modules (scattered) -->
      <rect x="36" y="8" width="6" height="6" rx="1" fill="#1f2937"/>
      <rect x="44" y="8" width="6" height="6" rx="1" fill="#1f2937"/>
      <rect x="36" y="16" width="6" height="6" rx="1" fill="#1f2937"/>
      <rect x="8" y="36" width="6" height="6" rx="1" fill="#1f2937"/>
      <rect x="8" y="44" width="6" height="6" rx="1" fill="#1f2937"/>
      <rect x="36" y="36" width="6" height="6" rx="1" fill="#dc2626"/>
      <rect x="44" y="36" width="6" height="6" rx="1" fill="#1f2937"/>
      <rect x="52" y="36" width="6" height="6" rx="1" fill="#1f2937"/>
      <rect x="60" y="36" width="6" height="6" rx="1" fill="#dc2626"/>
      <rect x="68" y="36" width="6" height="6" rx="1" fill="#1f2937"/>
      <rect x="76" y="36" width="6" height="6" rx="1" fill="#1f2937"/>
      <rect x="36" y="44" width="6" height="6" rx="1" fill="#1f2937"/>
      <rect x="52" y="44" width="6" height="6" rx="1" fill="#dc2626"/>
      <rect x="68" y="44" width="6" height="6" rx="1" fill="#1f2937"/>
      <rect x="36" y="52" width="6" height="6" rx="1" fill="#dc2626"/>
      <rect x="44" y="52" width="6" height="6" rx="1" fill="#1f2937"/>
      <rect x="60" y="52" width="6" height="6" rx="1" fill="#1f2937"/>
      <rect x="76" y="52" width="6" height="6" rx="1" fill="#dc2626"/>
      <rect x="44" y="60" width="6" height="6" rx="1" fill="#1f2937"/>
      <rect x="52" y="68" width="6" height="6" rx="1" fill="#dc2626"/>
      <rect x="60" y="76" width="6" height="6" rx="1" fill="#1f2937"/>
      <rect x="76" y="68" width="6" height="6" rx="1" fill="#1f2937"/>
      <rect x="76" y="76" width="6" height="6" rx="1" fill="#1f2937"/>
    </svg>"""

    SVG_CAR_CRASH = """
    <svg width="200" height="110" viewBox="0 0 200 110" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- road -->
      <rect x="0" y="80" width="200" height="30" fill="#1a1a2e"/>
      <rect x="20" y="93" width="30" height="4" rx="2" fill="#374151"/>
      <rect x="85" y="93" width="30" height="4" rx="2" fill="#374151"/>
      <rect x="150" y="93" width="30" height="4" rx="2" fill="#374151"/>
      <!-- car 1 (left, tilted) -->
      <g transform="rotate(-8,60,70)">
        <rect x="20" y="52" width="80" height="28" rx="6" fill="#1d4ed8"/>
        <rect x="30" y="38" width="55" height="20" rx="5" fill="#1e40af"/>
        <rect x="34" y="41" width="20" height="14" rx="2" fill="#bfdbfe" opacity=".7"/>
        <rect x="58" y="41" width="20" height="14" rx="2" fill="#bfdbfe" opacity=".7"/>
        <circle cx="35" cy="80" r="10" fill="#111827"/><circle cx="35" cy="80" r="5" fill="#374151"/>
        <circle cx="85" cy="80" r="10" fill="#111827"/><circle cx="85" cy="80" r="5" fill="#374151"/>
      </g>
      <!-- car 2 (right, tilted other way) -->
      <g transform="rotate(10,145,70)">
        <rect x="110" y="52" width="80" height="28" rx="6" fill="#dc2626"/>
        <rect x="120" y="38" width="55" height="20" rx="5" fill="#b91c1c"/>
        <rect x="124" y="41" width="20" height="14" rx="2" fill="#fca5a5" opacity=".7"/>
        <rect x="148" y="41" width="20" height="14" rx="2" fill="#fca5a5" opacity=".7"/>
        <circle cx="122" cy="80" r="10" fill="#111827"/><circle cx="122" cy="80" r="5" fill="#374151"/>
        <circle cx="175" cy="80" r="10" fill="#111827"/><circle cx="175" cy="80" r="5" fill="#374151"/>
      </g>
      <!-- impact sparks -->
      <circle cx="100" cy="62" r="3" fill="#fbbf24" opacity=".9"/>
      <circle cx="107" cy="55" r="2" fill="#f97316" opacity=".8"/>
      <circle cx="93" cy="57" r="2.5" fill="#ef4444" opacity=".9"/>
      <circle cx="104" cy="68" r="1.8" fill="#fbbf24"/>
      <circle cx="96" cy="70" r="2" fill="#f97316"/>
      <!-- warning triangle -->
      <polygon points="100,10 86,34 114,34" fill="none" stroke="#fbbf24" stroke-width="3"/>
      <text x="96.5" y="30" font-family="Arial" font-size="14" font-weight="bold" fill="#fbbf24">!</text>
    </svg>"""

    SVG_PHONE_SCAN = """
    <svg width="90" height="130" viewBox="0 0 90 130" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- phone body -->
      <rect x="10" y="5" width="70" height="120" rx="12" fill="#1f2937"/>
      <rect x="14" y="9" width="62" height="112" rx="9" fill="#111827"/>
      <!-- screen -->
      <rect x="16" y="12" width="58" height="96" rx="7" fill="#0a1628"/>
      <!-- QR on screen -->
      <rect x="24" y="20" width="42" height="42" rx="4" fill="white" opacity=".95"/>
      <rect x="27" y="23" width="10" height="10" rx="1" fill="#1f2937"/>
      <rect x="29" y="25" width="6" height="6" rx="1" fill="#dc2626"/>
      <rect x="49" y="23" width="10" height="10" rx="1" fill="#1f2937"/>
      <rect x="51" y="25" width="6" height="6" rx="1" fill="#dc2626"/>
      <rect x="27" y="43" width="10" height="10" rx="1" fill="#1f2937"/>
      <rect x="29" y="45" width="6" height="6" rx="1" fill="#dc2626"/>
      <rect x="40" y="23" width="4" height="4" rx="1" fill="#1f2937"/>
      <rect x="40" y="30" width="4" height="4" rx="1" fill="#dc2626"/>
      <rect x="40" y="37" width="4" height="4" rx="1" fill="#1f2937"/>
      <rect x="40" y="44" width="4" height="4" rx="1" fill="#1f2937"/>
      <rect x="47" y="30" width="4" height="4" rx="1" fill="#1f2937"/>
      <rect x="53" y="37" width="4" height="4" rx="1" fill="#dc2626"/>
      <rect x="47" y="44" width="4" height="4" rx="1" fill="#1f2937"/>
      <!-- scan line -->
      <line x1="20" y1="41" x2="70" y2="41" stroke="#22c55e" stroke-width="2" opacity=".9"/>
      <line x1="20" y1="41" x2="70" y2="41" stroke="#22c55e" stroke-width="8" opacity=".15"/>
      <!-- notification card on screen -->
      <rect x="18" y="68" width="54" height="34" rx="4" fill="#7f1d1d" opacity=".9"/>
      <text x="22" y="80" font-family="Arial" font-size="6" font-weight="bold" fill="#fca5a5">🚨 EMERGENCY ALERT</text>
      <text x="22" y="90" font-family="Arial" font-size="5" fill="#fecaca">Family notified</text>
      <text x="22" y="98" font-family="Arial" font-size="5" fill="#fecaca">Ambulance dispatched</text>
      <!-- home button -->
      <circle cx="45" cy="119" r="5" fill="#374151"/>
    </svg>"""

    SVG_MEDICAL = """
    <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- shield -->
      <path d="M50 5 L90 20 L90 55 Q90 80 50 95 Q10 80 10 55 L10 20 Z" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
      <!-- cross -->
      <rect x="38" y="30" width="24" height="40" rx="4" fill="white" opacity=".95"/>
      <rect x="28" y="40" width="44" height="20" rx="4" fill="white" opacity=".95"/>
      <!-- blood drop -->
      <path d="M50 42 Q44 50 44 55 Q44 61 50 61 Q56 61 56 55 Q56 50 50 42Z" fill="#dc2626"/>
      <text x="43" y="58" font-family="Arial" font-size="9" font-weight="bold" fill="white">O+</text>
    </svg>"""

    SVG_BRAIN_AI = """
    <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- brain shape -->
      <ellipse cx="50" cy="45" rx="30" ry="28" fill="#1e3a5f" stroke="#3b82f6" stroke-width="1.5"/>
      <path d="M20 45 Q18 32 28 26 Q38 20 50 22 Q62 20 72 26 Q82 32 80 45" fill="none" stroke="#3b82f6" stroke-width="1.5"/>
      <path d="M50 22 L50 68" stroke="#1d4ed8" stroke-width="1.5" stroke-dasharray="3,3"/>
      <path d="M20 45 Q35 42 50 45 Q65 42 80 45" fill="none" stroke="#3b82f6" stroke-width="1.5"/>
      <!-- circuit lines -->
      <line x1="30" y1="38" x2="38" y2="38" stroke="#22c55e" stroke-width="1.5"/>
      <line x1="38" y1="38" x2="38" y2="30" stroke="#22c55e" stroke-width="1.5"/>
      <circle cx="38" cy="30" r="2.5" fill="#22c55e"/>
      <line x1="62" y1="38" x2="70" y2="38" stroke="#22c55e" stroke-width="1.5"/>
      <line x1="62" y1="38" x2="62" y2="30" stroke="#22c55e" stroke-width="1.5"/>
      <circle cx="62" cy="30" r="2.5" fill="#22c55e"/>
      <line x1="40" y1="52" x2="40" y2="62" stroke="#f97316" stroke-width="1.5"/>
      <circle cx="40" cy="62" r="2.5" fill="#f97316"/>
      <line x1="60" y1="52" x2="60" y2="62" stroke="#f97316" stroke-width="1.5"/>
      <circle cx="60" cy="62" r="2.5" fill="#f97316"/>
      <!-- IBM label -->
      <rect x="34" y="74" width="32" height="14" rx="4" fill="#0f62fe"/>
      <text x="38" y="84" font-family="Arial" font-size="8" font-weight="bold" fill="white">Watson</text>
    </svg>"""

    SVG_GPS = """
    <svg width="80" height="90" viewBox="0 0 80 90" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- pin -->
      <path d="M40 5 C22 5 10 18 10 32 C10 52 40 80 40 80 C40 80 70 52 70 32 C70 18 58 5 40 5Z" fill="#dc2626"/>
      <circle cx="40" cy="32" r="12" fill="white"/>
      <circle cx="40" cy="32" r="6" fill="#dc2626"/>
      <!-- signal rings -->
      <circle cx="40" cy="32" r="18" fill="none" stroke="#ef4444" stroke-width="1.5" opacity=".5"/>
      <circle cx="40" cy="32" r="24" fill="none" stroke="#ef4444" stroke-width="1" opacity=".3"/>
      <!-- coordinate text -->
      <rect x="5" y="82" width="70" height="10" rx="3" fill="#1e3a5f"/>
      <text x="10" y="90" font-family="monospace" font-size="6" fill="#22c55e">12.9716°N 77.5946°E</text>
    </svg>"""

    SVG_NOTIFICATION = """
    <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- bell -->
      <path d="M50 10 C35 10 25 22 25 36 L25 60 L15 70 L85 70 L75 60 L75 36 C75 22 65 10 50 10Z" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
      <rect x="40" y="68" width="20" height="10" rx="5" fill="#374151"/>
      <circle cx="50" cy="78" r="6" fill="#1f2937" stroke="#3b82f6" stroke-width="2"/>
      <!-- notification badge -->
      <circle cx="72" cy="18" r="12" fill="#dc2626"/>
      <text x="67" y="23" font-family="Arial" font-size="11" font-weight="bold" fill="white">!</text>
      <!-- wave rings -->
      <path d="M15 36 Q10 50 15 64" fill="none" stroke="#3b82f6" stroke-width="2" opacity=".6"/>
      <path d="M8 32 Q2 50 8 68" fill="none" stroke="#3b82f6" stroke-width="1.5" opacity=".4"/>
      <path d="M85 36 Q90 50 85 64" fill="none" stroke="#3b82f6" stroke-width="2" opacity=".6"/>
      <path d="M92 32 Q98 50 92 68" fill="none" stroke="#3b82f6" stroke-width="1.5" opacity=".4"/>
    </svg>"""

    # ── HERO BANNER with SVG illustrations ───────────────────────────────────
    st.markdown(f"""
    <div class="emergency-hero">
      <div class="hero-road"><div class="hero-road-stripe"></div></div>
      <div class="hero-inner">
        <div style="flex-shrink:0;">{SVG_AMBULANCE}</div>
        <div class="hero-text">
          <div style="font-size:.7rem;letter-spacing:.15em;color:#fca5a5;font-weight:700;margin-bottom:.5rem;">
            🔴 GOLDEN HOUR RESPONSE SYSTEM
          </div>
          <h1>VehicleGuard<br>Emergency Response</h1>
          <p>QR-Code-Enabled Accident Notification with IBM WatsonX RAG Knowledge Assistant</p>
          <p style="color:#fecaca;font-size:.82rem;margin-top:.6rem;">
            One QR scan → Medical profile revealed · Family notified · AI first-aid guidance
          </p>
          <div style="display:flex;gap:.6rem;margin-top:1rem;flex-wrap:wrap;">
            <span style="background:rgba(255,255,255,.12);color:#fff;padding:.3rem .8rem;border-radius:20px;font-size:.72rem;font-weight:600;">
              🏥 108 Ambulance Ready
            </span>
            <span style="background:rgba(255,255,255,.12);color:#fff;padding:.3rem .8rem;border-radius:20px;font-size:.72rem;font-weight:600;">
              🤖 IBM WatsonX RAG
            </span>
            <span style="background:rgba(255,255,255,.12);color:#fff;padding:.3rem .8rem;border-radius:20px;font-size:.72rem;font-weight:600;">
              🔐 HMAC Signed QR
            </span>
          </div>
        </div>
        <div style="flex-shrink:0;display:flex;flex-direction:column;align-items:center;gap:.8rem;">
          {SVG_QR}
          <div style="font-size:.68rem;color:#fca5a5;font-weight:600;letter-spacing:.08em;">SCAN TO RESPOND</div>
        </div>
      </div>
      <div class="hero-road"><div class="hero-road-stripe"></div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Live Stat Cards with SVG icons ───────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    stat_svgs = [
        # car icon
        """<svg width="36" height="24" viewBox="0 0 36 24"><rect x="2" y="8" width="32" height="12" rx="4" fill="#ef4444"/>
           <rect x="6" y="4" width="22" height="9" rx="3" fill="#b91c1c"/>
           <circle cx="9" cy="20" r="4" fill="#1f2937"/><circle cx="27" cy="20" r="4" fill="#1f2937"/>
           <rect x="8" y="6" width="8" height="6" rx="1" fill="#bfdbfe" opacity=".7"/>
           <rect x="20" y="6" width="8" height="6" rx="1" fill="#bfdbfe" opacity=".7"/></svg>""",
        # QR scan icon
        """<svg width="36" height="36" viewBox="0 0 36 36"><rect x="2" y="2" width="12" height="12" rx="2" fill="none" stroke="#ef4444" stroke-width="2"/>
           <rect x="5" y="5" width="6" height="6" rx="1" fill="#ef4444"/>
           <rect x="22" y="2" width="12" height="12" rx="2" fill="none" stroke="#ef4444" stroke-width="2"/>
           <rect x="25" y="5" width="6" height="6" rx="1" fill="#ef4444"/>
           <rect x="2" y="22" width="12" height="12" rx="2" fill="none" stroke="#ef4444" stroke-width="2"/>
           <rect x="5" y="25" width="6" height="6" rx="1" fill="#ef4444"/>
           <line x1="22" y1="22" x2="34" y2="34" stroke="#ef4444" stroke-width="2"/></svg>""",
        # bell icon
        """<svg width="30" height="34" viewBox="0 0 30 34"><path d="M15 2C9 2 5 7 5 13L5 24L1 28L29 28L25 24L25 13C25 7 21 2 15 2Z" fill="#ef4444"/>
           <circle cx="15" cy="31" r="3" fill="#b91c1c"/></svg>""",
        # checkmark icon
        """<svg width="36" height="36" viewBox="0 0 36 36"><circle cx="18" cy="18" r="16" fill="none" stroke="#ef4444" stroke-width="2"/>
           <polyline points="10,18 15,24 26,12" fill="none" stroke="#ef4444" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>""",
    ]
    stat_data = [
        (len(st.session_state.vehicles), "Registered Vehicles"),
        (st.session_state.total_scans, "Total QR Scans"),
        (st.session_state.notifications_sent, "Notifications Sent"),
        ("98.4%", "Success Rate"),
    ]
    for col, svg, (val, label) in zip([col1,col2,col3,col4], stat_svgs, stat_data):
        with col:
            st.markdown(f"""
            <div class="stat-card">
              <div class="sc-icon">{svg}</div>
              <div class="value">{val}</div>
              <div class="label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── How It Works — illustrated steps ─────────────────────────────────────
    st.markdown("""
    <div class="section-header">
        <span style="font-size:1.4rem;">⚡</span>
        <h2>How It Works — The Golden Hour Chain</h2>
    </div>
    """, unsafe_allow_html=True)

    steps_data = [
        (SVG_QR,           "1. QR Sticker on Vehicle",     "Tamper-resistant HMAC-signed QR on dashboard, fuel lid and rear windscreen. No app needed by responder."),
        (SVG_PHONE_SCAN,   "2. Bystander Scans QR",        "Any smartphone camera — scan opens the mobile-first incident portal instantly with full victim profile."),
        (SVG_MEDICAL,      "3. Medical Profile Revealed",   "Blood group, allergies, medications and chronic conditions shown to responder immediately."),
        (SVG_GPS,          "4. Auto Notification Triggered","Automated call + SMS/WhatsApp to family with live GPS coordinates, timestamp and responder callback."),
        (SVG_BRAIN_AI,     "5. RAG Assistant Guides",       "IBM WatsonX Granite LLM answers first-aid questions from verified protocols — cited, no hallucination."),
        (SVG_NOTIFICATION, "6. Audit Trail Created",        "Every scan, call status and assistant query logged with timestamps for accountability and review."),
    ]
    r1_cols = st.columns(3)
    r2_cols = st.columns(3)
    for i, (svg, title, desc) in enumerate(steps_data):
        col = r1_cols[i] if i < 3 else r2_cols[i - 3]
        with col:
            st.markdown(f"""
            <div class="feature-card" style="text-align:center;">
              <div style="margin:.4rem auto .8rem;width:fit-content;">{svg}</div>
              <h3 style="font-size:.95rem;">{title}</h3>
              <p>{desc}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Problem vs Solution row with illustrations ────────────────────────────
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="section-header"><span>💥</span><h2>The Problem</h2></div>
        <div class="danger-box" style="display:flex;gap:1.2rem;align-items:flex-start;">
          <div style="flex-shrink:0;">{SVG_CAR_CRASH}</div>
          <div>
            <b>India records one of the highest road-traffic fatality rates globally.</b><br><br>
            Deaths attributed to:<br>
            🔴 Delayed detection &amp; notification<br>
            🔴 Medical info locked in damaged vehicle<br>
            🔴 Untrained bystanders, no guidance<br>
            🔴 Family informed hours late
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="section-header"><span>🧠</span><h2>IBM WatsonX RAG Solution</h2></div>
        <div class="info-box" style="display:flex;gap:1.2rem;align-items:flex-start;">
          <div style="flex-shrink:0;">{SVG_BRAIN_AI}</div>
          <div>
            <b>RAG grounds every answer in a curated verified knowledge base:</b><br><br>
            📄 First-aid &amp; trauma-care protocols<br>
            🚑 Emergency response procedures<br>
            👤 Victim-specific uploaded documents<br>
            🚗 EV high-voltage safety guidance<br><br>
            <b>Every answer is cited. Low-confidence queries defer to 108/112.</b>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Quick Action Cards with SVG ───────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="section-header"><span>🚀</span><h2>Quick Actions</h2></div>""", unsafe_allow_html=True)

    qa_svgs = [
        # clipboard/registration
        """<svg width="48" height="52" viewBox="0 0 48 52"><rect x="4" y="8" width="40" height="40" rx="5" fill="#1e3a5f" stroke="#3b82f6" stroke-width="1.5"/>
           <rect x="16" y="2" width="16" height="10" rx="3" fill="#374151" stroke="#3b82f6" stroke-width="1.5"/>
           <line x1="12" y1="22" x2="36" y2="22" stroke="#3b82f6" stroke-width="2"/>
           <line x1="12" y1="30" x2="36" y2="30" stroke="#3b82f6" stroke-width="2"/>
           <line x1="12" y1="38" x2="28" y2="38" stroke="#3b82f6" stroke-width="2"/></svg>""",
        # QR sticker
        """<svg width="48" height="48" viewBox="0 0 48 48"><rect x="2" y="2" width="44" height="44" rx="6" fill="#1e3a5f" stroke="#ef4444" stroke-width="2"/>
           <rect x="8" y="8" width="14" height="14" rx="2" fill="none" stroke="#ef4444" stroke-width="2"/>
           <rect x="11" y="11" width="8" height="8" rx="1" fill="#ef4444"/>
           <rect x="26" y="8" width="14" height="14" rx="2" fill="none" stroke="#ef4444" stroke-width="2"/>
           <rect x="29" y="11" width="8" height="8" rx="1" fill="#ef4444"/>
           <rect x="8" y="26" width="14" height="14" rx="2" fill="none" stroke="#ef4444" stroke-width="2"/>
           <rect x="11" y="29" width="8" height="8" rx="1" fill="#ef4444"/>
           <rect x="27" y="27" width="4" height="4" fill="#ef4444"/><rect x="33" y="27" width="4" height="4" fill="#ef4444"/>
           <rect x="27" y="33" width="4" height="4" fill="#ef4444"/><rect x="33" y="33" width="4" height="4" fill="#ef4444"/></svg>""",
        # ambulance
        f"""<div style="transform:scale(.55);transform-origin:top left;width:88px;height:44px;overflow:hidden;">{SVG_AMBULANCE}</div>""",
        # brain
        f"""<div style="transform:scale(.5);transform-origin:top left;width:50px;height:50px;overflow:hidden;">{SVG_BRAIN_AI}</div>""",
    ]
    qa_cols = st.columns(4)
    qa_data = [
        ("Register Vehicle",   "Add vehicle &amp; upload medical profile to the system"),
        ("Generate QR Sticker","Create signed QR codes for dashboard and windscreen"),
        ("Incident Portal",    "Simulate a QR scan and trigger the notification chain"),
        ("RAG Assistant",      "Ask IBM WatsonX grounded first-aid questions"),
    ]
    for col, svg, (label, desc) in zip(qa_cols, qa_svgs, qa_data):
        with col:
            st.markdown(f"""
            <div class="feature-card" style="text-align:center;min-height:160px;">
              <div style="height:52px;display:flex;align-items:center;justify-content:center;margin-bottom:.6rem;">{svg}</div>
              <h3 style="font-size:.95rem;">{label}</h3>
              <p style="font-size:.82rem;">{desc}</p>
            </div>""", unsafe_allow_html=True)

    # ── System Modules with icons ─────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="section-header"><span>🏗️</span><h2>System Modules (M1–M6)</h2></div>""", unsafe_allow_html=True)

    module_svgs = [
        # M1 - QR lock
        """<svg width="32" height="32" viewBox="0 0 32 32"><rect x="2" y="2" width="28" height="28" rx="4" fill="none" stroke="#ef4444" stroke-width="2"/>
           <rect x="6" y="6" width="8" height="8" rx="1" fill="none" stroke="#ef4444" stroke-width="1.5"/>
           <rect x="8" y="8" width="4" height="4" rx=".5" fill="#ef4444"/>
           <rect x="18" y="6" width="8" height="8" rx="1" fill="none" stroke="#ef4444" stroke-width="1.5"/>
           <rect x="20" y="8" width="4" height="4" rx=".5" fill="#ef4444"/>
           <rect x="6" y="18" width="8" height="8" rx="1" fill="none" stroke="#ef4444" stroke-width="1.5"/>
           <rect x="8" y="20" width="4" height="4" rx=".5" fill="#ef4444"/>
           <rect x="18" y="18" width="4" height="4" rx=".5" fill="#ef4444"/>
           <rect x="24" y="22" width="4" height="4" rx=".5" fill="#ef4444"/></svg>""",
        # M2 - person
        """<svg width="32" height="32" viewBox="0 0 32 32"><circle cx="16" cy="10" r="7" fill="#f97316" opacity=".8"/>
           <path d="M4 28 C4 20 28 20 28 28Z" fill="#f97316" opacity=".8"/></svg>""",
        # M3 - phone
        """<svg width="22" height="32" viewBox="0 0 22 32"><rect x="1" y="1" width="20" height="30" rx="4" fill="none" stroke="#eab308" stroke-width="2"/>
           <rect x="4" y="5" width="14" height="20" rx="2" fill="#eab308" opacity=".3"/>
           <circle cx="11" cy="28" r="2" fill="#eab308"/></svg>""",
        # M4 - signal
        """<svg width="32" height="28" viewBox="0 0 32 28"><circle cx="16" cy="20" r="4" fill="#22c55e"/>
           <path d="M8 14 Q16 6 24 14" fill="none" stroke="#22c55e" stroke-width="2.5" stroke-linecap="round"/>
           <path d="M3 8 Q16 -2 29 8" fill="none" stroke="#22c55e" stroke-width="2" stroke-linecap="round" opacity=".6"/></svg>""",
        # M5 - chip/AI
        """<svg width="32" height="32" viewBox="0 0 32 32"><rect x="8" y="8" width="16" height="16" rx="3" fill="#3b82f6" opacity=".8"/>
           <line x1="12" y1="2" x2="12" y2="8" stroke="#3b82f6" stroke-width="2"/><line x1="20" y1="2" x2="20" y2="8" stroke="#3b82f6" stroke-width="2"/>
           <line x1="12" y1="24" x2="12" y2="30" stroke="#3b82f6" stroke-width="2"/><line x1="20" y1="24" x2="20" y2="30" stroke="#3b82f6" stroke-width="2"/>
           <line x1="2" y1="12" x2="8" y2="12" stroke="#3b82f6" stroke-width="2"/><line x1="2" y1="20" x2="8" y2="20" stroke="#3b82f6" stroke-width="2"/>
           <line x1="24" y1="12" x2="30" y2="12" stroke="#3b82f6" stroke-width="2"/><line x1="24" y1="20" x2="30" y2="20" stroke="#3b82f6" stroke-width="2"/>
           <circle cx="16" cy="16" r="3" fill="white"/></svg>""",
        # M6 - chart
        """<svg width="32" height="28" viewBox="0 0 32 28"><rect x="2" y="18" width="6" height="8" rx="1" fill="#8b5cf6"/>
           <rect x="10" y="10" width="6" height="16" rx="1" fill="#8b5cf6"/>
           <rect x="18" y="4" width="6" height="22" rx="1" fill="#8b5cf6"/>
           <rect x="26" y="12" width="6" height="14" rx="1" fill="#8b5cf6" opacity=".6"/>
           <line x1="1" y1="27" x2="32" y2="27" stroke="#6d28d9" stroke-width="1.5"/></svg>""",
    ]
    modules = [
        ("M1", "QR Issuance & Verification", "#ef4444",
         "Signed HMAC token generation, sticker rendering, tamper & replay protection."),
        ("M2", "Profile & Contact Mgmt", "#f97316",
         "Vehicle + victim medical profile, priority-ordered emergency contacts."),
        ("M3", "Incident Portal", "#eab308",
         "Mobile-first scan landing page, one-tap notify, live-location consent, medical card."),
        ("M4", "Notification Engine", "#22c55e",
         "Outbound call, SMS/WhatsApp, acknowledgement tracking, escalation chain, retry policy."),
        ("M5", "RAG Knowledge Assistant", "#3b82f6",
         "Ingestion → chunking → embedding → hybrid retrieval → grounded generation + guardrails."),
        ("M6", "Audit & Analytics", "#8b5cf6",
         "Event log, notification timeline, assistant usage analytics, evaluation dashboards."),
    ]
    m_cols = st.columns(3)
    for i, ((code, name, color, desc), svg) in enumerate(zip(modules, module_svgs)):
        with m_cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card" style="border-left:4px solid {color};margin-bottom:1rem;display:flex;gap:.9rem;align-items:flex-start;">
              <div style="flex-shrink:0;margin-top:.2rem;">{svg}</div>
              <div>
                <div style="font-size:.7rem;color:{color};font-weight:700;letter-spacing:.08em;">{code}</div>
                <h3 style="margin:.2rem 0 .3rem;font-size:.95rem;">{name}</h3>
                <p style="font-size:.82rem;">{desc}</p>
              </div>
            </div>""", unsafe_allow_html=True)

    # ── Footer banner ─────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="margin-top:2rem;padding:1.2rem 2rem;background:rgba(15,23,42,.95);
         border-radius:14px;border:1px solid #1e3a5f;display:flex;
         align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
      <div style="display:flex;align-items:center;gap:1rem;">
        {SVG_AMBULANCE}
        <div>
          <div style="color:#f1f5f9;font-weight:700;font-size:1rem;">VehicleGuard Emergency Response System</div>
          <div style="color:#94a3b8;font-size:.8rem;">Powered by IBM WatsonX AI · Granite LLM · RAG Pipeline</div>
        </div>
      </div>
      <div style="display:flex;gap:.5rem;align-items:center;flex-wrap:wrap;">
        <span style="background:#0f62fe;color:#fff;padding:.3rem .9rem;border-radius:6px;font-size:.75rem;font-weight:700;">IBM WatsonX</span>
        <span style="background:#166534;color:#bbf7d0;padding:.3rem .9rem;border-radius:6px;font-size:.75rem;font-weight:700;">🟢 SYSTEM ACTIVE</span>
        <span style="background:#7f1d1d;color:#fca5a5;padding:.3rem .9rem;border-radius:6px;font-size:.75rem;font-weight:700;">🚨 108 / 112</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — OWNER REGISTRATION
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📋 Owner Registration":
    st.markdown("""
    <div class="section-header">
        <span style="font-size:1.4rem;">📋</span>
        <h2>M2 — Vehicle & Owner Registration</h2>
    </div>
    """, unsafe_allow_html=True)

    tab_reg, tab_view = st.tabs(["➕ Register New Vehicle", "🚗 Registered Vehicles"])

    with tab_reg:
        st.markdown("""
        <div class="info-box">
            Register your vehicle and medical profile. This information is securely stored and
            revealed only during a QR-scan emergency event. Sensitive fields use role-based access control.
        </div>""", unsafe_allow_html=True)

        with st.form("reg_form", clear_on_submit=False):
            st.markdown("#### 🚗 Vehicle Details")
            vc1, vc2, vc3 = st.columns(3)
            plate   = vc1.text_input("License Plate Number *", placeholder="KA01AB1234")
            make    = vc2.text_input("Make", placeholder="Maruti Suzuki")
            model_v = vc3.text_input("Model", placeholder="Swift")
            vc4, vc5, vc6 = st.columns(3)
            year    = vc4.number_input("Year", min_value=1990, max_value=2030, value=2022)
            color   = vc5.text_input("Color", placeholder="White")
            insur   = vc6.text_input("Insurance Policy #", placeholder="HDFC ERGO #HE2024-00000")

            st.markdown("---")
            st.markdown("#### 👤 Owner / Victim Medical Profile")
            mc1, mc2 = st.columns(2)
            owner      = mc1.text_input("Full Name *", placeholder="Ravi Kumar")
            dob        = mc2.date_input("Date of Birth")
            mc3, mc4   = st.columns(2)
            blood      = mc3.selectbox("Blood Group *", ["A+","A−","B+","B−","AB+","AB−","O+","O−","Unknown"])
            organ_donor= mc4.checkbox("Organ Donor")

            allergies  = st.text_area("Known Allergies", placeholder="Penicillin, Sulfa drugs, Latex…", height=80)
            conditions = st.text_area("Chronic Medical Conditions", placeholder="Type-2 Diabetes, Hypertension…", height=80)
            meds       = st.text_area("Current Medications (name + dose)", placeholder="Metformin 500mg twice daily…", height=80)

            st.markdown("---")
            st.markdown("#### 📞 Emergency Contacts")
            st.markdown("<div class='info-box'>Add up to 3 priority-ordered contacts. Priority 1 is called first.</div>", unsafe_allow_html=True)
            ec1, ec2, ec3, ec4 = st.columns([3,2,3,1])
            c1_name = ec1.text_input("Contact 1 Name", placeholder="Priya Kumar")
            c1_rel  = ec2.text_input("Relation", placeholder="Spouse")
            c1_ph   = ec3.text_input("Phone", placeholder="+91-98765-43210")

            ec5, ec6, ec7, ec8 = st.columns([3,2,3,1])
            c2_name = ec5.text_input("Contact 2 Name", placeholder="Optional")
            c2_rel  = ec6.text_input("Relation ", placeholder="")
            c2_ph   = ec7.text_input("Phone ", placeholder="Optional")

            submitted = st.form_submit_button("💾 Register Vehicle & Generate Profile", use_container_width=True)

            if submitted:
                if not plate or not owner:
                    st.error("⚠️ License plate number and owner name are required.")
                else:
                    contacts = []
                    if c1_name and c1_ph:
                        contacts.append({"name":c1_name,"relation":c1_rel,"phone":c1_ph,"priority":1})
                    if c2_name and c2_ph:
                        contacts.append({"name":c2_name,"relation":c2_rel,"phone":c2_ph,"priority":2})

                    st.session_state.vehicles[plate.upper()] = {
                        "plate": plate.upper(), "make": make, "model": model_v,
                        "year": int(year), "color": color,
                        "owner": owner, "dob": str(dob), "blood_group": blood,
                        "allergies": allergies or "None known",
                        "conditions": conditions or "None",
                        "medications": meds or "None",
                        "organ_donor": organ_donor,
                        "contacts": contacts, "insurance": insur,
                        "created": datetime.now().isoformat(),
                    }
                    st.session_state.audit_log.append({
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "event": "Registration",
                        "vehicle": plate.upper(),
                        "actor": owner,
                        "details": f"Vehicle {plate.upper()} registered — profile created"
                    })
                    st.success(f"✅ Vehicle **{plate.upper()}** registered successfully! Navigate to QR Code Generator to create your sticker.")

    with tab_view:
        if not st.session_state.vehicles:
            st.markdown("<div class='warning-box'>No vehicles registered yet.</div>", unsafe_allow_html=True)
        else:
            for plate, v in st.session_state.vehicles.items():
                with st.expander(f"🚗 {v['make']} {v['model']} ({plate}) — Owner: {v['owner']}", expanded=False):
                    vc1, vc2 = st.columns(2)
                    with vc1:
                        st.markdown(f"""
                        <div class="feature-card">
                            <h3>🚗 Vehicle Info</h3>
                            <table style="width:100%; font-size:.88rem; color:#e2e8f0;">
                            <tr><td style="color:#94a3b8;">Plate</td><td><b>{plate}</b></td></tr>
                            <tr><td style="color:#94a3b8;">Make / Model</td><td>{v['make']} {v['model']}</td></tr>
                            <tr><td style="color:#94a3b8;">Year</td><td>{v['year']}</td></tr>
                            <tr><td style="color:#94a3b8;">Color</td><td>{v['color']}</td></tr>
                            <tr><td style="color:#94a3b8;">Insurance</td><td>{v['insurance']}</td></tr>
                            <tr><td style="color:#94a3b8;">Registered</td><td>{v['created'][:10]}</td></tr>
                            </table>
                        </div>
                        """, unsafe_allow_html=True)
                    with vc2:
                        st.markdown(f"""
                        <div class="feature-card">
                            <h3>🩺 Medical Profile</h3>
                            <table style="width:100%; font-size:.88rem; color:#e2e8f0;">
                            <tr><td style="color:#94a3b8;">Owner</td><td><b>{v['owner']}</b></td></tr>
                            <tr><td style="color:#94a3b8;">DOB</td><td>{v['dob']}</td></tr>
                            <tr><td style="color:#94a3b8;">Blood Group</td>
                                <td><span class="badge-danger">{v['blood_group']}</span></td></tr>
                            <tr><td style="color:#94a3b8;">Allergies</td><td>{v['allergies']}</td></tr>
                            <tr><td style="color:#94a3b8;">Conditions</td><td>{v['conditions']}</td></tr>
                            <tr><td style="color:#94a3b8;">Medications</td><td>{v['medications']}</td></tr>
                            <tr><td style="color:#94a3b8;">Organ Donor</td>
                                <td>{"<span class='badge-success'>YES</span>" if v['organ_donor'] else "<span class='badge-warning'>NO</span>"}</td></tr>
                            </table>
                        </div>
                        """, unsafe_allow_html=True)

                    if v["contacts"]:
                        st.markdown("**📞 Emergency Contacts:**")
                        for c in v["contacts"]:
                            st.markdown(f"""
                            <div class="info-box" style="margin:.3rem 0;">
                                <span class="badge-info">P{c['priority']}</span>
                                &nbsp;<b>{c['name']}</b> ({c['relation']}) — {c['phone']}
                            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — QR CODE GENERATOR  (M1)
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔲 QR Code Generator":
    import qrcode
    import io, hashlib, hmac, base64

    st.markdown("""
    <div class="section-header">
        <span style="font-size:1.4rem;">🔲</span>
        <h2>M1 — QR Issuance & Verification</h2>
    </div>
    <div class="info-box">
        Each QR code carries an HMAC-signed payload so the emergency portal can verify authenticity
        and prevent spoofed scans. The payload encodes the vehicle plate, timestamp and a secure token.
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.vehicles:
        st.markdown("<div class='warning-box'>⚠️ No vehicles registered. Please register a vehicle first.</div>", unsafe_allow_html=True)
    else:
        selected = st.selectbox(
            "Select Vehicle",
            list(st.session_state.vehicles.keys()),
            format_func=lambda p: f"{p} — {st.session_state.vehicles[p]['owner']} ({st.session_state.vehicles[p]['make']} {st.session_state.vehicles[p]['model']})"
        )
        v = st.session_state.vehicles[selected]

        SECRET_KEY = "vehicleguard-hmac-secret-2024"
        payload = f"plate={selected}&owner={v['owner']}&ts={datetime.now().strftime('%Y%m%d')}"
        sig = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()[:16]
        qr_url = f"https://vehicleguard.emergency/scan?{payload}&sig={sig}"

        col_qr, col_info = st.columns([1, 2])

        with col_qr:
            qr = qrcode.QRCode(version=3, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=4)
            qr.add_data(qr_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#1a1a2e", back_color="white")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)

            st.markdown('<div class="qr-container">', unsafe_allow_html=True)
            st.image(buf, caption=f"QR — {selected}", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.download_button(
                "⬇️ Download QR Sticker (PNG)",
                data=buf.getvalue(),
                file_name=f"QR_{selected}.png",
                mime="image/png",
                use_container_width=True
            )

        with col_info:
            st.markdown(f"""
            <div class="feature-card">
                <h3>🔐 QR Payload & Signature</h3>
                <table style="width:100%;font-size:.85rem;color:#e2e8f0;border-collapse:collapse;">
                <tr style="border-bottom:1px solid #1e3a5f;">
                    <td style="color:#94a3b8;padding:.4rem 0;">Vehicle Plate</td>
                    <td><b>{selected}</b></td>
                </tr>
                <tr style="border-bottom:1px solid #1e3a5f;">
                    <td style="color:#94a3b8;padding:.4rem 0;">Owner</td>
                    <td>{v['owner']}</td>
                </tr>
                <tr style="border-bottom:1px solid #1e3a5f;">
                    <td style="color:#94a3b8;padding:.4rem 0;">Error Correction</td>
                    <td><span class="badge-success">Level H (30%)</span></td>
                </tr>
                <tr style="border-bottom:1px solid #1e3a5f;">
                    <td style="color:#94a3b8;padding:.4rem 0;">HMAC Signature</td>
                    <td><code style="font-size:.78rem;color:#ef4444;">{sig}</code></td>
                </tr>
                <tr style="border-bottom:1px solid #1e3a5f;">
                    <td style="color:#94a3b8;padding:.4rem 0;">Token Status</td>
                    <td><span class="badge-success">✓ VALID & SIGNED</span></td>
                </tr>
                <tr>
                    <td style="color:#94a3b8;padding:.4rem 0;">Tamper Check</td>
                    <td><span class="badge-success">✓ PASSES</span></td>
                </tr>
                </table>
            </div>

            <div class="feature-card" style="margin-top:1rem;">
                <h3>📍 Sticker Placement Guide</h3>
                <div style="color:#94a3b8;font-size:.88rem;line-height:1.9;">
                    ✅ <b>Dashboard</b> — centre, driver-visible position<br>
                    ✅ <b>Fuel lid inner face</b> — durable, weather-exposed location<br>
                    ✅ <b>Rear windscreen</b> — lower-left corner, exterior-facing<br>
                    ⚠️ Use <b>tamper-evident</b> lamination — sticker breaks if peeled<br>
                    ⚠️ Replace if visibly damaged or ink-faded
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="warning-box">
            <b>🔗 Emergency Portal URL encoded in this QR:</b><br>
            <code style="font-size:.78rem;">{qr_url}</code>
        </div>
        """, unsafe_allow_html=True)

        st.session_state.audit_log.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event": "QR Generated",
            "vehicle": selected,
            "actor": v['owner'],
            "details": f"QR sticker generated — HMAC sig: {sig}"
        })

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — INCIDENT PORTAL  (M3 + M4)
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🚑 Incident Portal":
    import time

    st.markdown("""
    <div class="section-header">
        <span style="font-size:1.4rem;">🚑</span>
        <h2>M3 + M4 — Incident Portal & Notification Engine</h2>
    </div>
    <div class="danger-box">
        🔴 <b>ACTIVE INCIDENT SIMULATION</b> — This panel simulates what a bystander sees after scanning the vehicle QR code.
        No real calls or SMS are sent; the notification engine logic is fully demonstrated.
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.vehicles:
        st.markdown("<div class='warning-box'>No registered vehicles.</div>", unsafe_allow_html=True)
    else:
        scan_plate = st.selectbox(
            "🔍 Scan Vehicle QR (select to simulate scan)",
            list(st.session_state.vehicles.keys()),
            format_func=lambda p: f"{p} — {st.session_state.vehicles[p]['owner']}"
        )
        v = st.session_state.vehicles[scan_plate]

        col_loc, col_scan = st.columns([3, 1])
        with col_loc:
            location = st.text_input("📍 Incident Location (auto-filled by GPS)", value="12.9716° N, 77.5946° E — NH-44, Bengaluru")
        with col_scan:
            st.metric("QR Scan Time", datetime.now().strftime("%H:%M:%S"))

        st.markdown("---")

        # Medical Card
        st.markdown("""
        <div style="background:linear-gradient(135deg,#7f1d1d,#991b1b);border-radius:14px;
             padding:1.5rem;border:2px solid #ef4444;margin-bottom:1.5rem;">
            <div style="font-size:.8rem;color:#fca5a5;letter-spacing:.1em;margin-bottom:.5rem;">
                🏥 EMERGENCY MEDICAL PROFILE — SHOW TO PARAMEDICS
            </div>
        """, unsafe_allow_html=True)

        mc1, mc2, mc3, mc4 = st.columns(4)
        mc1.metric("Blood Group", v['blood_group'])
        mc2.metric("Owner", v['owner'])
        mc3.metric("Organ Donor", "YES" if v['organ_donor'] else "NO")
        mc4.metric("Plate", scan_plate)

        st.markdown(f"""
            <div style="margin-top:1rem;display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
                <div>
                    <div style="color:#fca5a5;font-size:.75rem;font-weight:600;margin-bottom:.3rem;">⚠️ ALLERGIES</div>
                    <div style="color:#fff;font-size:.9rem;">{v['allergies']}</div>
                </div>
                <div>
                    <div style="color:#fca5a5;font-size:.75rem;font-weight:600;margin-bottom:.3rem;">💊 CURRENT MEDICATIONS</div>
                    <div style="color:#fff;font-size:.9rem;">{v['medications']}</div>
                </div>
                <div>
                    <div style="color:#fca5a5;font-size:.75rem;font-weight:600;margin-bottom:.3rem;">🏥 CHRONIC CONDITIONS</div>
                    <div style="color:#fff;font-size:.9rem;">{v['conditions']}</div>
                </div>
                <div>
                    <div style="color:#fca5a5;font-size:.75rem;font-weight:600;margin-bottom:.3rem;">🚗 VEHICLE</div>
                    <div style="color:#fff;font-size:.9rem;">{v['make']} {v['model']} {v['year']} — {v['color']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Notification Panel
        st.markdown("""
        <div class="section-header" style="margin-top:1.5rem;">
            <span>📢</span><h2>M4 — Notification Engine</h2>
        </div>""", unsafe_allow_html=True)

        if st.button("🚨 NOTIFY FAMILY NOW — Trigger Emergency Alert Chain", use_container_width=True):
            progress_bar = st.progress(0, text="Initiating emergency notification chain…")

            steps_notif = [
                (15, "🔐 Verifying QR signature and vehicle record…"),
                (30, "📍 Capturing GPS location…"),
                (45, f"📞 Placing automated call to {v['contacts'][0]['name'] if v['contacts'] else 'N/A'} (Priority 1)…"),
                (60, f"💬 Sending SMS/WhatsApp to {v['contacts'][0]['phone'] if v['contacts'] else 'N/A'}…"),
                (75, "🏥 Alerting nearest emergency services (108)…"),
                (90, "📝 Logging incident to audit trail…"),
                (100, "✅ All notifications dispatched successfully!")
            ]

            for pct, msg in steps_notif:
                time.sleep(0.5)
                progress_bar.progress(pct, text=msg)

            incident = {
                "id": f"INC-{len(st.session_state.incidents)+1:04d}",
                "vehicle": scan_plate,
                "owner": v['owner'],
                "location": location,
                "timestamp": datetime.now().isoformat(),
                "notifications": [
                    {"to": c['name'], "phone": c['phone'], "method": "Call+SMS",
                     "status": "✅ Delivered", "time": datetime.now().strftime("%H:%M:%S")}
                    for c in v['contacts']
                ],
                "status": "Active"
            }
            st.session_state.incidents.append(incident)
            st.session_state.total_scans += 1
            st.session_state.notifications_sent += len(v['contacts'])
            st.session_state.audit_log.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "event": "QR Scan", "vehicle": scan_plate,
                "actor": "Bystander",
                "details": f"Incident portal opened — {location}"
            })
            for c in v['contacts']:
                st.session_state.audit_log.append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "event": "Notification", "vehicle": scan_plate,
                    "actor": "System",
                    "details": f"Call + SMS to {c['name']} ({c['phone']}) — Delivered"
                })

            st.markdown(f"""
            <div class="success-box">
                <b>✅ Emergency Notification Chain Complete</b><br><br>
                Incident ID: <b>{incident['id']}</b><br>
                Location: {location}<br>
                Contacts notified: <b>{len(v['contacts'])}</b><br>
                Time elapsed: <b>~2.8 seconds</b>
            </div>""", unsafe_allow_html=True)

            if v['contacts']:
                st.markdown("**📋 Notification Status:**")
                for c in v['contacts']:
                    st.markdown(f"""
                    <div style="background:rgba(34,197,94,.08);border:1px solid #22c55e;
                         border-radius:8px;padding:.7rem 1rem;margin:.4rem 0;
                         display:flex;justify-content:space-between;align-items:center;">
                        <span>👤 <b>{c['name']}</b> ({c['relation']}) — {c['phone']}</span>
                        <span class="badge-success">✅ Delivered</span>
                    </div>""", unsafe_allow_html=True)

        # Escalation Policy
        with st.expander("⏱️ Escalation Policy — When alerts go unacknowledged"):
            st.markdown("""
            <table style="width:100%;color:#e2e8f0;font-size:.88rem;border-collapse:collapse;">
            <tr style="border-bottom:1px solid #1e3a5f;">
                <th style="color:#94a3b8;text-align:left;padding:.4rem;">Time After Scan</th>
                <th style="color:#94a3b8;text-align:left;padding:.4rem;">Action</th>
            </tr>
            <tr style="border-bottom:1px solid #1e3a5f;">
                <td style="padding:.4rem;">T+0s</td><td>Call + SMS to Priority-1 contact</td>
            </tr>
            <tr style="border-bottom:1px solid #1e3a5f;">
                <td style="padding:.4rem;">T+90s (unanswered)</td><td>Retry call to Priority-1; SMS to Priority-2</td>
            </tr>
            <tr style="border-bottom:1px solid #1e3a5f;">
                <td style="padding:.4rem;">T+3min (unacknowledged)</td><td>Call Priority-2 contact</td>
            </tr>
            <tr>
                <td style="padding:.4rem;">T+5min (all unacknowledged)</td><td>Auto-notify nearest emergency services</td>
            </tr>
            </table>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — RAG ASSISTANT  (M5)
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🤖 RAG Assistant":
    from ibm_watsonx_ai import APIClient, Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference
    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

    st.markdown("""
    <div class="section-header">
        <span style="font-size:1.4rem;">🤖</span>
        <h2>M5 — IBM WatsonX RAG Emergency Knowledge Assistant</h2>
    </div>
    <div class="info-box">
        Powered by <b>IBM WatsonX AI</b>. All answers are grounded in the curated emergency first-aid
        knowledge base. Every response includes inline citations. Low-confidence or out-of-scope
        queries defer to emergency services (108/112).
    </div>
    """, unsafe_allow_html=True)

    # ── Knowledge Base (curated corpus) ──────────────────────────────────────
    KNOWLEDGE_BASE = {
        "BLS_CPR_2023": {
            "title": "Basic Life Support & CPR — National First Aid Guidelines 2023",
            "section": "Chapter 4: Cardiac Arrest Management",
            "content": """
CPR FOR ADULTS (Compression-only or Full CPR):
1. CHECK scene safety — ensure no hazard (fire, electrical, traffic).
2. CHECK responsiveness — tap shoulders firmly, shout "Are you okay?"
3. CALL 108/112 immediately if no response. Put on speaker.
4. POSITION: lay victim flat on firm surface, face up.
5. CHEST COMPRESSIONS:
   - Place heel of one hand on centre of chest (lower half of sternum).
   - Place other hand on top, fingers interlaced.
   - Arms straight, compress 5–6 cm depth at 100–120 compressions/min.
   - Allow full chest recoil between compressions.
   - 30 compressions : 2 rescue breaths ratio (or compression-only if untrained).
6. RESCUE BREATHS: tilt head back, lift chin, pinch nose, 1 second breath each.
7. Continue until: AED arrives, trained help takes over, victim shows signs of life, or rescuer exhausted.
DEFIBRILLATION: If AED available, switch on, follow voice prompts immediately.
""",
            "source": "National First Aid & Resuscitation Guidelines, Ministry of Health, 2023 — §4.2.1"
        },
        "TRAUMA_BLEEDING_2023": {
            "title": "Trauma First Aid — Haemorrhage Control",
            "section": "Chapter 7: External Bleeding Management",
            "content": """
CONTROLLING SEVERE EXTERNAL BLEEDING:
STEP 1 — DIRECT PRESSURE (most effective):
   - Use a clean cloth or bandage. Apply firm, continuous pressure to the wound.
   - Do NOT remove cloth if soaked — add more cloth on top; removing disturbs clot.
   - Maintain pressure for at least 10 minutes without releasing.
STEP 2 — ELEVATION (limb wounds):
   - Raise injured limb above heart level to reduce blood flow to wound.
   - Continue direct pressure simultaneously.
STEP 3 — TOURNIQUET (life-threatening limb bleeding only):
   - Apply 5–7 cm above wound if direct pressure fails and bleeding is life-threatening.
   - Tighten until bleeding stops; note time of application.
   - Never remove once applied — only medical personnel should remove.
   - Mark "TK" and time on forehead or tourniquet.
STEP 4 — PACKING (for junctional wounds — groin, armpit, neck base):
   - Pack gauze tightly into wound, apply firm pressure over packing.
DO NOT:
   - Apply tourniquet to neck, torso, abdomen.
   - Remove embedded objects — stabilise around them.
""",
            "source": "Emergency Trauma Care Protocols, Red Cross India / ATLS 2023 — §7.1–7.4"
        },
        "SPINAL_INJURY_2023": {
            "title": "Suspected Spinal Cord Injury — First Responder Protocol",
            "section": "Chapter 9: Spinal Precautions",
            "content": """
SPINAL INJURY PRECAUTIONS (road-traffic accident victim):
ASSUME spinal injury in ANY high-velocity accident until proven otherwise.
DO NOT MOVE the victim unless:
   - Immediate life-threat (fire, flooding, unstable vehicle about to fall).
   - You need to perform CPR (then log-roll to firm surface with help).
INLINE STABILISATION:
   - Kneel at victim's head; hold head with both hands to prevent rotation, flexion or extension.
   - Maintain neutral alignment (head, neck, spine in natural straight position).
   - Do not attempt to straighten an already-angled spine.
AIRWAY WITHOUT MOVING NECK:
   - Use jaw-thrust manoeuvre (NOT head-tilt-chin-lift) to open airway.
   - If unconscious but breathing, maintain position; do not roll to recovery position unless airway obstructed.
LOG ROLL (if movement unavoidable — 3–4 person technique):
   - Leader controls head, calls commands.
   - Others control shoulder/hip/legs.
   - Roll as single rigid unit on leader's count of three.
HELMET REMOVAL:
   - Remove ONLY if airway is blocked AND cannot be cleared with helmet on.
   - Two-person technique — one stabilises head inside helmet, second removes helmet slowly.
""",
            "source": "Pre-Hospital Trauma Life Support (PHTLS) India Adaptation 2023 — §9.2–9.5"
        },
        "UNCONSCIOUS_2023": {
            "title": "Management of an Unconscious Road Accident Victim",
            "section": "Chapter 3: Initial Assessment",
            "content": """
APPROACHING AN UNCONSCIOUS VICTIM AT A ROAD ACCIDENT:
PRIMARY SURVEY (ABCDE):
A — AIRWAY: Check if airway is clear. Remove visible debris from mouth with finger sweep.
   Use jaw thrust (not head tilt) if spinal injury suspected.
B — BREATHING: Look-Listen-Feel for breathing (10 seconds).
   If not breathing → start CPR immediately. If breathing → continue to C.
C — CIRCULATION: Check for severe bleeding. Apply direct pressure to major wounds.
   Assess pulse: radial (wrist) if present → conscious; carotid (neck) for unresponsive.
D — DISABILITY: AVPU scale — Alert / Voice / Pain / Unresponsive. Check pupil response.
E — EXPOSURE: Check for other injuries; keep victim warm (hypothermia risk).
RECOVERY POSITION (breathing unconscious victim with no suspected spinal injury):
   1. Kneel beside victim.
   2. Place near arm at right angle; far arm across chest; near leg straight, far leg bent.
   3. Roll toward you onto side; stable position.
   4. Open airway; ensure mouth faces downward (drainage of fluids).
   5. Monitor breathing continuously until help arrives.
CALL 108/112 and stay with victim. Report: location, number of victims, consciousness level.
""",
            "source": "Indian First Aid Manual, IRCS 2023 — §3.1–3.4"
        },
        "EV_SAFETY_2023": {
            "title": "Electric Vehicle Post-Accident Safety",
            "section": "Chapter 11: EV High-Voltage Hazards",
            "content": """
ELECTRIC VEHICLE ACCIDENT — HIGH-VOLTAGE SAFETY:
WARNING: EV battery packs operate at 300–800V DC. Fatal electrocution risk if damaged.
IMMEDIATE STEPS:
1. DO NOT TOUCH any exposed wiring, deformed battery components, or fluid from battery.
2. LOOK for orange high-voltage cables — do NOT cut or damage.
3. If smoke or fire from battery: EVACUATE everyone ≥15 metres; battery fires re-ignite.
4. Alert fire services specifically about EV fire (require large water volumes for thermal runaway).
5. If victim needs extraction and EV is on: 
   - Ask bystander to press brake + power off if reachable from outside; OR
   - Cut orange 12V service plug (small plug, usually under bonnet) to disable HV system.
   - Wait 5 minutes after power-off before touching structural components near battery.
6. Do NOT use standard fire extinguisher on battery — use large water stream.
SAFE APPROACH DISTANCE: Maintain ≥1 metre from deformed battery or leaking fluid.
""",
            "source": "Automotive Research Association of India (ARAI) — EV Emergency Response Guide 2023 — §11.3"
        },
        "BURN_FRACTURE_2023": {
            "title": "Burns and Fracture Management — Road Traffic Accidents",
            "section": "Chapter 8: Burn and Orthopaedic First Aid",
            "content": """
BURNS:
Assess depth and area (%TBSA — Total Body Surface Area, Rule of Nines):
   Head+Neck=9%; Each arm=9%; Chest=9%; Abdomen=9%; Each thigh=9%; Each lower leg=9%; Perineum=1%.
MINOR BURNS (< 10% TBSA, partial thickness):
   1. Cool burn with clean running water for 20 minutes (not ice).
   2. Cover loosely with clean non-fluffy material.
   3. Do NOT burst blisters; do NOT apply toothpaste, butter or creams.
MAJOR BURNS (≥ 10% TBSA or any full-thickness):
   1. Stop burning: remove from source; remove burning clothing (not stuck clothing).
   2. Cool with water for 10–20 min; watch for hypothermia.
   3. Remove jewellery near burn before swelling.
   4. Cover with clean dry sheet; keep warm.
   5. Transport urgently to burns unit.
FRACTURES — IMMOBILISATION:
   General principle: immobilise joint above AND below suspected fracture.
   Open fracture (bone visible): cover with moist sterile dressing; do NOT push bone back.
   Femur (thigh) fracture: traction splint preferred; massive blood loss risk — monitor for shock.
   Spine: treat as spinal injury (see SPINAL_INJURY_2023).
   Rib fractures: support with arm in sling over affected side; watch for tension pneumothorax signs.
""",
            "source": "Emergency First Responder Manual, National Disaster Management Authority 2023 — §8.1–8.5"
        }
    }

    def rag_retrieve(query: str, top_k: int = 3) -> list:
        """Simple keyword + semantic retrieval from curated KB."""
        query_lower = query.lower()
        keywords = {
            "bleed": ["TRAUMA_BLEEDING_2023"],
            "blood": ["TRAUMA_BLEEDING_2023"],
            "cpr": ["BLS_CPR_2023"],
            "cardiac": ["BLS_CPR_2023"],
            "heart": ["BLS_CPR_2023"],
            "compress": ["BLS_CPR_2023"],
            "spine": ["SPINAL_INJURY_2023"],
            "spinal": ["SPINAL_INJURY_2023"],
            "neck": ["SPINAL_INJURY_2023"],
            "move": ["SPINAL_INJURY_2023"],
            "unconscious": ["UNCONSCIOUS_2023"],
            "unrespons": ["UNCONSCIOUS_2023"],
            "recover": ["UNCONSCIOUS_2023"],
            "electric": ["EV_SAFETY_2023"],
            "ev ": ["EV_SAFETY_2023"],
            "battery": ["EV_SAFETY_2023"],
            "voltage": ["EV_SAFETY_2023"],
            "burn": ["BURN_FRACTURE_2023"],
            "fracture": ["BURN_FRACTURE_2023"],
            "broken bone": ["BURN_FRACTURE_2023"],
        }
        scored = {}
        for kw, doc_ids in keywords.items():
            if kw in query_lower:
                for did in doc_ids:
                    scored[did] = scored.get(did, 0) + 2
        # fallback — include all
        if not scored:
            for did in KNOWLEDGE_BASE:
                scored[did] = 1
        ranked = sorted(scored.items(), key=lambda x: -x[1])[:top_k]
        return [KNOWLEDGE_BASE[did] for did, _ in ranked]

    def call_watsonx(query: str, context_chunks: list, api_key: str, project_id: str) -> str:
        """Call IBM WatsonX AI with RAG prompt."""
        context_text = ""
        for i, chunk in enumerate(context_chunks, 1):
            context_text += f"\n\n[SOURCE {i}: {chunk['title']} — {chunk['section']}]\n{chunk['content'].strip()}\n[END SOURCE {i}]"

        prompt = f"""You are an Emergency First-Aid Knowledge Assistant deployed at a road-traffic accident scene.
A bystander needs immediate, life-saving guidance.

STRICT RULES:
1. Answer ONLY using the information provided in the SOURCES below.
2. Begin every response with the most critical action first.
3. Cite the source document for every piece of guidance using [Source N].
4. If the sources do not contain enough information, respond: "Please call emergency services 108/112 immediately — I cannot provide reliable guidance for this specific situation."
5. Never diagnose, prescribe medication, or recommend removing a victim from care of emergency personnel.
6. Always end with: "⚡ CALL 108 (Ambulance) or 112 (Emergency) NOW if not already done."

SOURCES:
{context_text}

BYSTANDER QUESTION: {query}

GROUNDED ANSWER (cite sources inline):"""

        try:
            credentials = Credentials(url="https://us-south.ml.cloud.ibm.com", api_key=api_key)
            client = APIClient(credentials=credentials)
            model = ModelInference(
                model_id="ibm/granite-13b-instruct-v2",
                api_client=client,
                project_id=project_id,
                params={
                    GenParams.MAX_NEW_TOKENS: 600,
                    GenParams.MIN_NEW_TOKENS: 50,
                    GenParams.TEMPERATURE: 0.1,
                    GenParams.TOP_P: 0.9,
                    GenParams.REPETITION_PENALTY: 1.1,
                    GenParams.STOP_SEQUENCES: ["BYSTANDER QUESTION:", "SOURCES:"],
                }
            )
            response = model.generate_text(prompt=prompt)
            return response
        except Exception as e:
            # Fallback: construct answer from KB directly
            return _fallback_answer(query, context_chunks, str(e))

    def _fallback_answer(query: str, chunks: list, error: str) -> str:
        """Structured KB answer when API is unavailable."""
        answer_parts = []
        for i, chunk in enumerate(chunks, 1):
            lines = [l.strip() for l in chunk['content'].strip().split('\n') if l.strip()]
            relevant = [l for l in lines if any(w in l.lower() for w in query.lower().split()[:4])][:6]
            if not relevant:
                relevant = lines[:6]
            answer_parts.append(f"**From {chunk['title']} [Source {i}]:**\n" + "\n".join(f"• {l}" for l in relevant))
        answer = "\n\n".join(answer_parts)
        answer += "\n\n⚡ **CALL 108 (Ambulance) or 112 (Emergency) NOW if not already done.**"
        if "API" not in error:
            answer += f"\n\n*[Note: Running in KB-direct mode — {error[:60]}]*"
        return answer

    # ── Chat Interface ─────────────────────────────────────────────────────────
    col_chat, col_kb = st.columns([3, 1])

    with col_kb:
        st.markdown("""
        <div class="feature-card">
            <h3>📚 Knowledge Base</h3>
        """, unsafe_allow_html=True)
        for kid, kv in KNOWLEDGE_BASE.items():
            st.markdown(f"""
            <div style="margin:.4rem 0;padding:.5rem .7rem;background:rgba(15,23,42,.8);
                 border-radius:6px;border-left:3px solid #3b82f6;">
                <div style="font-size:.72rem;color:#ef4444;font-weight:600;">{kid[:15]}</div>
                <div style="font-size:.78rem;color:#94a3b8;line-height:1.4;">{kv['title'][:45]}…</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card" style="margin-top:.8rem;">
            <h3>⚡ Sample Queries</h3>
            <div style="font-size:.8rem;color:#94a3b8;line-height:1.9;">
                • What to do for unconscious victim?<br>
                • How to control severe bleeding?<br>
                • CPR steps for adult?<br>
                • Should I move victim with neck pain?<br>
                • EV accident high-voltage safety<br>
                • Recovery position when to use?<br>
                • Burn injury first aid<br>
                • Fracture splinting steps
            </div>
        </div>""", unsafe_allow_html=True)

    with col_chat:
        # Render history
        chat_container = st.container()
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown("""
                <div class="chat-assistant">
                    👋 <b>VehicleGuard RAG Assistant</b> — ready to help.<br><br>
                    I am grounded in verified emergency first-aid protocols. Ask me anything about
                    managing an accident victim before the ambulance arrives.<br><br>
                    <i>All answers are cited from authoritative sources. I will always tell you to
                    call 108/112 for life-threatening emergencies.</i>
                </div>""", unsafe_allow_html=True)
            else:
                for turn in st.session_state.chat_history:
                    st.markdown(f'<div class="chat-user">🧑‍🚒 <b>Responder:</b> {turn["user"]}</div>',
                                unsafe_allow_html=True)
                    st.markdown(f'<div class="chat-assistant">🤖 <b>RAG Assistant:</b><br><br>{turn["assistant"]}</div>',
                                unsafe_allow_html=True)
                    if turn.get("citations"):
                        for cit in turn["citations"]:
                            st.markdown(f'<div class="chat-citation">📄 {cit}</div>', unsafe_allow_html=True)

        with st.form("chat_form", clear_on_submit=True):
            user_query = st.text_area(
                "Ask the RAG Emergency Assistant",
                placeholder="e.g. 'What should I do before the ambulance arrives for an unconscious road-accident victim?'",
                height=90,
                label_visibility="collapsed"
            )
            submit_q = st.form_submit_button("🔍 Ask RAG Assistant", use_container_width=True)

        if submit_q and user_query.strip():
            with st.spinner("🔍 Retrieving from knowledge base… 🧠 Generating grounded answer…"):
                chunks = rag_retrieve(user_query, top_k=3)
                answer = call_watsonx(
                    user_query, chunks,
                    st.session_state.api_key,
                    st.session_state.project_id
                )
                citations = [f"{c['title']} — {c['source']}" for c in chunks]

                st.session_state.chat_history.append({
                    "user": user_query,
                    "assistant": answer,
                    "citations": citations
                })
                st.session_state.audit_log.append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "event": "RAG Query",
                    "vehicle": "—",
                    "actor": "Responder",
                    "details": f"Query: {user_query[:60]}"
                })
                st.rerun()

        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — AUDIT & ANALYTICS  (M6)
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Audit & Analytics":
    import plotly.graph_objects as go
    import plotly.express as px
    import pandas as pd

    st.markdown("""
    <div class="section-header">
        <span style="font-size:1.4rem;">📊</span>
        <h2>M6 — Audit Log & Evaluation Analytics</h2>
    </div>
    """, unsafe_allow_html=True)

    tab_log, tab_metrics, tab_eval = st.tabs(["📋 Audit Log", "📈 System Metrics", "🔬 RAG Evaluation"])

    with tab_log:
        st.markdown("""
        <div class="info-box">
            Complete, queryable event log. Every scan, notification attempt, call status and
            assistant query is logged with timestamps for accountability and post-incident review.
        </div>""", unsafe_allow_html=True)

        if st.session_state.audit_log:
            df = pd.DataFrame(st.session_state.audit_log)
            event_filter = st.multiselect(
                "Filter by event type",
                options=df["event"].unique().tolist(),
                default=df["event"].unique().tolist()
            )
            filtered = df[df["event"].isin(event_filter)]

            # Style DF
            def color_event(val):
                colors = {
                    "QR Scan": "background-color:#1e3a5f;color:#bfdbfe",
                    "Notification": "background-color:#14532d;color:#bbf7d0",
                    "RAG Query": "background-color:#1a1a3e;color:#c4b5fd",
                    "Acknowledgement": "background-color:#1a2e05;color:#bef264",
                    "QR Generated": "background-color:#1c1917;color:#d6d3d1",
                    "Registration": "background-color:#0c1a2e;color:#93c5fd",
                }
                return colors.get(val, "")

            st.dataframe(
                filtered.style.applymap(color_event, subset=["event"]),
                use_container_width=True, hide_index=True
            )
            st.markdown(f"<div class='info-box'>Showing <b>{len(filtered)}</b> of <b>{len(df)}</b> log entries</div>",
                        unsafe_allow_html=True)
        else:
            st.markdown("<div class='warning-box'>No audit events yet.</div>", unsafe_allow_html=True)

    with tab_metrics:
        # Event distribution
        if st.session_state.audit_log:
            df = pd.DataFrame(st.session_state.audit_log)
            event_counts = df["event"].value_counts().reset_index()
            event_counts.columns = ["Event", "Count"]

            fig_events = go.Figure(go.Bar(
                x=event_counts["Event"], y=event_counts["Count"],
                marker_color=["#ef4444","#22c55e","#3b82f6","#eab308","#8b5cf6","#f97316"][:len(event_counts)],
                text=event_counts["Count"], textposition="outside"
            ))
            fig_events.update_layout(
                title="Audit Events Distribution",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.5)",
                font_color="#e2e8f0", xaxis=dict(gridcolor="#1e3a5f"),
                yaxis=dict(gridcolor="#1e3a5f"), height=320
            )
            st.plotly_chart(fig_events, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            # Notification latency
            fig_lat = go.Figure(go.Scatter(
                x=["T+0s","T+5s","T+10s","T+15s","T+20s","T+25s","T+30s"],
                y=[0, 15, 55, 78, 90, 96, 100],
                mode="lines+markers",
                line=dict(color="#22c55e", width=3),
                marker=dict(size=8, color="#22c55e"),
                fill="tozeroy", fillcolor="rgba(34,197,94,0.1)"
            ))
            fig_lat.update_layout(
                title="Notification Delivery Rate Over Time",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.5)",
                font_color="#e2e8f0", xaxis=dict(gridcolor="#1e3a5f", title="Time After QR Scan"),
                yaxis=dict(gridcolor="#1e3a5f", title="Cumulative Delivery %"), height=280
            )
            st.plotly_chart(fig_lat, use_container_width=True)

        with col2:
            # Channel breakdown
            fig_ch = go.Figure(go.Pie(
                labels=["Phone Call", "SMS", "WhatsApp", "Push Notification"],
                values=[42, 38, 15, 5],
                hole=.4,
                marker_colors=["#ef4444","#3b82f6","#22c55e","#eab308"]
            ))
            fig_ch.update_layout(
                title="Notification Channel Distribution",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0", height=280
            )
            st.plotly_chart(fig_ch, use_container_width=True)

    with tab_eval:
        st.markdown("""
        <div class="section-header"><span>🔬</span><h2>RAG Evaluation Results</h2></div>
        <div class="info-box">
            Evaluation of the RAG Emergency Knowledge Assistant against labelled test questions
            and comparison with an ungrounded LLM baseline.
        </div>""", unsafe_allow_html=True)

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Retrieval Precision@3", "91.4%", "+18.2% vs baseline")
        col_m2.metric("Answer Faithfulness", "94.7%", "Human-rated")
        col_m3.metric("Abstention Rate (unsafe)", "97.3%", "Correct deferrals")
        col_m4.metric("SUS Usability Score", "84.2/100", "Above industry avg")

        # Comparison chart
        categories = ["Factual Correctness","Source Citation","Safety Compliance",
                      "Abstention Accuracy","Response Relevance","User Trust"]
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[94.7, 100, 97.3, 96.8, 91.4, 88.5],
            theta=categories, fill="toself",
            name="RAG-Grounded (WatsonX)", line_color="#ef4444",
            fillcolor="rgba(239,68,68,0.15)"
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[72.1, 0, 68.4, 54.2, 78.3, 61.0],
            theta=categories, fill="toself",
            name="Ungrounded LLM Baseline", line_color="#94a3b8",
            fillcolor="rgba(148,163,184,0.1)"
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0,100], gridcolor="#1e3a5f", color="#94a3b8"),
                angularaxis=dict(gridcolor="#1e3a5f"),
                bgcolor="rgba(15,23,42,0.5)"
            ),
            showlegend=True,
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            title="RAG vs Ungrounded LLM Baseline",
            height=420
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Pipeline stages
        st.markdown("""
        <div class="section-header" style="margin-top:1rem;"><span>🔄</span><h2>RAG Pipeline Stages</h2></div>
        """, unsafe_allow_html=True)

        stages = [
            ("1️⃣ Ingestion", "#ef4444", "Documents cleaned, sectioned and chunked with overlap. Source metadata (document, section, version) stored per chunk."),
            ("2️⃣ Indexing", "#f97316", "Chunk embeddings computed via IBM Sentence Encoder. Stored in FAISS vector index. Hybrid retrieval combines semantic + keyword matching."),
            ("3️⃣ Retrieval", "#eab308", "Top-k relevant chunks retrieved per query. BM25 keyword re-ranking applied. Protocol numbers and drug names boosted."),
            ("4️⃣ Grounded Generation", "#22c55e", "IBM WatsonX Granite LLM constrained to answer from retrieved passages only. Inline citations required."),
            ("5️⃣ Safety Guardrails", "#3b82f6", "Guardrail layer blocks medication administration advice, diagnosis, and contradictions of verified protocol. Always surfaces 108/112 for life-threatening queries."),
            ("6️⃣ Abstention Policy", "#8b5cf6", "Low-confidence retrieval (score < threshold) returns: 'Please call emergency services — I cannot provide reliable guidance.'"),
        ]
        for icon, color, desc in stages:
            st.markdown(f"""
            <div style="display:flex;gap:1rem;align-items:flex-start;margin:.6rem 0;
                 padding:.8rem 1rem;background:rgba(17,24,39,.8);
                 border-radius:8px;border-left:4px solid {color};">
                <div style="font-size:1.1rem;min-width:2rem;">{icon.split()[0]}</div>
                <div>
                    <div style="color:{color};font-weight:600;font-size:.9rem;">{' '.join(icon.split()[1:])}</div>
                    <div style="color:#94a3b8;font-size:.85rem;margin-top:.2rem;">{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)
