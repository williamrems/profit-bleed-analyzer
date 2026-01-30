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

# --- CSS: THE GOLDILOCKS ZONE ---
st.markdown("""
    <style>
    /* 1. BALANCED PADDING */
    .main .block-container { 
        padding-top: 2rem !important; 
        padding-bottom: 2rem !important; 
        max-width: 90% !important;
    }
    
    /* 2. HEADERS THAT POP */
    h1 { font-size: 2.2rem !important; margin: 0 !important; font-weight: 800; color: #1e293b; }
    p { font-size: 1.1rem !important; color: #64748b; margin-top: 0.5rem; }
    h3 { font-size: 1.2rem !important; margin-top: 1rem !important; margin-bottom: 1rem !important; color: #334155; font-weight: 700;}
    
    /* 3. WIDGET SPACING (BREATHABLE) */
    div[data-testid="stVerticalBlock"] { gap: 0.8rem !important; }
    
    /* 4. THE BIG METRIC (GRAVITAS) */
    div[data-testid="stMetricValue"] { 
        font-size: 3.8rem !important; 
        color: #dc2626 !important; 
        font-weight: 900; 
        text-shadow: 2px 2px 0px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricLabel"] { font-size: 1.1rem !important; font-weight: 700; color: #64748b; }
    
    /* 5. REALITY CHECK BOXES */
    .reality-row { display: flex; gap: 15px; margin-bottom: 15px; }
    .reality-box { 
        background: #fff; border: 1px solid #cbd5e1; border-radius: 8px; 
        padding: 15px; flex: 1; text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .reality-val { font-size: 1.6rem; font-weight: 800; line-height: 1.2; }
    .reality-lbl { font-size: 0.8rem; text-transform: uppercase; color: #64748b; font-weight: 700; }
    
    /* 6. FORM CONTAINER (Professional Footer) */
    .form-container {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 20px;
        margin-top: 15px;
    }
    
    /* Center Logo vertically */
    div[data-testid="stImage"] { display: flex; align-items: center; justify-content: center; height: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIC ---
personas = {
    "Custom (Enter Your Own)": {"jobs": 8, "rev": 15000, "margin": 20, "chaos": 2, "cost": 250},
    "Chuck in a Truck": {"jobs": 4, "rev": 12000, "margin": 25, "chaos": 4, "cost": 150},
    "Growing Pains": {"jobs": 15, "rev": 18000, "margin": 20, "chaos": 3, "cost": 300},
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
    if loss_amount < 5000: return "That's a nice family vacation."
    elif loss_amount < 12000: return "That's a brand new Honda ATV."
    elif loss_amount < 25000: return "You could have bought a new Harley."
    elif loss_amount < 50000: return "You threw away a brand new F-150."
    elif loss_amount < 80000: return "That's a Project Manager's salary."
    else: return "You could have bought a vacation cabin."

# --- HEADER (CLEAN & POWERFUL) ---
c_logo, c_title = st.columns([1, 6])
with c_logo:
    try: st.image("logo.png", width=110)
    except: st.write("LOGO")
with c_title:
    st.markdown("<h1>Is Your Process Bleeding Profit?</h1>", unsafe_allow_html=True)
    st.markdown("<p>Most exterior remodelers lose 15-20% of their margin to inefficiency.</p>", unsafe_allow_html=True)

st.markdown("---")

# --- MAIN DASHBOARD (SPLIT 35/65) ---
# Giving the right column more space for the Chart to breathe
col_inputs, col_results = st.columns([1, 1.5], gap="large")

# ========================
# LEFT COLUMN: INPUTS (The Control Panel)
# ========================
with col_inputs:
    # Scenario Picker
    st.selectbox("📂 Load Profile:", options=list(personas.keys()), key="persona_selector", on_change=update_sliders)
    st.write("") # spacer

    # SECTION 1: NUMBERS
    st.markdown("### 1. Your Numbers")
    
    st.markdown(f"**A. Job Volume:** {st.session_state.jobs}/mo")
    st.slider("Jobs", 1, 50, key="jobs", label_visibility="collapsed")

    st.markdown(f"**B. Avg Invoice:** ${st.session_state.rev:,.0f}") 
    st.slider("Revenue", 5000, 50000, key="rev", step=500, label_visibility="collapsed")

    st.markdown(f"**C. Target Margin:** {st.session_state.margin}%")
    st.slider("Margin", 5, 50, key="margin", step=1, label_visibility="collapsed")
    
    st.divider()

    # SECTION 2: CHAOS
    st.markdown("### 2. The Chaos Factor")
    
    st.markdown(f"**D. Incidents Per Job:** {st.session_state.chaos}")
    st.caption("How often do crews wait, return to supply house, or fix paperwork?")
    st.select_slider("Incidents", options=[0, 1, 2, 3, 4, 5], key="chaos", label_visibility="collapsed")

    st.write("") # spacer

    st.markdown(f"**E. Cost Per Incident:** ${st.session_state.cost}")
    breakdown = "IDLE CREW ($105) + FUEL ($45) + OFFICE ($30) + OPPORTUNITY ($70) = $250"
    st.slider("Cost", 50, 1000, key="cost", step=50, label_visibility="collapsed", help=breakdown)

# ==========================
# RIGHT COLUMN: RESULTS (The Impact)
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
        
        # 2. THE ALERT
        pain = get_pain_analogy(annual_bleed)
        if annual_bleed > 20000: st.error(f"⚠️ {pain}")
        else: st.warning(f"⚠️ {pain}")

        # 3. REALITY CHECK (Side by Side)
        st.markdown(f"""
        <div class="reality-row">
            <div class="reality-box" style="border-bottom: 4px solid #dc2626;">
                <div class="reality-lbl">Profit Burned</div>
                <div class="reality-val" style="color: #dc2626;">{percent_burned:.1f}%</div>
                <div style='font-size:0.8rem; color:#94a3b8;'>of your potential</div>
            </div>
            <div class="reality-box" style="border-bottom: 4px solid #f59e0b;">
                <div class="reality-lbl">Realized Margin</div>
                <div class="reality-val" style="color: #d97706;">{realized_margin:.1f}%</div>
                <div style='font-size:0.8rem; color:#94a3b8;'>vs {st.session_state.margin}% Goal</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4. TOWER CHART (Restored Height)
        chart_data = pd.DataFrame({'Category': ['Keep', 'Burn'], 'Amount': [max(0, actual_profit), annual_bleed]})
        color_scale = alt.Scale(domain=['Keep', 'Burn'], range=['#198754', '#dc2626'])
        
        c = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Category', title=None, axis=alt.Axis(labelAngle=0)), 
            y=alt.Y('Amount', title=None, axis=alt.Axis(format='$,.0f', grid=False)), 
            color=alt.Color('Category', scale=color_scale, legend=None),
            tooltip=['Category', 'Amount']
        ).properties(height=320) # <--- THE GRAVITAS IS HERE
        
        st.altair_chart(c, use_container_width=True)

        # 5. INTEGRATED FORM
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown("**🛑 Stop The Bleeding. Get the Fix.**")
        with st.form("lead_capture_form"):
            c1, c2, c3 = st.columns([1, 1, 1.5])
            with c1: st.text_input("First Name", label_visibility="collapsed", placeholder="First Name")
            with c2: st.text_input("Last Name", label_visibility="collapsed", placeholder="Last Name")
            with c3: st.text_input("Email", label_visibility="collapsed", placeholder="Email Address")
            
            st.form_submit_button("SEND ME THE REPORT >>", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.success("You claimed 0 incidents. Move the slider to see reality!")
