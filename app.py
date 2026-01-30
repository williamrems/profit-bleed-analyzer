import streamlit as st
import pandas as pd
import altair as alt

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ContractorFlow | Profit Calculator",
    page_icon="favicon.png",
    layout="wide", 
    initial_sidebar_state="expanded" # Expanded so they see the Persona picker immediately
)

# --- CSS SURGERY (MAXIMUM TIGHTNESS) ---
st.markdown("""
    <style>
    /* Reduce main padding to almost nothing */
    .main .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    
    /* Compact Headers */
    h1 { font-size: 1.4rem !important; margin: 0 !important; }
    h3 { font-size: 1.1rem !important; margin: 0 !important; }
    p { font-size: 0.9rem !important; margin-bottom: 0.2rem !important; }
    
    /* Tighter Widget Spacing */
    div[data-testid="stVerticalBlock"] { gap: 0.3rem !important; }
    
    /* Metrics */
    div[data-testid="stMetricValue"] { font-size: 2rem !important; color: #dc2626 !important; font-weight: 900; }
    .reality-metric { font-size: 1.2rem; font-weight: 800; color: #0f172a; }
    .reality-label { font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase; }
    
    /* Form Styling - Compact */
    div[data-testid="stForm"] { border: 1px solid #e2e8f0; padding: 1rem; border-radius: 8px; background-color: #fff; }
    
    /* Center Images */
    div[data-testid="stImage"] { display: flex; justify-content: center; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { padding-top: 2rem; background-color: #f1f5f9; }
    </style>
""", unsafe_allow_html=True)

# --- PERSONA LOGIC ---
personas = {
    "Custom (Enter Your Own)": {"jobs": 8, "rev": 15000, "margin": 20, "chaos": 2, "cost": 250},
    "Chuck in a Truck (Small Owner)": {"jobs": 4, "rev": 12000, "margin": 25, "chaos": 4, "cost": 150},
    "Growing Pains (Mid-Sized)": {"jobs": 15, "rev": 18000, "margin": 20, "chaos": 3, "cost": 300},
    "Volume Player (Storm Chaser)": {"jobs": 40, "rev": 15000, "margin": 15, "chaos": 1, "cost": 250}
}

# Session State Init
if 'jobs' not in st.session_state: st.session_state['jobs'] = 8
if 'rev' not in st.session_state: st.session_state['rev'] = 15000
if 'margin' not in st.session_state: st.session_state['margin'] = 20
if 'chaos' not in st.session_state: st.session_state['chaos'] = 2
if 'cost' not in st.session_state: st.session_state['cost'] = 250

def update_sliders():
    selected = st.session_state.persona_selector
    vals = personas[selected]
    st.session_state['jobs'] = vals['jobs']
    st.session_state['rev'] = vals['rev']
    st.session_state['margin'] = vals['margin']
    st.session_state['chaos'] = vals['chaos']
    st.session_state['cost'] = vals['cost']

def get_pain_analogy(loss_amount):
    if loss_amount < 5000: return "That's a nice family vacation to Mexico."
    elif loss_amount < 12000: return "That's a brand new Honda ATV."
    elif loss_amount < 25000: return "You could have bought a new Harley."
    elif loss_amount < 50000: return "You threw away a brand new Ford F-150."
    elif loss_amount < 80000: return "That's a Project Manager's salary burned."
    else: return "You could have bought a vacation cabin."

# --- SIDEBAR (CONFIGURATION) ---
with st.sidebar:
    try: st.image("logo.png", width=150) 
    except: st.header("ContractorFlow")
    
    st.markdown("### ⚙️ Scenarios")
    st.selectbox("Load Profile:", options=list(personas.keys()), key="persona_selector", on_change=update_sliders)
    st.info("👈 Pick a profile to auto-load realistic industry numbers.")

# --- HEADER (COMPACT) ---
c1, c2 = st.columns([1, 6]) # Use columns to align text 
with c2:
    st.markdown("<h1>Is Your Process Bleeding Profit?</h1>", unsafe_allow_html=True)
    st.caption("Most exterior remodelers lose 15-20% of their margin to inefficiency. Find out your number.")

st.markdown("---")

# --- MAIN DASHBOARD (2 COLUMNS) ---
# We give the Right Column slightly more width (1.2) to accommodate the Form comfortably
col_inputs, col_results = st.columns([1, 1.2], gap="large")

