import streamlit as st

st.set_page_config(page_title="DeFi Vault Prompt Builder", layout="wide")

st.title("DeFi Auto-Farm Prompt Generator")

st.markdown("Configure ton agent IA et génère automatiquement un prompt optimisé.")

# =========================
# INPUTS
# =========================

st.sidebar.header("Core Parameters")

BASE_CURRENCY = st.sidebar.text_input("Base Currency", "USDT")

MIN_APR_24H = st.sidebar.number_input("Min APR 24h (%)", value=1500)
MIN_APR_7D = st.sidebar.number_input("Min APR 7d (%)", value=500)

MIN_POOL_TVL = st.sidebar.number_input("Min Pool TVL ($)", value=15000)
MIN_VOLUME_24H = st.sidebar.number_input("Min Volume 24h ($)", value=50000)

MAX_VOLATILITY = st.sidebar.number_input("Max Volatility (%)", value=75)

MAX_CAPITAL_PER_POOL = st.sidebar.slider("Max Capital per Pool (%)", 10, 100, 70)

MIN_POSITION_VALUE = st.sidebar.number_input("Min Position Value ($)", value=15)

HARVEST_PERC = st.sidebar.slider("Harvest Trigger (%)", 1, 20, 5)

STOP_LOSS = st.sidebar.slider("Stop Loss (%)", -50, 0, -10)
TAKE_PROFIT = st.sidebar.slider("Take Profit (%)", 5, 100, 25)

# =========================
# PROMPT TEMPLATE
# =========================

prompt = f"""
# AUTO-FARM INSTRUCTIONS
## HYBRID AGGRESSIVE — DUAL APR DRIVEN + DUST ARBITRAGE + CAPITAL CONCENTRATION

---

## CONFIGURATION

### VAULT VARIABLES
BASE_CURRENCY = {BASE_CURRENCY}

MIN_TOTAL_TVL_FOR_DIVERSIFICATION = 150
MAX_ACTIVE_STRATEGIES_SMALL_TVL = 2
MAX_ACTIVE_STRATEGIES_MEDIUM_TVL = 3

---

### POOL FILTERS

MIN_APR_24H = {MIN_APR_24H}%
MIN_APR_7D = {MIN_APR_7D}%

MIN_POOL_TVL = ${MIN_POOL_TVL}
MIN_VOLUME_24H = ${MIN_VOLUME_24H}

MAX_VOLATILITY = {MAX_VOLATILITY}%

MIN_VOLUME_TVL_RATIO = 2

---

### CAPITAL MANAGEMENT

MAX_CAPITAL_PER_POOL = {MAX_CAPITAL_PER_POOL}%

DOMINANCE_THRESHOLD = 1.5
DOMINANCE_ALLOCATION = 0.65

MIN_POSITION_VALUE = ${MIN_POSITION_VALUE}

---

### ENTRY LOGIC

ENTRY_ENABLED = TRUE

IF POOL:
- APR_24H >= MIN_APR_24H
- APR_7D >= MIN_APR_7D
- TVL >= MIN_POOL_TVL
- VOLUME >= MIN_VOLUME_24H
- VOLATILITY <= MAX_VOLATILITY

THEN:
- CREATE POSITION

ALLOCATION:
- FIRST POSITION = 60–70% CAPITAL
- SECOND POSITION = REMAINING CAPITAL

---

### RANGE MANAGEMENT

RANGE_VOL_MULT = 0.5
MIN_RANGE_WIDTH = 5%

RANGE_WIDTH = MAX(MIN_RANGE_WIDTH, VOLATILITY * RANGE_VOL_MULT)

---

### HARVEST LOGIC

HARVEST_TRIGGER = {HARVEST_PERC}%

HARVEST IF:
- FEES >= HARVEST_TRIGGER
OR
- TVL < 100 AND FEES >= $1

---

### EXIT LOGIC

STOP_LOSS = {STOP_LOSS}%
TAKE_PROFIT = {TAKE_PROFIT}%

EXIT IF:
- ROI < STOP_LOSS
- ROI >= TAKE_PROFIT
- APR DROP BELOW THRESHOLD
- POSITION < MIN_POSITION_VALUE

---

### CAPITAL CONCENTRATION

IF:
APR_TOP > 1.5x APR_SECOND

THEN:
- ALLOCATE >= 60% TO TOP POOL

---

### DUST MANAGEMENT

IF TVL < $100:
- CONVERT ALL DUST TO BASE
- OR REINJECT INTO BEST POSITION

---

### EXECUTION FILTER

DO NOT EXECUTE IF:
COST > 10% EXPECTED GAIN

IF TVL < $100:
ALLOW UP TO 20%

---

### TOKEN SAFETY

REJECT IF:
- TAX > 2%
- SELL RESTRICTIONS
- LOW LIQUIDITY CONTROL
- TOKEN TOO NEW

---

### STRATEGY PRIORITY ORDER

1. EXIT
2. OUT_RANGE
3. HARVEST
4. INCREASE_LIQUIDITY
5. ENTRY

---

### OBJECTIVE

MAXIMIZE:
- REAL YIELD (FEES)
- CAPITAL EFFICIENCY
- POSITION SIZE

MINIMIZE:
- GAS COSTS
- OVER-DIVERSIFICATION
- LOW VALUE ACTIONS

---

### MODE

HIGH_RISK + HIGH_CONCENTRATION + LOW_TVL_OPTIMIZED
"""

# =========================
# OUTPUT
# =========================

st.subheader("Generated Prompt")

st.code(prompt, language="markdown")

st.download_button(
    label="Download Prompt",
    data=prompt,
    file_name="defi_prompt.txt",
    mime="text/plain"
)
