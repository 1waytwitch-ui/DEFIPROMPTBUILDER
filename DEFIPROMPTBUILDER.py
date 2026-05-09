import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="DeFi Prompt Builder", layout="wide")

st.title("DeFi AI Agent Prompt Builder")

# -----------------------------
# SIDEBAR - MODES
# -----------------------------
st.sidebar.header("Strategy Mode")

mode = st.sidebar.selectbox(
    "Select Mode",
    ["CUSTOM", "SAFE", "BALANCED", "AGGRESSIVE", "SNIPER"]
)

# Presets
def load_mode(mode):
    if mode == "SAFE":
        return {
            "apr_24h": 800,
            "apr_7d": 300,
            "tvl": 50000,
            "strategies": 2,
            "max_alloc": 50,
            "slippage": 1,
            "gas": 2,
        }
    elif mode == "BALANCED":
        return {
            "apr_24h": 1200,
            "apr_7d": 600,
            "tvl": 25000,
            "strategies": 2,
            "max_alloc": 70,
            "slippage": 2,
            "gas": 2,
        }
    elif mode == "AGGRESSIVE":
        return {
            "apr_24h": 1500,
            "apr_7d": 500,
            "tvl": 15000,
            "strategies": 2,
            "max_alloc": 90,
            "slippage": 2,
            "gas": 2,
        }
    elif mode == "SNIPER":
        return {
            "apr_24h": 2500,
            "apr_7d": 1000,
            "tvl": 10000,
            "strategies": 1,
            "max_alloc": 100,
            "slippage": 3,
            "gas": 3,
        }
    else:
        return None

preset = load_mode(mode)

# -----------------------------
# INPUTS
# -----------------------------
st.header("Strategy Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    apr_24h = st.slider(
        "Min APR 24h (%)", 500, 5000,
        preset["apr_24h"] if preset else 1500
    )
    apr_7d = st.slider(
        "Min APR 7d (%)", 100, 3000,
        preset["apr_7d"] if preset else 500
    )
    tvl = st.number_input(
        "Min Pool TVL ($)",
        value=preset["tvl"] if preset else 15000
    )

with col2:
    strategies = st.selectbox(
        "Max Strategies",
        [1, 2, 3],
        index=[1,2,2][strategies-1] if preset else 1
    )
    max_alloc = st.slider(
        "Max Capital per Pool (%)",
        50, 100,
        preset["max_alloc"] if preset else 100
    )
    min_position = st.slider("Min Position Value ($)", 10, 50, 20)

with col3:
    slippage = st.slider(
        "Slippage (%)",
        1, 5,
        preset["slippage"] if preset else 2
    )
    gas = st.slider(
        "Max Gas ($)",
        1, 5,
        preset["gas"] if preset else 2
    )
    harvest_min = st.slider("Min Harvest ($)", 1, 10, 2)

# Advanced
st.header("Advanced Options")

col4, col5 = st.columns(2)

with col4:
    dominance = st.checkbox("Enable Dominance Logic", True)
    dust = st.checkbox("Enable Dust Cleanup", True)

with col5:
    auto_realloc = st.checkbox("Auto Reallocation", True)
    strict_execution = st.checkbox("Strict Cost Control", True)

# -----------------------------
# BUILD CONFIG
# -----------------------------
def build_config():
    return {
        "POOL_MIN_APR_24H": apr_24h,
        "POOL_MIN_APR_7D": apr_7d,
        "POOL_MIN_TVL": tvl,
        "CAPITAL_MAX_PER_POOL_PERC": max_alloc,
        "CAPITAL_TARGET_STRATEGIES": strategies,
        "CAPITAL_MIN_POSITION_VALUE": min_position,
        "SLIPPAGE_SWAP_MAX": slippage,
        "GAS_MAX_USD": gas,
        "HARVEST_MIN_USD": harvest_min,
    }

# -----------------------------
# PROMPT TEMPLATE
# -----------------------------
def generate_prompt(config):
    dominance_block = ""
    if dominance:
        dominance_block = f"""
DOMINANCE_ENABLE = true
DOMINANCE_MIN_APR_RATIO = 1.2
DOMINANCE_MIN_ROI_RATIO = 2
DOMINANCE_FORCE_REALLOCATION = {str(auto_realloc).lower()}
"""

    dust_block = ""
    if dust:
        dust_block = """
DUST_ENABLE = true
DUST_MIN_USD = 3
"""

    execution_block = f"""
EXECUTION_MAX_COST_RATIO = {25 if strict_execution else 40}%
EXECUTION_MIN_ACTION_VALUE = 5
"""

    prompt = f"""
# AUTO GENERATED DEFI PROMPT

## POOL SELECTION
POOL_MIN_APR_24H = {config['POOL_MIN_APR_24H']}%
POOL_MIN_APR_7D = {config['POOL_MIN_APR_7D']}%
POOL_MIN_TVL = {config['POOL_MIN_TVL']}

## CAPITAL MANAGEMENT
CAPITAL_MAX_PER_POOL_PERC = {config['CAPITAL_MAX_PER_POOL_PERC']}%
CAPITAL_TARGET_STRATEGIES = {config['CAPITAL_TARGET_STRATEGIES']}
CAPITAL_MIN_POSITION_VALUE = {config['CAPITAL_MIN_POSITION_VALUE']}

## EXECUTION
SLIPPAGE_SWAP_MAX = {config['SLIPPAGE_SWAP_MAX']}%
GAS_MAX_USD = {config['GAS_MAX_USD']}

## HARVEST
HARVEST_MIN_USD = {config['HARVEST_MIN_USD']}

{dominance_block}

{dust_block}

{execution_block}
"""
    return prompt

# -----------------------------
# GENERATE BUTTON
# -----------------------------
if st.button("Generate Prompt"):
    config = build_config()
    prompt = generate_prompt(config)

    st.subheader("Generated Prompt")
    st.code(prompt, language="text")

    st.download_button(
        label="Download Prompt",
        data=prompt,
        file_name="defi_prompt.txt",
        mime="text/plain"
    )