# ========================
# LEFT COLUMN: INPUTS
# ========================
with col_inputs:
    st.markdown("### 1. Your Numbers")
    
    st.markdown("**A. Job Volume**")
    st.slider("Jobs/Month", 1, 50, key="jobs", label_visibility="collapsed")
    st.caption(f"Doing **{st.session_state.jobs}** jobs per month.")

    st.markdown("**B. Average Invoice (Total Job Price)**") 
    st.slider("Revenue", 5000, 50000, key="rev", step=500, format="$%d", label_visibility="collapsed")
    st.caption(f"Avg Ticket: **${st.session_state.rev:,.0f}**")

    st.markdown("**C. Target Net Profit Margin**")
    st.slider("Margin", 5, 50, key="margin", step=1, format="%d%%", label_visibility="collapsed")
    st.caption(f"Goal Margin: **{st.session_state.margin}%**")

    st.markdown("---") 
    
    st.markdown("### 2. The Chaos Factor")
    st.markdown("**D. 'Oh Sh*t' Moments Per Job**")
    st.select_slider("Incidents", options=[0, 1, 2, 3, 4, 5], key="chaos", label_visibility="collapsed")
    st.caption(f"Incidents: **{st.session_state.chaos}**")

    st.markdown("**E. Cost Per Incident**")
    breakdown = "IDLE CREW ($105) + FUEL ($45) + OFFICE ($30) + OPPORTUNITY ($70) = $250"
    st.slider("Cost", 50, 1000, key="cost", step=50, format="$%d", label_visibility="collapsed", help=breakdown)
    st.caption(f"Using **${st.session_state.cost}** per incident.")

# ==========================
# RIGHT COLUMN: RESULTS + FORM
# ==========================
with col_results:
    # Calculations
    monthly_bleed = (st.session_state.jobs * st.session_state.chaos * st.session_state.cost)
    annual_bleed = monthly_bleed * 12
    monthly_revenue = st.session_state.jobs * st.session_state.rev
    annual_revenue = monthly_revenue * 12
    potential_profit = annual_revenue * (st.session_state.margin / 100)
    actual_profit = potential_profit - annual_bleed
    
    if potential_profit > 0:
        percent_burned = (annual_bleed / potential_profit) * 100
        realized_margin = (actual_profit / annual_revenue) * 100
    else:
        percent_burned, realized_margin = 0, 0

    if st.session_state.chaos > 0:
        # 1. THE BIG NUMBER
        st.metric(label="ANNUAL PROFIT LOST", value=f"${annual_bleed:,.0f}")
        
        # 2. THE ANALOGY
        pain = get_pain_analogy(annual_bleed)
        if annual_bleed > 20000: st.error(f"⚠️ {pain}")
        else: st.warning(f"⚠️ {pain}")

        # 3. REALITY CHECK METRICS
        k1, k2 = st.columns(2)
        with k1:
            st.markdown(f"<div class='reality-label'>Profit Burned</div><div class='reality-metric' style='color:#dc2626;'>{percent_burned:.1f}%</div>", unsafe_allow_html=True)
        with k2:
            st.markdown(f"<div class='reality-label'>Realized Margin</div><div class='reality-metric' style='color:#d97706;'>{realized_margin:.1f}%</div>", unsafe_allow_html=True)

        # 4. COMPACT CHART (Height reduced to 180px)
        chart_data = pd.DataFrame({'Category': ['Keep', 'Burn'], 'Amount': [max(0, actual_profit), annual_bleed]})
        c = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Amount', title=None, axis=None), # Horizontal Bar saves vertical space!
            y=alt.Y('Category', title=None, sort=None),
            color=alt.Color('Category', scale=alt.Scale(range=['#198754', '#dc2626']), legend=None),
            tooltip=['Category', 'Amount']
        ).properties(height=100) # Ultra compact horizontal bar
        st.altair_chart(c, use_container_width=True)

    # 5. THE FORM (Now inside the Right Column!)
    st.markdown("#### Stop The Bleeding.")
    with st.form("lead_capture_form"):
        # Very compact form layout
        f1, f2 = st.columns(2)
        with f1: first_name = st.text_input("First Name")
        with f2: last_name = st.text_input("Last Name")
        email = st.text_input("Email Address") # Company name removed to save space (you can infer it from email domain often)
        
        submitted = st.form_submit_button("SEND ME THE FIX >>")

        if submitted:
            if not email: st.error("Need an email!")
            else:
                payload = {
                    "oid": "YOUR_SALESFORCE_ORG_ID_HERE",
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "00N_BLEED": annual_bleed,
                    "description": f"Persona: {st.session_state.persona_selector}"
                }
                st.success(f"Sent to {email}!")
