import streamlit as st

st.set_page_config(page_title="DeFi Vault Prompt Builder", layout="wide")

# =========================
# THEME TERMINAL GREEN
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

    .stSidebar {
        background-color: #050805;
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

    </style>
    """,
    unsafe_allow_html=True
)

st.title("DeFi Auto-Farm Prompt Generator (Auto Mode)")
st.markdown("Génération automatique avec adaptation dynamique selon le TVL.")

# =========================
# INPUTS
# =========================
st.sidebar.header("Vault State")

TVL = st.sidebar.number_input("Vault TVL ($)", value=60.0)
BASE_CURRENCY = st.sidebar.text_input("Base Currency", "USDT")
MIN_APR_24H = st.sidebar.number_input("Min APR 24h (%)", value=1500)
MIN_APR_7D = st.sidebar.number_input("Min APR 7d (%)", value=500)
MIN_POOL_TVL = st.sidebar.number_input("Min Pool TVL ($)", value=15000)
MIN_VOLUME_24H = st.sidebar.number_input("Min Volume 24h ($)", value=50000)
MAX_VOLATILITY = st.sidebar.number_input("Max Volatility (%)", value=75)
STOP_LOSS = st.sidebar.slider("Stop Loss (%)", -50, 0, -10)
TAKE_PROFIT = st.sidebar.slider("Take Profit (%)", 5, 100, 25)
HARVEST_PERC = st.sidebar.slider("Harvest Trigger (%)", 1, 20, 5)

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

)
