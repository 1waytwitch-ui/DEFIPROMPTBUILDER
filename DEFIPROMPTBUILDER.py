import streamlit as st
import requests
import numpy as np
import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import yfinance as yf
import math
import time
import random

st.set_page_config(page_title="DeFi Vault Prompt Builder", layout="wide")

# =========================
# THEME
# =========================
st.markdown(
    """
    <style>
    body {
        background-color: #0b0f0a;
        color: #00ff66;
    }

    .stApp {
        background-color: #0b0f0a;
        color: #00ff66;
        font-family: "Courier New", monospace;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #00ff66 !important;
        text-shadow: 0px 0px 8px #00ff66;
    }

    .stTextInput input, .stNumberInput input {
        background-color: #050805 !important;
        color: #00ff66 !important;
        border: 1px solid #00ff66 !important;
    }

    .stSlider > div {
        color: #00ff66;
    }

    .stCodeBlock {
        background-color: #050805 !important;
        color: #00ff66 !important;
        border: 1px solid #00ff66;
    }

    div.stButton > button {
        background-color: #001a0a;
        color: #00ff66;
        border: 1px solid #00ff66;
        box-shadow: 0px 0px 10px #00ff66;
    }

    div.stButton > button:hover {
        background-color: #003314;
        color: #00ff66;
        box-shadow: 0px 0px 20px #00ff66;
    }

    .compact-box {
        border: 1px solid #00ff66;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 15px;
        background-color: #050805;
    }

    .warning-box {
        border: 1px solid #ffcc00;
        background-color: rgba(255, 204, 0, 0.08);
        padding: 15px;
        border-radius: 8px;
        margin-top: 15px;
        margin-bottom: 20px;
        font-family: monospace;
        color: #ffcc00;
        box-shadow: 0 0 10px rgba(255, 204, 0, 0.15);
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title("DEFI VAULT AUTO FARM AUTO PROMPT")

# -----------------------
# CODE SECRET - TERMINAL
# -----------------------
SECRET_CODE = st.secrets["Secret_Code"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "secret_content" not in st.session_state:
    st.session_state.secret_content = []

terminal_placeholder = st.empty()

# ======= RENDER ======
def render():
    terminal_placeholder.markdown(
        """
        <div id='secret-terminal' class='checklist-terminal'>
        """ + "<br>".join(st.session_state.secret_content) + """
        <span class='cursor'></span>
        </div>
        <script>
        const term = document.getElementById("secret-terminal");
        if (term) { term.scrollTop = term.scrollHeight; }
        </script>
        """,
        unsafe_allow_html=True
    )

# ======= STYLE TERMINAL ======
st.markdown("""
<style>
.checklist-terminal {
    background-color: #000000;
    border: 1px solid #00ff88;
    border-radius: 8px;
    padding: 15px;
    margin-top: 20px;
    box-shadow: 0 0 12px rgba(0,255,150,0.15);
    font-family: monospace;
    font-size: 13px;
    line-height: 1.3;
    max-height: 400px;
    overflow-y: auto;
}
.cursor {
    display: inline-block;
    width: 8px;
    background-color: #00ff88;
    margin-left: 3px;
    animation: blink 1s infinite;
}
@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0; }
    100% { opacity: 1; }
}
.stButton>button {
    background-color: black;
    color: #00ff88;
    border: 1px solid #00ff88;
    font-family: monospace;
}
</style>
""", unsafe_allow_html=True)

# ======= TYPING / GLITCH ======
def type_line(line):
    st.session_state.secret_content.append("")
    current = ""
    for char in line:
        current += char
        st.session_state.secret_content[-1] = current
        render()
        time.sleep(random.uniform(0.01, 0.01))

def subtle_glitch(line, chance=0.15):
    if not st.session_state.secret_content:
        return

    if random.random() < chance:
        chars = list("█▓▒░<>/\\|#@$%&*")
        glitched = "".join(random.choice(chars) for _ in range(len(line)))
        st.session_state.secret_content[-1] = glitched
        render()
        time.sleep(0.01)

def add_line(line, glitch=False):
    type_line(line)
    if glitch:
        subtle_glitch(line)
    time.sleep(random.uniform(0.01, 0.1))

# ======= TERMINAL AUTHENTICATION ======
if not st.session_state.authenticated:

    if not st.session_state.secret_content:
        add_line("$ ACCESS PROTOCOL INITIALIZATION", glitch=True)
        add_line("> Vérification des droits de la Team Élite KBOUR Crypto...")
        add_line("> Veuillez saisir le code d'accès ci-dessous")

    code_input = st.text_input("Code d'accès", key="secret_code", type="password")

    if st.button("Valider", use_container_width=True):
        if code_input == SECRET_CODE:
            st.session_state.authenticated = True
            st.rerun()
        else:
            add_line("> [!] CODE INCORRECT", glitch=True)
            st.error("Code incorrect")

    st.stop()

# ======= UNLOCK MESSAGE ======
st.markdown("""
<div style='color:#00ff88; font-family:monospace; font-size:13px; margin-top:10px;'>
> ACCÈS AUTORISÉ — Bonjour et bienvenue !
</div>
""", unsafe_allow_html=True)

st.markdown("AUTO ADJUST WITH TVL")

# =========================
# INPUTS COMPACTS EN HAUT
# =========================
st.markdown("### DEGEN VAULT SETTINGS")

with st.container():

    st.markdown("<div class='compact-box'>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        TVL = st.number_input("Vault TVL ($)", value=60.0)
        MIN_APR_24H = st.number_input("Min APR 24h (%)", value=1500)
        MIN_POOL_TVL = st.number_input("Min Pool TVL ($)", value=15000)

    with col2:
        BASE_CURRENCY = st.text_input("Base Currency", "USDT")
        MIN_APR_7D = st.number_input("Min APR 7d (%)", value=500)
        MIN_VOLUME_24H = st.number_input("Min Volume 24h ($)", value=50000)

    with col3:
        MAX_VOLATILITY = st.number_input("Max Volatility (%)", value=75)
        STOP_LOSS = st.slider("Stop Loss (%)", -50, 0, -10)

    with col4:
        TAKE_PROFIT = st.slider("Take Profit (%)", 5, 100, 25)
        HARVEST_PERC = st.slider("Harvest Trigger (%)", 1, 20, 5)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# DISCLAIMER
# =========================
st.markdown("""
<div class='warning-box'>
<b>⚠ DISCLAIMER :</b><br><br>

