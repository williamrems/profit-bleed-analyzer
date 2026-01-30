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

# --- CSS: ZERO WASTE EDITION ---
st.markdown("""
    <style>
    /* 1. AGGRESSIVE PADDING REMOVAL */
    .main .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 1rem !important; 
        max-width: 95% !important;
    }
    
    /* 2. COMPACT HEADERS */
    h1 { font-size: 1.5rem !important; margin: 0 !important; padding: 0 !important;}
    p { font-size: 0.9rem !important; margin-top: 0 !important; margin-bottom: 0.5rem !important; }
    h3 { font-size: 1.1rem !important; margin-top: 0.5rem !important; margin-bottom: 0.2rem !important; border-bottom: 1px solid #eee;}
    
    /* 3. TIGHTER WIDGETS */
    div[data-testid="stVerticalBlock"] { gap: 0.4rem !important; }
    div.stSlider { padding-top: 0rem !important; padding-bottom: 0rem !important; margin-bottom: -15px !important; }
    
    /* 4. THE BIG METRIC */
    div[data-testid="stMetricValue"] { 
        font-size: 3rem !important; 
        color: #dc2626 !important; 
        font-weight: 900; 
        line-height: 1.1;
    }
    div[data-testid="stMetricLabel"] { font-size: 0.9rem !important; font-weight: 700; }
    
    /* 5. REALITY CHECK BOXES */
    .reality-row { display: flex; gap: 0.5rem; margin-bottom: 0.5rem; }
    .reality-box { 
        background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; 
        padding: 0.5rem; flex: 1; text-align: center;
    }
    .reality-val { font-size: 1.2rem; font-weight: 800; line-height: 1; }
    .reality-lbl { font-size: 0.7rem; text-transform: uppercase; color: #64748b; font-weight: 700; }
    
    /* 6. FORM CONTAINER */
    .form-container {
        background-color: #f1f5f9;
        border-radius: 8px;
        padding: 10px 15px;
        margin-top: 10px;
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

# --- HEADER (EFFICIENT) ---
# Small column for Logo, Big for Title
c_logo, c_title = st.columns([1, 6])

with c_logo:
    try: st.image("logo.png", width=100)
    except: st.write("LOGO")

with c_title:
    st.markdown("<h1>Is Your Process Bleeding Profit?</h1>", unsafe_allow_html=True)
    st.markdown("<p>Most exterior remodelers lose 15-20% of their margin to inefficiency.</p>", unsafe_allow_html=True)

st.markdown("---") # Thin divider

# --- MAIN DASHBOARD (SPLIT 40/60) ---
col_inputs, col_results = st.columns([1, 1.3], gap="large")

# ========================
# LEFT COLUMN: INPUTS (STACKED TIGHT)
# ========================
with col_inputs:
    # Scenario Picker
    st.selectbox("📂 Load Profile:", options=list(personas.keys()), key="persona_selector", on_change=update_sliders)
    
    # SECTION 1
    st.subheader("1. Your Numbers")
    
    st.caption(f"**A. Job Volume:** {st.session_state.jobs}/mo")
    st.slider("Jobs", 1, 50, key="jobs", label_visibility="collapsed")

    st.caption(f"**B. Avg Invoice:** ${st.session_state.rev:,.0f}") 
    st.slider("Revenue", 5000, 50000, key="rev", step=500, label_visibility="collapsed")

    st.caption(f"**C. Target Margin:** {st.session_state.margin}%")
    st.slider("Margin", 5, 50, key="margin", step=1, label_visibility="collapsed")
    
    # SECTION 2
    st.subheader("2. The Chaos Factor")
    
    st.caption(f"**D. Incidents Per Job:** {st.session_state.chaos}")
    st.select_slider("Incidents", options=[0, 1, 2, 3, 4, 5], key="chaos", label_visibility="collapsed")

    st.caption(f"**E. Cost Per Incident:** ${st.session_state.cost}")
    breakdown = "IDLE CREW ($105) + FUEL ($45) + OFFICE ($30) + OPPORTUNITY ($70) = $250"
    st.slider("Cost", 50, 1000, key="cost", step=50, label_visibility="collapsed", help=breakdown)

# ==========================
# RIGHT COLUMN: RESULTS (VISUALS)
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

        # 3. REALITY CHECK (Compact Row)
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

        # 4. VERTICAL CHART (SMACKING!)
        chart_data = pd.DataFrame({'Category': ['Keep', 'Burn'], 'Amount': [max(0, actual_profit), annual_bleed]})
        color_scale = alt.Scale(domain=['Keep', 'Burn'], range=['#198754', '#dc2626'])
        
        c = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Category', title=None, axis=alt.Axis(labelAngle=0)), 
            y=alt.Y('Amount', title=None, axis=alt.Axis(format='$,.0f', grid=False)), 
            color=alt.Color('Category', scale=color_scale, legend=None),
            tooltip=['Category', 'Amount']
        ).properties(height=200) # Compact height but still vertical
        
        st.altair_chart(c, use_container_width=True)

        # 5. COMPACT FORM (Integrated)
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.caption("🛑 **Stop The Bleeding. Get the Fix.**")
        with st.form("lead_capture_form"):
            c1, c2, c3 = st.columns([1, 1, 1.5])
            with c1: st.text_input("First Name", label_visibility="collapsed", placeholder="First Name")
            with c2: st.text_input("Last Name", label_visibility="collapsed", placeholder="Last Name")
            with c3: st.text_input("Email", label_visibility="collapsed", placeholder="Email Address")
            
            st.form_submit_button("SEND ME THE REPORT >>", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.success("You claimed 0 incidents. Move the slider to see reality!")
