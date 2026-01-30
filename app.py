import streamlit as st
import pandas as pd
import altair as alt

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ContractorFlow | Profit Bleed",
    page_icon="favicon.png",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- CSS: PERFECT BALANCE & CLEAN FORM ---
st.markdown("""
    <style>
    /* 1. RESET STREAMLIT PADDING */
    .main .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 1rem !important; 
        max-width: 95% !important;
    }
    
    /* 2. HEADER GRID */
    .header-wrapper {
        display: grid;
        grid-template-columns: auto 1fr;
        align-items: center;
        gap: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    
    /* 3. WIDGET SPACING */
    div[data-testid="stVerticalBlock"] { gap: 0.6rem !important; }
    div.stSlider { padding-top: 0px !important; padding-bottom: 10px !important; }
    
    /* 4. THE BIG METRIC (CENTERED) */
    .big-metric-container {
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-label {
        font-size: 0.9rem;
        font-weight: 700;
        color: #64748b;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 3.8rem;
        font-weight: 900;
        color: #dc2626;
        line-height: 1.0;
        text-shadow: 2px 2px 0px rgba(0,0,0,0.05);
    }
    .metric-sub {
        font-size: 1.1rem;
        font-weight: 700;
        color: #dc2626;
        background-color: #fee2e2;
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 5px;
    }
    
    /* 5. TWIN SCORECARDS */
    .card-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin-bottom: 20px;
    }
    .score-card {
        background: #fff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 100px;
    }
    
    /* RED CARD (PAIN) */
    .card-red { border-bottom: 4px solid #dc2626; }
    .card-red .card-val { font-size: 1.1rem; font-weight: 700; color: #dc2626; line-height: 1.3; }
    .card-red .card-lbl { font-size: 0.7rem; text-transform: uppercase; color: #94a3b8; font-weight: 700; margin-bottom: 5px; }

    /* ORANGE CARD (MARGIN) */
    .card-orange { border-bottom: 4px solid #f59e0b; }
    .card-orange .card-val { font-size: 1.8rem; font-weight: 800; color: #d97706; }
    .card-orange .card-lbl { font-size: 0.7rem; text-transform: uppercase; color: #94a3b8; font-weight: 700; margin-bottom: 5px; }
    .card-orange .card-sub { font-size: 0.75rem; color: #64748b; }
    
    /* 6. CLEAN FORM STYLING (THE FIX) */
    /* Target the Streamlit Form directly to avoid double-borders */
    div[data-testid="stForm"] {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 20px; /* Separation from chart */
    }

    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- CRASS PERSONAS ---
personas = {
    "Select a Profile...": {"jobs": 8, "rev": 15000, "margin": 20, "chaos": 2, "cost": 250},
    "Chuck in a Truck (Solo & Stressed)": {"jobs": 4, "rev": 12000, "margin": 25, "chaos": 4, "cost": 150},
    "The 'Napkin Math' O.G. (Old School)": {"jobs": 10, "rev": 14000, "margin": 30, "chaos": 3, "cost": 200},
    "The Sales God (Great Sales, Sh*t Ops)": {"jobs": 20, "rev": 18000, "margin": 25, "chaos": 4, "cost": 350},
    "The Storm Chaser (Burn & Turn)": {"jobs": 50, "rev": 15000, "margin": 15, "chaos": 2, "cost": 300},
    "The 'We'll Fix It Later' Crew": {"jobs": 12, "rev": 16000, "margin": 18, "chaos": 5, "cost": 400}
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

# --- THE 2026 PRICE CHECK ---
def get_pain_analogy(loss_amount):
    if loss_amount < 5000: return "Basically your beer money for the year."
    elif loss_amount < 12000: return "You burned a decent used side-by-side."
    elif loss_amount < 20000: return "That's a nice used Harley you don't have."
    elif loss_amount < 35000: return "You threw away a used work truck."
    elif loss_amount < 55000: return "You torched a brand new F-150 XL."
    elif loss_amount < 85000: return "That's a fully loaded F-250 Platinum gone."
    elif loss_amount < 120000: return "That's a down payment on a lake house."
    else: return "You are literally working for free."

# --- SLIDER ROASTS ---
def get_chaos_commentary(level):
    if level == 0: return "You're lying. No one is this perfect."
    if level == 1: return "1 Home Depot run per job. Manageable."
    if level == 2: return "Forgot materials twice? That's expensive."
    if level == 3: return "You're at Menards more than the roof."
    if level == 4: return "Your crew is getting paid to sit in the truck."
    if level == 5: return "Total Dumpster Fire. You are working for free."
    return ""

# --- HEADER ---
c1, c2 = st.columns([1, 8])
with c1:
    try: st.image("logo.png", width=100)
    except: st.write("LOGO")
with c2:
    st.markdown("""
    <div>
        <h1 style="font-size: 2.2rem; margin: 0; line-height: 1.1;">Stop The Bleeding.</h1>
        <p style="font-size: 1rem; color: #64748b; margin: 0;">Most exterior remodelers lose 15-20% of their margin to <b>Home Depot runs</b> and dumb mistakes.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- DASHBOARD ---
col_inputs, col_results = st.columns([1, 1.4], gap="large")

with col_inputs:
    st.selectbox("📂 Pick a Scenario:", options=list(personas.keys()), key="persona_selector", on_change=update_sliders)
    st.write("") 

    st.markdown("##### 1. Your Numbers")
    
    st.caption(f"**A. Job Volume:** {st.session_state.jobs}/mo")
    st.slider("Jobs", 1, 50, key="jobs", label_visibility="collapsed")

    st.caption(f"**B. Avg Invoice:** ${st.session_state.rev:,.0f}") 
    st.slider("Revenue", 5000, 50000, key="rev", step=500, label_visibility="collapsed")

    st.caption(f"**C. Target Margin:** {st.session_state.margin}%")
    st.slider("Margin", 5, 50, key="margin", step=1, label_visibility="collapsed")
    
    st.write("") 

    st.markdown("##### 2. The Chaos Factor")
    
    st.markdown(f"**D. 'Oh Sh*t' Moments Per Job:** {st.session_state.chaos}")
    roast = get_chaos_commentary(st.session_state.chaos)
    st.caption(f"*{roast}*")
    st.select_slider("Incidents", options=[0, 1, 2, 3, 4, 5], key="chaos", label_visibility="collapsed")

    st.write("") 

    st.caption(f"**E. Cost Per Screw Up:** ${st.session_state.cost}")
    breakdown = "IDLE CREW ($105) + FUEL ($45) + OFFICE ($30) + OPPORTUNITY ($70) = $250"
    st.slider("Cost", 50, 1000, key="cost", step=50, label_visibility="collapsed", help=breakdown)

with col_results:
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
        
        # 1. THE TOTEM POLE (Center Aligned Metric + Burn Rate)
        st.markdown(f"""
        <div class="big-metric-container">
            <div class="metric-label">ANNUAL PROFIT LOST</div>
            <div class="metric-value">${annual_bleed:,.0f}</div>
            <div class="metric-sub">🔥 {percent_burned:.1f}% of Profit Burned</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. THE TWIN CARDS (Pain vs Reality)
        pain = get_pain_analogy(annual_bleed)
        st.markdown(f"""
        <div class="card-row">
            <div class="score-card card-red">
                <div class="card-lbl">The Reality</div>
                <div class="card-val">{pain}</div>
            </div>
            <div class="score-card card-orange">
                <div class="card-lbl">Realized Margin</div>
                <div class="card-val">{realized_margin:.1f}%</div>
                <div class="card-sub">vs {st.session_state.margin}% Goal</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3. CHART
        chart_data = pd.DataFrame({'Category': ['Keep', 'Burn'], 'Amount': [max(0, actual_profit), annual_bleed]})
        color_scale = alt.Scale(domain=['Keep', 'Burn'], range=['#198754', '#dc2626'])
        
        c = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Category', title=None, axis=alt.Axis(labelAngle=0)), 
            y=alt.Y('Amount', title=None, axis=alt.Axis(format='$,.0f', grid=False)), 
            color=alt.Color('Category', scale=color_scale, legend=None),
            tooltip=['Category', 'Amount']
        ).properties(height=280) 
        
        st.altair_chart(c, use_container_width=True)

        # 4. FORM (Clean Integration)
        st.markdown("##### 🛑 Stop The Bleeding. Get the Fix.")
        with st.form("lead_capture_form"):
            c1, c2, c3 = st.columns([1, 1, 1.5])
            with c1: st.text_input("First Name", label_visibility="collapsed", placeholder="First Name")
            with c2: st.text_input("Last Name", label_visibility="collapsed", placeholder="Last Name")
            with c3: st.text_input("Email", label_visibility="collapsed", placeholder="Email Address")
            
            st.form_submit_button("SEND ME THE REPORT >>", use_container_width=True)

    else:
        st.success("You claimed 0 incidents. Move the slider to see reality!")
