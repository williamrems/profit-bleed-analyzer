import streamlit as st
import pandas as pd
import altair as alt

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ContractorFlow | Profit Calculator",
    page_icon="favicon.png",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- CSS: THE "GRAVITAS" TWEAKS ---
st.markdown("""
    <style>
    /* 1. Tighten the top, give room at bottom */
    .main .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; }
    
    /* 2. Make the Main Number SCARY big */
    div[data-testid="stMetricValue"] { 
        font-size: 3.5rem !important; 
        color: #dc2626 !important; 
        font-weight: 900; 
        text-shadow: 0px 0px 0px;
    }
    div[data-testid="stMetricLabel"] { font-size: 1.1rem !important; font-weight: 700; }
    
    /* 3. The "Reality Check" Sub-metrics */
    .reality-row { display: flex; gap: 1rem; margin-bottom: 1rem; }
    .reality-box { 
        background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; 
        padding: 0.8rem; flex: 1; text-align: center;
    }
    .reality-val { font-size: 1.4rem; font-weight: 800; line-height: 1; }
    .reality-lbl { font-size: 0.75rem; text-transform: uppercase; color: #64748b; font-weight: 700; margin-bottom: 4px; }
    
    /* 4. Form Container - Clean & Integrated */
    .form-container {
        border-top: 2px dashed #cbd5e1;
        margin-top: 1rem;
        padding-top: 1rem;
    }
    
    /* 5. Header adjustments */
    h1 { font-size: 1.8rem !important; margin: 0; }
    p { font-size: 0.95rem; color: #64748b; margin-top: 0.2rem; }
    
    /* 6. Center Images */
    div[data-testid="stImage"] { display: flex; justify-content: center; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIC ---
personas = {
    "Custom (Enter Your Own)": {"jobs": 8, "rev": 15000, "margin": 20, "chaos": 2, "cost": 250},
    "Chuck in a Truck": {"jobs": 4, "rev": 12000, "margin": 25, "chaos": 4, "cost": 150},
    "Growing Pains (Mid-Sized)": {"jobs": 15, "rev": 18000, "margin": 20, "chaos": 3, "cost": 300},
    "Volume Player": {"jobs": 40, "rev": 15000, "margin": 15, "chaos": 1, "cost": 250}
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

# --- HEADER (COMPACT & CENTERED) ---
c1, c2, c3 = st.columns([1, 6, 1])
with c2:
    st.markdown("<h1 style='text-align: center;'>Is Your Process Bleeding Profit?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Most exterior remodelers lose 15-20% of their margin to inefficiency. Find out your number.</p>", unsafe_allow_html=True)
st.divider()

# --- MAIN DASHBOARD (SPLIT 40/60) ---
col_inputs, col_results = st.columns([1, 1.3], gap="large")

# ========================
# LEFT COLUMN: INPUTS
# ========================
with col_inputs:
    # 1. SCENARIO PICKER (Top of Inputs)
    st.selectbox("📂 Load a Profile (Optional):", options=list(personas.keys()), key="persona_selector", on_change=update_sliders)
    st.write("") # tiny spacer

    # 2. JOB DATA
    st.subheader("1. Your Numbers")
    st.markdown("**A. Job Volume**")
    st.slider("Jobs/Month", 1, 50, key="jobs", label_visibility="collapsed")
    st.caption(f"Doing **{st.session_state.jobs}** jobs per month.")

    st.markdown("**B. Average Invoice**") 
    st.slider("Revenue", 5000, 50000, key="rev", step=500, format="$%d", label_visibility="collapsed")
    st.caption(f"Avg Ticket: **${st.session_state.rev:,.0f}**")

    st.markdown("**C. Target Net Profit Margin**")
    st.slider("Margin", 5, 50, key="margin", step=1, format="%d%%", label_visibility="collapsed")
    st.caption(f"Goal Margin: **{st.session_state.margin}%**")

    st.divider() 
    
    # 3. CHAOS DATA
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
        # A. THE BIG NUMBER
        st.metric(label="ANNUAL PROFIT LOST", value=f"${annual_bleed:,.0f}")
        
        # B. THE ANALOGY (Full Width Alert)
        pain = get_pain_analogy(annual_bleed)
        if annual_bleed > 20000: st.error(f"⚠️ {pain}")
        else: st.warning(f"⚠️ {pain}")

        # C. REALITY CHECK ROW (Side by Side)
        st.markdown(f"""
        <div class="reality-row">
            <div class="reality-box">
                <div class="reality-lbl">Profit Burned</div>
                <div class="reality-val" style="color: #dc2626;">{percent_burned:.1f}%</div>
            </div>
            <div class="reality-box">
                <div class="reality-lbl">Realized Margin</div>
                <div class="reality-val" style="color: #d97706;">{realized_margin:.1f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # D. THE VERTICAL CHART (THE GRAVITAS IS BACK)
        chart_data = pd.DataFrame({'Category': ['Money You Keep', 'Money You Burn'], 'Amount': [max(0, actual_profit), annual_bleed]})
        color_scale = alt.Scale(domain=['Money You Keep', 'Money You Burn'], range=['#198754', '#dc2626'])
        
        c = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Category', title=None, axis=alt.Axis(labelAngle=0)), # Vertical Bars
            y=alt.Y('Amount', title='Annual Dollars', axis=alt.Axis(format='$,.0f')), 
            color=alt.Color('Category', scale=color_scale, legend=None),
            tooltip=['Category', 'Amount']
        ).properties(height=220) # Taller chart for impact
        
        st.altair_chart(c, use_container_width=True)

        # E. THE FORM (Integrated at bottom)
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown("##### 🛑 Stop The Bleeding.")
        with st.form("lead_capture_form"):
            f1, f2 = st.columns(2)
            with f1: first_name = st.text_input("First Name")
            with f2: last_name = st.text_input("Last Name")
            email = st.text_input("Email Address")
            
            submitted = st.form_submit_button("SEND ME THE FIX >>")

            if submitted:
                if not email: st.error("Need an email!")
                else: st.success(f"Report sent to {email}!")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.success("You claimed 0 incidents. Move the slider to see reality!")
