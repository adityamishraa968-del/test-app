import streamlit as st
import numpy as np
from PIL import Image
import matplotlib
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

matplotlib.use("Agg")

FUND_RISK_MAP = {
    'Fixed Maturity / Income Funds': 1,
    'Short-Term Debt Funds': 2,
    'Hybrid Funds (Balanced)': 3,
    'Large Cap / Balanced Equity': 4,
    'Small Cap / Sectoral Funds': 5,
    'Speculative (Derivatives/Crypto)': 6,
}

IMAGE_PATH = "/mnt/data/WhatsApp Image 2025-11-23 at 16.57.13_e35090ec.jpg"

def clamp(x, a, b):
    return max(a, min(b, x))

def compute_risk_score(base, inflation, max_infl=15.0, shift_magnitude=1.8):
    shift = (inflation / max_infl) * shift_magnitude
    new_score = base - shift
    return round(clamp(new_score, 1.0, 6.0), 2)

def plt_colormap(i, n):
    if n <= 1:
        return (0.5, 0.5, 0.5)
    r = i / (n - 1)
    g = 1 - r
    b = 0.15
    return (r, g, b)

def draw_gauge(score):
    fig = Figure(figsize=(5, 3))
    ax = fig.add_subplot(111, polar=True)
    bands = 6
    for i in range(bands):
        start = np.pi - (i / bands) * np.pi
        end = np.pi - ((i + 1) / bands) * np.pi
        width = start - end
        theta = end
        ax.bar(theta, 1.0, width=width, bottom=0.0, align='edge',
               color=plt_colormap(i, bands), edgecolor='k', linewidth=0.5)

    angle = np.pi - ((score - 1) / (6 - 1)) * np.pi
    ax.plot([angle, angle], [0, 0.9], linewidth=3, color='k')
    ax.scatter([0.0], [0.0], s=60, color='k', zorder=5)

    labels = ['Low', 'Low-Mod', 'Moderate', 'Mod-High', 'High', 'Very High']
    for i, lab in enumerate(labels):
        ang = np.pi - ((i + 0.5) / bands) * np.pi
        deg = (ang - np.pi/2) * (180/np.pi)
        ax.text(ang, 1.05, lab, rotation=-deg, ha='center', va='center')

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylim(0, 1.2)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    fig.tight_layout()
    return fig

def draw_bar():
    labels = list(FUND_RISK_MAP.keys())
    vals = list(FUND_RISK_MAP.values())
    y = np.arange(len(labels))
    fig = Figure(figsize=(6, 3))
    ax = fig.add_subplot(111)
    ax.barh(y, vals)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel('Baseline Risk Level (1=Low .. 6=Very High)')
    fig.tight_layout()
    return fig

def draw_line(selected_fund):
    infl = np.linspace(0, 15, 50)
    base = FUND_RISK_MAP.get(selected_fund, 3)
    baseline_return = 6 + (base - 3) * 3
    expected_return = baseline_return - (infl * 0.6)
    fig = Figure(figsize=(6, 3))
    ax = fig.add_subplot(111)
    ax.plot(infl, expected_return)
    ax.set_xlabel('Inflation (%)')
    ax.set_ylabel('Expected Nominal Return (%)')
    ax.set_title('Simulated Inflation vs Expected Return')
    fig.tight_layout()
    return fig

def interpret_score(score):
    s = float(score)
    if s <= 1.5:
        return 'Very Low Risk: suitable for capital preservation, income funds, fixed maturity products.'
    if s <= 2.5:
        return 'Low Risk: short-term debt, conservative hybrid funds.'
    if s <= 3.5:
        return 'Moderate Risk: balanced funds, moderate equity exposure; good for medium term.'
    if s <= 4.5:
        return 'Moderate to High Risk: large-cap equity, balanced equity funds; expect volatility.'
    if s <= 5.5:
        return 'High Risk: small-cap & sectoral funds, higher volatility and higher potential returns.'
    return 'Very High Risk: speculative investments like derivatives and crypto. High potential returns and high losses.'

st.set_page_config(page_title="Risk-O-Meter", layout="wide")

st.title("Risk-O-Meter: Mutual Fund Risk & Inflation Impact")

col1, col2 = st.columns([1, 2])

with col1:
    selected_fund = st.selectbox("Select Fund Type", list(FUND_RISK_MAP.keys()))
    inflation = st.slider("Inflation Rate (%)", min_value=0.0, max_value=15.0, value=5.0, step=0.1)
    base = FUND_RISK_MAP.get(selected_fund, 3)
    risk_score = compute_risk_score(base, inflation)
    st.metric("Computed Risk Score (1-6)", f"{risk_score}")
    st.markdown("**Interpretation**")
    st.info(interpret_score(risk_score))

    try:
        img = Image.open(IMAGE_PATH)
        st.markdown("**Handwritten Notes (uploaded)**")
        st.image(img, use_column_width=True)
    except Exception as e:
        st.warning("Handwritten notes image not found at the configured path.")

with col2:
    st.markdown("### Risk Gauge")
    fig_gauge = draw_gauge(risk_score)
    st.pyplot(fig_gauge)

    st.markdown("### Baseline Risk Levels (fund types)")
    fig_bar = draw_bar()
    st.pyplot(fig_bar)

    st.markdown("### Inflation vs Expected Return (simulated)")
    fig_line = draw_line(selected_fund)
    st.pyplot(fig_line)

st.markdown("---")
st.markdown(
    "This app demonstrates how a baseline fund risk and inflation interact to produce a computed risk score. "
    "Deploy this to Streamlit Cloud by pushing this file to a GitHub repo and connecting the repo in Streamlit."
)