Ce générateur de stratégie DeFi est fourni uniquement à titre éducatif et expérimental.<br><br>

Il ne constitue en aucun cas un conseil en investissement, une recommandation financière ou une garantie de rendement.<br><br>

Les stratégies DeFi "degen" comportent des risques extrêmement élevés :
<ul>
<li>Perte totale du capital</li>
<li>Hack de protocole</li>
<li>Rug pull</li>
<li>Impermanent loss</li>
<li>Volatilité extrême</li>
<li>Erreurs de smart contracts</li>
</ul>

N'investissez que du capital que vous êtes prêt à perdre intégralement et utilisez toujours une répartition réfléchie de votre portefeuille.
</div>
""", unsafe_allow_html=True)

# =========================
# AUTO MODE SWITCH
# =========================
if TVL < 100:
    MODE = "SURVIVAL"
    max_strategies = 2
    max_capital_per_pool = 80
    execution_cost = 20
    min_action = 2
    dominance = 0.75

elif TVL < 500:
    MODE = "SCALING"
    max_strategies = 3
    max_capital_per_pool = 70
    execution_cost = 15
    min_action = 3
    dominance = 0.65

elif TVL < 2000:
    MODE = "OPTIMIZATION"
    max_strategies = 4
    max_capital_per_pool = 55
    execution_cost = 10
    min_action = 5
    dominance = 0.6

else:
    MODE = "AGGRESSIVE"
    max_strategies = 5
    max_capital_per_pool = 45
    execution_cost = 10
    min_action = 10
    dominance = 0.55

# =========================
# PROMPT TEMPLATE
# =========================
prompt = f"""
# AUTO-FARM INSTRUCTIONS

