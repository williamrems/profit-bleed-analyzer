import streamlit as st
import pandas as pd
import altair as alt

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ContractorFlow | Profit Calculator",
    page_icon="favicon.png",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- CSS POLISH (RELAXED & FIXED) ---
st.markdown("""
    <style>
    /* 1. Less Aggressive Top Padding (Give it some headroom) */
    .main .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
    
    /* 2. Relaxed Widget Spacing (No longer cramped) */
    div[data-testid="stVerticalBlock"] { gap: 1rem !important; }
    
    /* 3. Header Styling */
    h1 { font-size: 1.8rem !important; margin: 0 !important; }
    p { font-size: 1rem !important; color: #64748b; }
    
    /* 4. The BIG Metric */
    div[data-testid="stMetricValue"] { font-size: 2.5rem !important; color: #dc2626 !important; font-weight: 900; }
    
    /* 5. Custom Reality Metrics (Fixed Cropping) */
    .reality-box {
        background-color: #f8fafc;
        border-radius: 8px;
        padding: 10px;
        border-left: 4px solid #cbd5e1;
        margin-bottom: 10px;
    }
    .reality-label { font-size: 0.85rem; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
    .reality-value { font-size: 1.5rem; font-weight: 800; line-height: 1.2; }
    .reality-sub { font-size: 0.8rem; color: #94a3b8; }
    
    /* 6. Form Styling */
    div[data-testid="stForm"] { 
        border: 1px solid #e2e8f0; 
        padding: 1.5rem; 
        border-radius: 12px; 
        background-color: #ffffff; 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Center Images */
    div[data-testid="stImage"] { display: flex; justify-content: center; }
    
    /* Sidebar Background */
    section[data-testid="stSidebar"] { background-color: #f8fafc; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIC & SETUP ---
personas = {
    "Custom (Enter Your Own)": {"jobs": 8, "rev": 15000, "margin": 20, "chaos": 2, "cost": 250},
    "Chuck in a Truck (Small Owner)": {"jobs": 4, "rev": 12000, "margin": 25, "chaos": 4, "cost": 150},
    "Growing Pains (Mid-Sized)": {"jobs": 15, "rev": 18000, "margin": 20, "chaos": 3, "cost": 300},
    "Volume Player (Storm Chaser)": {"jobs": 40, "rev": 15000, "margin": 15, "chaos": 1, "cost": 250}
}

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

# --- SIDEBAR ---
with st.sidebar:
    try: st.image("logo.png", width=150) 
    except: st.header("ContractorFlow")
    
    st.markdown("### ⚙️ Scenarios")
    st.selectbox("Load Profile:", options=list(personas.keys()), key="persona_selector", on_change=update_sliders)
    st.info("👈 **Start Here:** Pick a profile to see realistic numbers, then tweak them.")

# --- HEADER ---
c1, c2 = st.columns([1, 8]) 
with c2:
    st.markdown("<h1>Is Your Process Bleeding Profit?</h1>", unsafe_allow_html=True)
    st.markdown("<p>Most exterior remodelers lose 15-20% of their margin to inefficiency. Find out your number.</p>", unsafe_allow_html=True)

st.write("") # Spacer

# --- MAIN DASHBOARD ---
# Increased gap to 'large' for better separation
col_inputs, col_results = st.columns([1, 1.2], gap="large")

# ========================
# LEFT COLUMN: INPUTS
# ========================
with col_inputs:
    st.subheader("1. Your Numbers")
    
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
    
    st.subheader("2. The Chaos Factor")
    st.markdown("**D. 'Oh Sh*t' Moments Per Job**")
    st.select_slider("Incidents", options=[0, 1, 2, 3, 4, 5], key="chaos", label_visibility="collapsed")
    st.caption(f"Incidents: **{st.session_state.chaos}**")

    st.markdown("**E. Cost Per Incident**")
    breakdown = "IDLE CREW ($105) + FUEL ($45) + OFFICE ($30) + OPPORTUNITY ($70) = $250"
    st.slider("Cost", 50, 1000, key="cost", step=50, format="$%d", label_visibility="collapsed", help=breakdown)
    st.caption(f"Using **${st.session_state.cost}** per incident.")

# ==========================
# RIGHT COLUMN: RESULTS
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

        # 3. REALITY CHECK METRICS (New CSS Grid Layout)
        # This prevents the cropping issues by using styled divs instead of st.columns
        st.markdown(f"""
        <div style="display: flex; gap: 15px; margin-top: 10px; margin-bottom: 20px;">
            <div class="reality-box" style="flex: 1; border-left-color: #dc2626;">
                <div class="reality-label">Profit Burned</div>
                <div class="reality-value" style="color: #dc2626;">{percent_burned:.1f}%</div>
                <div class="reality-sub">of profit is gone</div>
            </div>
            <div class="reality-box" style="flex: 1; border-left-color: #f59e0b;">
                <div class="reality-label">Realized Margin</div>
                <div class="reality-value" style="color: #d97706;">{realized_margin:.1f}%</div>
                <div class="reality-sub">vs {st.session_state.margin}% Goal</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4. CHART (FIXED COLORS)
        chart_data = pd.DataFrame({'Category': ['Money You Keep', 'Money You Burn'], 'Amount': [max(0, actual_profit), annual_bleed]})
        
        # Explicitly map 'Money You Keep' to Green and 'Money You Burn' to Red
        color_scale = alt.Scale(domain=['Money You Keep', 'Money You Burn'], range=['#198754', '#dc2626'])
        
        c = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Amount', title=None, axis=None, stack='normalize'), # Stacked bar 100% width
            color=alt.Color('Category', scale=color_scale, legend=None),
            tooltip=['Category', 'Amount']
        ).properties(height=60) # Sleek horizontal bar
        
        st.altair_chart(c, use_container_width=True)

        # 5. THE FORM
        st.markdown("#### Stop The Bleeding.")
        with st.form("lead_capture_form"):
            f1, f2 = st.columns(2)
            with f1: first_name = st.text_input("First Name")
            with f2: last_name = st.text_input("Last Name")
            email = st.text_input("Email Address")
            
            submitted = st.form_submit_button("SEND ME THE FIX >>")

            if submitted:
                if not email: st.error("Need an email!")
                else:
                    st.success(f"Report sent to {email}!")
    else:
        st.success("You claimed 0 incidents. Move the slider to see reality!")
