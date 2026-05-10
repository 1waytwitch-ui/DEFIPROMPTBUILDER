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
        font-size: 12px;
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
        padding: 10px;
        border-radius: 8px;
        margin-top: 10px;
        margin-bottom: 15px;
        font-family: monospace;
        color: #ffcc00;
        font-size: 12px;
        box-shadow: 0 0 10px rgba(255, 204, 0, 0.15);
    }

    .keyword-box {
        border: 1px solid #00ff66;
        border-radius: 6px;
        padding: 8px;
        margin-bottom: 6px;
        background-color: #050805;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title("DEFI VAULT AUTO FARM AUTO PROMPT")

# -----------------------
# CODE SECRET
# -----------------------
SECRET_CODE = st.secrets["Secret_Code"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "secret_content" not in st.session_state:
    st.session_state.secret_content = []

terminal_placeholder = st.empty()

# =========================
# TERMINAL
# =========================
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
</style>
""", unsafe_allow_html=True)

def type_line(line):
    st.session_state.secret_content.append("")
    current = ""
    for char in line:
        current += char
        st.session_state.secret_content[-1] = current
        render()
        time.sleep(0.01)

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

# =========================
# AUTH
# =========================
if not st.session_state.authenticated:

    if not st.session_state.secret_content:
        add_line("$ ACCESS PROTOCOL INITIALIZATION", glitch=True)
        add_line("> Vérification Team Élite KBOUR Crypto...")
        add_line("> Veuillez saisir le code d'accès")

    code_input = st.text_input("Code d'accès", key="secret_code", type="password")

    if st.button("Valider", use_container_width=True):
        if code_input == SECRET_CODE:
            st.session_state.authenticated = True
            st.rerun()
        else:
            add_line("> [!] CODE INCORRECT", glitch=True)
            st.error("Code incorrect")

    st.stop()

# =========================
# HEADER
# =========================
st.markdown("""
<div style='color:#00ff88; font-family:monospace; font-size:13px; margin-top:10px;'>
> ACCÈS AUTORISÉ — Bonjour et bienvenue !
</div>
""", unsafe_allow_html=True)

st.markdown("AUTO ADJUST WITH TVL")

# =========================
# INPUTS
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
⚠ <b>DISCLAIMER</b> — Outil éducatif uniquement. Aucun conseil en investissement.<br>
Le DeFi degen comporte un risque élevé de perte totale du capital (hack, rug, volatilité, smart contract).<br>
Utilisez uniquement un capital à risque avec une répartition réfléchie.
</div>
""", unsafe_allow_html=True)

# =========================
# AUTO MODE
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
## HYBRID AGGRESSIVE — CAPITAL CONCENTRATION (SMALL TVL OPTIMIZED)

---

## CONFIGURATION

### VAULT variables
* BASE_CURRENCY = {BASE_CURRENCY}

# Capital efficiency (SMALL VAULT MODE)
* MIN_TOTAL_TVL_FOR_DIVERSIFICATION = ${MIN_POOL_TVL}
* TARGET_STRATEGIES_SMALL_TVL = {max(1, max_strategies - 1)}
* TARGET_STRATEGIES_MEDIUM_TVL = {max_strategies}

# Minimum viable actions
* MIN_ACTION_VALUE = ${min_action}

---

### POOL variables
* MAX_PRICE_VOLATILITY = {MAX_VOLATILITY}%
* POOL_ACTION_TIMEFRAME = 24h
* POOL_ACTION_TIMEFRAME_TP = 4h
* APR_FRAME_SHORT = 24h
* APR_FRAME_LONG = 7d
* MIN_ELIGIBLE_APR_SHORT = {MIN_APR_24H}%
* MIN_ELIGIBLE_APR_LONG = {MIN_APR_7D}%
* MIN_POOL_TVL = ${MIN_POOL_TVL}
* MIN_POOL_VOLUME_24H = ${MIN_VOLUME_24H}
* MIN_VOLUME_TVL_RATIO = 2
* MIN_USD = ${min_action}

# Strong concentration allowed
* MAX_CAPITAL_PER_POOL_PERC = {max_capital_per_pool}%

---

### ENTRY / OUT_RANGE variables
* PRICE_IMPACT = 0.15%
* RANGE_VOL_MULT = 0.5
* MIN_POSITION_RANGE_WIDTH = 5%
* POSITION_RANGE_WIDTH = max(MIN_POSITION_RANGE_WIDTH, PriceVolatility × RANGE_VOL_MULT)
* LOWER_RANGE_PERC = POSITION_RANGE_WIDTH / 2
* UPPER_RANGE_PERC = POSITION_RANGE_WIDTH / 2

---

### HARVEST variables
* HARVEST_PERC = {HARVEST_PERC}%
* MIN_HARVEST_USD = ${min_action}

---

### EXIT variables
* STOP_LOSS_PERC = {STOP_LOSS}%
* TAKE_PROFIT_PERC = {TAKE_PROFIT}%
* STOP_LOSS_SLIPPAGE_L1 = 15%
* STOP_LOSS_SLIPPAGE_L2 = 25%

# Micro position threshold
* MIN_POSITION_VALUE = ${max(min_action * 4, 20)}

---

### DUST variables
* MIN_DUST_SWAP_USD = ${max(2, int(min_action/2))}

---

## HARD PRIORITY RULE

EXIT conditions ALWAYS override any other action.

---

## CAPITAL CONCENTRATION LOGIC

### Strategy count control

IF Vault TVL < MIN_TOTAL_TVL_FOR_DIVERSIFICATION:
    TARGET_STRATEGIES = TARGET_STRATEGIES_SMALL_TVL

ELSE:
    TARGET_STRATEGIES = TARGET_STRATEGIES_MEDIUM_TVL

---

### Dominance rule (IMPROVED)

IF one position has:
    ROI > 2x other positions
    OR APR > 1.2x other positions
THEN:
    Mark as DOMINANT

---

### Forced reallocation

IF DOMINANT exists AND multiple positions:
    EXIT weakest position
    REALLOCATE to dominant position

---

### Micro-position cleanup

IF position value < MIN_POSITION_VALUE:
    EXIT (withdraw_and_swap)

---

## TOKEN SAFETY FILTER

Reject pool if ANY:
* Token transfer tax > 2%
* Token has sell restrictions
* >40% liquidity controlled by one address
* Token age < 24h AND volume < $300k

---

## APR RELIABILITY FILTER

APR valid ONLY if:
* Based on fees
* Updated < 60 min
* Volume/TVL ≥ MIN_VOLUME_TVL_RATIO
* APR spike ≤ 5x vs 7d

---

## EXECUTION COST FILTER

Do not execute if:
* Cost > {execution_cost}% of expected gain

IF TVL < $100:
* Allow up to 25%

ALSO:
* Do not execute if action size < MIN_ACTION_VALUE

---

## TOKEN EXPOSURE LIMIT

IF TVL < $100:
    Max exposure per token = 90%
ELSE:
    Max exposure per token = 50%

---

## DECISION FRAMEWORK

1. Compute variables
2. Apply CAPITAL CONCENTRATION
3. Evaluate strategies:

   EXIT → OUT_RANGE → HARVEST → INCREASE_LIQUIDITY

4. Evaluate new:

   POOL_SELECTION → ENTRY

---

## ENTRY

Conditions:
* Pool valid
* Current strategies < TARGET_STRATEGIES

Execution:
1. swap_and_mint
2. Allocate:

   IF first position:
       {int(dominance * 100)}–100% capital

   IF second:
       remaining only IF strong diversification

Skip if:
* Size < MIN_ACTION_VALUE

---

## INCREASE_LIQUIDITY

Only if:
* No better pool
* ROI > 0%
* Position is DOMINANT

---

## HARVEST

Harvest ONLY if:
* Fees ≥ HARVEST_PERC
AND
* Fees ≥ MIN_HARVEST_USD

---

## DUST

IF TVL < $100:
* Ignore dust unless > MIN_DUST_SWAP_USD

---

## EXIT

Execute if:

### Standard:
* ROI < STOP_LOSS
* ROI ≥ TAKE_PROFIT

### Forced:
* Position < MIN_POSITION_VALUE
* Weakest vs dominant

---

## STOP-LOSS SLIPPAGE

Same logic unchanged

---

## POOL FAILURE MEMORY

Same logic unchanged
"""

# =========================
# KEYWORDS DATABASE
# =========================
keywords = {
    "1. STRUCTURE GLOBALE": [
        "CATEGORY_KEY_NAME ="
    ],

    "2. POOL SELECTION": [
        "POOL_MIN_APR_24H =",
        "POOL_MIN_APR_7D =",
        "POOL_MAX_APR_SPIKE_RATIO =",
        "POOL_MIN_TVL =",
        "POOL_MIN_VOLUME_24H =",
        "POOL_MIN_VOLUME_TVL_RATIO =",
        "POOL_MAX_VOLATILITY =",
        "POOL_MAX_DRAWDOWN_24H =",
        "POOL_MIN_FEES_24H =",
        "POOL_REQUIRE_RELIABLE_APR =",
        "POOL_REQUIRE_FEE_BASED_APR =",
        "POOL_DATA_MAX_AGE_MINUTES ="
    ],

    "3. CAPITAL MANAGEMENT": [
        "CAPITAL_BASE_CURRENCY =",
        "CAPITAL_MIN_TVL_FOR_DIVERSIFICATION =",
        "CAPITAL_TARGET_STRATEGIES_SMALL =",
        "CAPITAL_TARGET_STRATEGIES_MEDIUM =",
        "CAPITAL_TARGET_STRATEGIES_LARGE =",
        "CAPITAL_MAX_PER_POOL_PERC =",
        "CAPITAL_MAX_PER_TOKEN_PERC_SMALL =",
        "CAPITAL_MAX_PER_TOKEN_PERC_NORMAL =",
        "CAPITAL_MIN_POSITION_VALUE =",
        "CAPITAL_MIN_ACTION_VALUE ="
    ],

    "4. DOMINANCE & REALLOCATION": [
        "DOMINANCE_ENABLE =",
        "DOMINANCE_MIN_APR_RATIO =",
        "DOMINANCE_MIN_ROI_RATIO =",
        "DOMINANCE_FORCE_REALLOCATION =",
        "DOMINANCE_MIN_WINNER_ALLOCATION ="
    ],

    "5. ENTRY": [
        "ENTRY_ENABLE =",
        "ENTRY_MIN_APR_24H =",
        "ENTRY_MIN_APR_7D =",
        "ENTRY_MAX_ACTIVE_STRATEGIES =",
        "ENTRY_CAPITAL_FIRST_POSITION =",
        "ENTRY_CAPITAL_SECOND_POSITION =",
        "ENTRY_MIN_SIZE_USD =",
        "ENTRY_PRICE_IMPACT_MAX ="
    ],

    "6. INCREASE LIQUIDITY": [
        "INCREASE_ENABLE =",
        "INCREASE_ONLY_IF_NO_BETTER_POOL =",
        "INCREASE_REQUIRE_POSITIVE_ROI =",
        "INCREASE_ONLY_ON_DOMINANT =",
        "INCREASE_MIN_AMOUNT_USD ="
    ],

    "7. EXIT": [
        "EXIT_ENABLE =",
        "EXIT_STOP_LOSS =",
        "EXIT_TAKE_PROFIT =",
        "EXIT_MIN_POSITION_VALUE =",
        "EXIT_ON_APR_DROP =",
        "EXIT_MIN_APR_24H =",
        "EXIT_MIN_APR_7D =",
        "EXIT_ON_BETTER_POOL =",
        "EXIT_BETTER_POOL_APR_RATIO =",
        "EXIT_BETTER_POOL_TVL_RATIO ="
    ],

    "8. RANGE MANAGEMENT": [
        "RANGE_MIN_WIDTH =",
        "RANGE_VOL_MULTIPLIER =",
        "RANGE_ADJUST_ON_OUT =",
        "RANGE_MAX_ADJUST_PER_2H =",
        "RANGE_INCREASE_IF_TRENDING =",
        "RANGE_REDUCE_SIZE_IF_TRENDING ="
    ],

    "9. HARVEST": [
        "HARVEST_ENABLE =",
        "HARVEST_MIN_PERC =",
        "HARVEST_MIN_USD =",
        "HARVEST_REQUIRE_PROFITABLE =",
        "HARVEST_SKIP_IF_TOO_SMALL ="
    ],

    "10. DUST MANAGEMENT": [
        "DUST_ENABLE =",
        "DUST_MIN_USD =",
        "DUST_CONVERT_TO_BASE =",
        "DUST_IGNORE_IF_TVL_SMALL ="
    ],

    "11. EXECUTION / GAS / SLIPPAGE": [
        "EXECUTION_MAX_COST_RATIO =",
        "EXECUTION_MAX_COST_RATIO_SMALL_TVL =",
        "EXECUTION_MIN_ACTION_VALUE =",
        "SLIPPAGE_SWAP_MAX =",
        "SLIPPAGE_LIQUIDITY_MAX =",
        "SLIPPAGE_WITHDRAW_MAX =",
        "GAS_MAX_USD =",
        "COOLDOWN_MINUTES ="
    ],

    "12. RISK CONTROL": [
        "RISK_ENABLE_GLOBAL_KILL_SWITCH =",
        "RISK_MAX_STOP_LOSS_IN_12H =",
        "RISK_DISABLE_ENTRY_ON_TRIGGER =",
        "RISK_DISABLE_DURATION_HOURS ="
    ],

    "13. TOKEN SAFETY": [
        "TOKEN_MAX_TRANSFER_TAX =",
        "TOKEN_MAX_SINGLE_HOLDER_LIQUIDITY =",
        "TOKEN_MIN_AGE_HOURS =",
        "TOKEN_MIN_VOLUME_IF_NEW =",
        "TOKEN_REQUIRE_NO_SELL_RESTRICTIONS ="
    ],

    "BONUS : META KEYWORDS": [
        "MODE =",
        "STRATEGY_TYPE =",
        "GOAL =",
        "CHAIN =",
        "SMALL_TVL_MODE =",
        "ENABLE_CAPITAL_CONCENTRATION =",
        "ENABLE_MICRO_OPTIMIZATION ="
    ]
}

# =========================
# KEYWORDS UI
# =========================
st.markdown("## KEYWORDS LIBRARY")

for category, values in keywords.items():

    with st.expander(category):

        for item in values:

            col1, col2 = st.columns([8, 1])

            with col1:
                st.code(item)

            with col2:
                st.button(
                    "📋",
                    key=f"copy_{category}_{item}",
                    help=f"Copy {item}"
                )