## HYBRID AGGRESSIVE — AUTO MODE SWITCH + CAPITAL CONCENTRATION

---

## VAULT STATE
TVL = ${TVL}
BASE_CURRENCY = {BASE_CURRENCY}
MODE = {MODE}

---

## AUTO MODE SWITCH LOGIC
IF TVL < 100: MODE = SURVIVAL
ELIF TVL < 500: MODE = SCALING
ELIF TVL < 2000: MODE = OPTIMIZATION
ELSE: MODE = AGGRESSIVE

---

## MODE PARAMETERS
MAX_ACTIVE_STRATEGIES = {max_strategies}
MAX_CAPITAL_PER_POOL = {max_capital_per_pool}%
EXECUTION_COST_LIMIT = {execution_cost}%
MIN_ACTION_VALUE = ${min_action}
DOMINANCE_ALLOCATION = {dominance}

---

## POOL FILTERS
MIN_APR_24H = {MIN_APR_24H}%
MIN_APR_7D = {MIN_APR_7D}%
MIN_POOL_TVL = ${MIN_POOL_TVL}
MIN_VOLUME_24H = ${MIN_VOLUME_24H}
MAX_VOLATILITY = {MAX_VOLATILITY}%
MIN_VOLUME_TVL_RATIO = 2

---

## ENTRY LOGIC
ONLY ENTER IF:
- APR_24H >= MIN_APR_24H
- APR_7D >= MIN_APR_7D
- TVL >= MIN_POOL_TVL
- VOLUME >= MIN_VOLUME_24H

ALLOCATION RULES:
IF FIRST POSITION: ALLOCATE {int(dominance*100)}%
IF SECOND POSITION: ALLOCATE REMAINING

---

## CAPITAL CONCENTRATION
IF: APR_TOP > 1.5x APR_SECOND THEN:
ALLOCATE >= {int(dominance*100)}% TO TOP POOL

---

## RANGE MANAGEMENT
RANGE_VOL_MULT = 0.5
MIN_RANGE_WIDTH = 5%
RANGE_WIDTH = MAX(MIN_RANGE_WIDTH, VOLATILITY * RANGE_VOL_MULT)

---

## HARVEST LOGIC
HARVEST IF:
- FEES >= {HARVEST_PERC}% OR
- FEES >= ${min_action}

IF MODE = SURVIVAL:
- DELAY HARVEST
- FAVOR COMPOUND

---

## EXIT LOGIC
STOP_LOSS = {STOP_LOSS}%
TAKE_PROFIT = {TAKE_PROFIT}%

EXIT IF:
- ROI < STOP_LOSS
- ROI >= TAKE_PROFIT
- POSITION VALUE TOO SMALL
- APR COLLAPSE

---

## DUST MANAGEMENT
IF MODE = SURVIVAL:
- MERGE ALL DUST INTO MAIN POSITION
- AVOID SWAPS
ELSE:
- CLEAN DUST NORMALLY

---

## EXECUTION FILTER
DO NOT EXECUTE IF:
COST > {execution_cost}% EXPECTED GAIN
IGNORE ACTIONS < ${min_action}

---

## BEHAVIORAL RULES
IF MODE = SURVIVAL:
- PRIORITIZE POSITION SIZE
- MINIMIZE ACTIONS
- AVOID OVER-DIVERSIFICATION

IF MODE = SCALING:
- BALANCE GROWTH AND COST

IF MODE = OPTIMIZATION:
- OPTIMIZE YIELD VS COST

IF MODE = AGGRESSIVE:
- MAXIMIZE YIELD
- ALLOW ROTATION

---

## PRIORITY
1. EXIT
2. OUT_RANGE
3. HARVEST
4. INCREASE
5. ENTRY

---

## OBJECTIVE
MAXIMIZE:
- FEES
- CAPITAL EFFICIENCY

MINIMIZE:
- GAS
- SLIPPAGE
- USELESS ACTIONS
"""

# =========================
# OUTPUT
# =========================
st.subheader(f"Detected Mode: {MODE}")
st.code(prompt, language="markdown")
