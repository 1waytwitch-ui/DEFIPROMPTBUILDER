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
import json

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

    .stCodeBlock {
        background-color: #050805 !important;
        color: #00ff66 !important;
        border: 1px solid #00ff66;
    }

    div.stButton > button {
        background-color: #001a0a;
        color: #00ff66;
        border: 1px solid #00ff66;
    }

    .compact-box {
        border: 1px solid #00ff66;
        padding: 12px;
        border-radius: 8px;
        background-color: #050805;
    }

    .warning-box {
        border: 1px solid #ffcc00;
        background-color: rgba(255, 204, 0, 0.08);
        padding: 10px;
        border-radius: 8px;
        color: #ffcc00;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title("DEFI VAULT AUTO FARM PROMPT ENGINE")

# =========================
# SECRET
# =========================
SECRET_CODE = st.secrets["Secret_Code"]

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    code = st.text_input("Access code", type="password")
    if st.button("Validate"):
        if code == SECRET_CODE:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Wrong code")
    st.stop()

# =========================
# INPUTS
# =========================
st.markdown("## CONFIGURATION")

col1, col2, col3, col4 = st.columns(4)

with col1:
    TVL = st.number_input("Vault TVL", value=60.0)
    BASE_CURRENCY = st.text_input("Base currency", "USDT")

with col2:
    MIN_APR_24H = st.number_input("Min APR 24h", value=1500)
    MIN_APR_7D = st.number_input("Min APR 7d", value=500)

with col3:
    MIN_POOL_TVL = st.number_input("Min Pool TVL", value=15000)
    MIN_VOLUME_24H = st.number_input("Min Volume 24h", value=50000)

with col4:
    MAX_VOLATILITY = st.number_input("Max volatility", value=75)
    STOP_LOSS = st.slider("Stop Loss", -50, 0, -10)

TAKE_PROFIT = st.slider("Take Profit", 5, 100, 25)
HARVEST_PERC = st.slider("Harvest %", 1, 20, 5)

# =========================
# RISK PROFILE (Suggestion 1)
# =========================
if TVL < 100:
    RISK_PROFILE = "EXTREME_SURVIVAL"
    token_exposure = 95
elif TVL < 500:
    RISK_PROFILE = "SURVIVAL"
    token_exposure = 80
elif TVL < 2000:
    RISK_PROFILE = "BALANCED"
    token_exposure = 65
else:
    RISK_PROFILE = "AGGRESSIVE"
    token_exposure = 50

# =========================
# MODE
# =========================
if TVL < 100:
    MODE = "SURVIVAL"
    max_strategies = 1
    max_capital = 100
    execution_cost = 25
    min_action = 2
    dominance = 0.90
else:
    MODE = "SCALING"
    max_strategies = 2
    max_capital = 80
    execution_cost = 15
    min_action = 5
    dominance = 0.70

# =========================
# LLM FORMAT MODE (Suggestion 6)
# =========================
FORMAT_MODE = st.selectbox(
    "LLM Format Mode",
    ["Markdown", "YAML", "JSON", "Compact"]
)

# =========================
# PRESET (Suggestion 4)
# =========================
preset = st.selectbox(
    "Strategy preset",
    ["Survival", "Balanced", "Aggressive", "Ultra Degen"]
)

# =========================
# FAILURE MEMORY (Suggestion 12)
# =========================
if "FAILED_POOLS" not in st.session_state:
    st.session_state.FAILED_POOLS = []

# =========================
# PROMPT STATE MACHINE (Suggestion 15)
# =========================
STATE_MACHINE = """
STATE = SEARCHING → ENTRY_EVALUATION → FARMING → HARVESTING → EXITING → DEFENSIVE
"""

# =========================
# PROMPT
# =========================
prompt = f"""
# AUTO-FARM ENGINE

STATE MACHINE:
{STATE_MACHINE}

---

## RISK PROFILE
RISK_PROFILE = {RISK_PROFILE}
MAX_TOKEN_EXPOSURE = {token_exposure}%

---

## CONFIG
BASE_CURRENCY = {BASE_CURRENCY}
TVL = {TVL}
MODE = {MODE}
PRESET = {preset}
FORMAT = {FORMAT_MODE}

---

## POOL RULES
MIN_APR_24H = {MIN_APR_24H}
MIN_APR_7D = {MIN_APR_7D}
MIN_POOL_TVL = {MIN_POOL_TVL}
MIN_VOLUME_24H = {MIN_VOLUME_24H}
MAX_VOLATILITY = {MAX_VOLATILITY}

---

## EXECUTION
EXECUTION_COST = {execution_cost}%
MIN_ACTION = {min_action}

---

## CAPITAL
MAX_CAPITAL_PER_POOL = {max_capital}%
DOMINANCE = {dominance}

---

## STRATEGY RULES
EXIT overrides everything.

---

## FAILURE MEMORY
FAILED_POOLS = {json.dumps(st.session_state.FAILED_POOLS)}

DO NOT REENTER FAILED_POOLS FOR 24H

---

## BEHAVIOR
- minimize unnecessary actions
- prioritize capital efficiency
- avoid low conviction trades
"""

# =========================
# DISPLAY
# =========================
st.subheader("Generated Prompt")

st.code(prompt, language="markdown")

# =========================
# KEYWORD LIBRARY (Suggestion 10 + 11)
# =========================
st.markdown("## KEYWORD LIBRARY")

keywords = {
    "STRUCTURE": ["CATEGORY_KEY_NAME ="],
    "POOL": ["POOL_MIN_APR_24H =", "POOL_MIN_TVL =", "POOL_MAX_VOLATILITY ="],
    "CAPITAL": ["CAPITAL_MAX_PER_POOL_PERC =", "CAPITAL_MIN_ACTION_VALUE ="],
    "RISK": ["RISK_ENABLE_GLOBAL_KILL_SWITCH =", "RISK_MAX_STOP_LOSS_IN_12H ="],
    "EXECUTION": ["EXECUTION_MAX_COST_RATIO =", "SLIPPAGE_SWAP_MAX ="],
    "STATE MACHINE": ["STATE = SEARCHING", "STATE = FARMING", "STATE = EXITING"]
}

for cat, items in keywords.items():
    with st.expander(cat):

        for k in items:
            col1, col2 = st.columns([10, 1])

            with col1:
                st.code(k)

            with col2:
                if st.button("📋", key=f"{cat}_{k}"):
                    st.session_state["copied"] = k
                    st.success("Copied")

# =========================
# METRICS (Suggestion 13)
# =========================
st.markdown("## AI METRICS")

entry_confidence = "HIGH" if MIN_APR_24H > 1000 else "MEDIUM"
exit_confidence = "HIGH" if STOP_LOSS > -15 else "LOW"

st.metric("ENTRY CONFIDENCE", entry_confidence)
st.metric("EXIT CONFIDENCE", exit_confidence)

st.metric("RISK PROFILE", RISK_PROFILE)
