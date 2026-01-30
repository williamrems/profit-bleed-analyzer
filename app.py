import streamlit as st
import pandas as pd
import altair as alt
import base64
import requests # <--- NEW: Needed to actually send data to Salesforce

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ContractorFlow | Profit Bleed",
    page_icon="favicon.png",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- HELPER: BASE64 IMAGE LOADER ---
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

logo_b64 = get_image_base64("logo.png")

# --- CSS: PERFECT BALANCE & CLEAN FORM ---
st.markdown("""
    <style>
    /* 1. RESET STREAMLIT PADDING */
    .main .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 2rem !important; 
        max-width: 95% !important;
    }
    
    /* 2. WIDGET SPACING */
    div[data-testid="stVerticalBlock"] { gap: 0.6rem !important; }
    div.stSlider { padding-top: 0px !important; padding-bottom: 10px !important; }
    
    /* 3. BIG METRIC */
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
    
    /* 4. TWIN SCORECARDS */
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
    .card-red { border-bottom: 4px solid #dc2626; }
    .card-red .card-val { font-size: 1.1rem; font-weight: 700; color: #dc2626; line-height: 1.3; }
    .card-red .card-lbl { font-size: 0.7rem; text-transform: uppercase; color: #94a3b8; font-weight: 700; margin-bottom: 5px; }

    .card-orange { border-bottom: 4px solid #f59e0b; }
    .card-orange .card-val { font-size: 1.8rem; font-weight: 800; color: #d97706; }
    .card-orange .card-lbl { font-size: 0.7rem; text-transform: uppercase; color: #94a3b8; font-weight: 700; margin-bottom: 5px; }
    .card-orange .card-sub { font-size: 0.75rem; color: #64748b; }
    
    /* 5. FORM STYLING */
    div[data-testid="stForm"] {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-top: 20px;
    }
    
    /* Make the CTA Button aggressive */
    div.stButton > button {
        background-color: #dc2626; /* Urgent Red */
        color: white;
        font-weight: 800;
        border: none;
        padding: 0.8rem 1rem;
        text-transform: uppercase;
        width: 100%;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #b91c1c;
        border: none;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
    }

    /* 6. FOOTER STYLING */
    .footer-container {
        margin-top: 60px;
        padding-top: 30px;
        border-top: 1px solid #e2e8f0;
        text-align: center;
    }
    .footer-tagline {
        font-size: 1.4rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 10px;
    }
    .footer-desc {
        font-size: 0.95rem;
        color: #64748b;
        max-width: 600px;
        margin: 0 auto 15px auto;
        line-height: 1.5;
    }
    .footer-link a {
        color: #0d6efd;
        font-weight: 600;
        text-decoration: none;
    }
    .footer-link a:hover { text-decoration: underline; }

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

# --- PRICE CHECK ---
def get_pain_analogy(loss_amount):
    if loss_amount < 5000: return "Basically your beer money for the year."
    elif loss_amount < 12000: return "You burned a decent used side-by-side."
    elif loss_amount < 20000: return "That's a nice used Harley you don't have."
    elif loss_amount < 35000: return "You threw away a used work truck."
    elif loss_amount < 55000: return "You torched a brand new F-150 XL."
    elif loss_amount < 85000: return "That's a fully loaded F-250 Platinum gone."
    elif loss_amount < 120000: return "That's a down payment on a lake house."
    else: return "You are literally working for free."

# --- ROASTS ---
def get_chaos_commentary(level):
    if level == 0: return "You're lying. No one is this perfect."
    if level == 1: return "1 Home Depot run per job. Manageable."
    if level == 2: return "Forgot materials twice? That's expensive."
    if level == 3: return "You're at Menards more than the roof."
    if level == 4: return "Your crew is getting paid to sit in the truck."
    if level == 5: return "Total Dumpster Fire. You are working for free."
    return ""

# --- HEADER (CLICKABLE LOGO) ---
st.markdown(f"""
    <div style="display: grid; grid-template-columns: auto 1fr; gap: 20px; align-items: center; border-bottom: 1px solid #e2e8f0; padding-bottom: 15px; margin-bottom: 20px;">
        <a href="https://www.contractorflowapp.com" target="_blank">
            <img src="data:image/png;base64,{logo_b64}" width="110">
        </a>
        <div>
            <h1 style="font-size: 2.2rem; margin: 0; line-height: 1.1; color: #1e293b;">Stop The Bleeding.</h1>
            <p style="font-size: 1rem; color: #64748b; margin: 0;">Most exterior remodelers lose 15-20% of their margin to <b>Home Depot runs</b> and dumb mistakes.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

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
        
        # 1. THE TOTEM POLE
        st.markdown(f"""
        <div class="big-metric-container">
            <div class="metric-label">ANNUAL PROFIT LOST</div>
            <div class="metric-value">${annual_bleed:,.0f}</div>
            <div class="metric-sub">🔥 {percent_burned:.1f}% of Profit Burned</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. THE TWIN CARDS
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

        # 4. FORM (REAL SALESFORCE WEB-TO-LEAD)
        st.markdown("##### 🛑 Stop The Bleeding. Fix Your Numbers.")
        
        with st.form("lead_capture_form"):
            c1, c2 = st.columns(2)
            with c1: 
                first_name = st.text_input("First Name")
                email = st.text_input("Email")
            with c2: 
                last_name = st.text_input("Last Name")
                company = st.text_input("Company Name")
            
            mobile = st.text_input("Mobile Phone (Optional)")

            # The CTA Button
            submitted = st.form_submit_button("STOP THE BLEEDING - BOOK A DEMO >>")

            if submitted:
                if not email or not last_name:
                    st.error("Please provide at least a Name and Email.")
                else:
                    # --- SALESFORCE SUBMISSION LOGIC ---
                    
                    # 1. Prepare the URL
                    sf_url = "https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8"
                    
                    # 2. Prepare the Description String (Calculator Results)
                    # We inject the calculator results into the 'description' field so the sales rep sees it.
                    calc_summary = f"""
                    --- PROFIT BLEED CALCULATOR RESULTS ---
                    Persona: {st.session_state.persona_selector}
                    Annual Profit Lost: ${annual_bleed:,.0f}
                    Profit Burned: {percent_burned:.1f}%
                    Realized Margin: {realized_margin:.1f}% (vs {st.session_state.margin}% Target)
                    Chaos Factor: {st.session_state.chaos}/5
                    Cost Per Incident: ${st.session_state.cost}
                    Analogy: {pain}
                    """
                    
                    # 3. Prepare the Payload
                    payload = {
                        "oid": "00D5Y000002VYeK",
                        "retURL": "http://", # Dummy URL, we handle success message here
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "company": company,
                        "mobile": mobile,
                        "lead_source": "Website", # Or "SFDC-DM|ContractorFlow" if preferred
                        "description": calc_summary
                    }
                    
                    # 4. Send the POST request
                    try:
                        r = requests.post(sf_url, data=payload)
                        if r.status_code == 200:
                            st.success("Request Sent! A ContractorFlow expert will reach out shortly.")
                            st.balloons()
                        else:
                            st.error("There was an error sending your request. Please try again.")
                    except Exception as e:
                        st.error(f"Connection Error: {e}")

    else:
        st.success("You claimed 0 incidents. Move the slider to see reality!")

# --- FOOTER ---
st.markdown("""
    <div class="footer-container">
        <div class="footer-tagline">Built by Contractors, For Contractors. 🔨</div>
        <div class="footer-desc">
            All-In-One CRM Software Built for Contractors.<br>
            Manage leads, sales, scheduling, employees, and projects in one powerful platform.<br>
            Built on Salesforce and designed by contractors to help you scale with confidence.
        </div>
        <div class="footer-link">
            <a href="https://www.contractorflowapp.com" target="_blank">www.contractorflowapp.com</a>
        </div>
    </div>
""", unsafe_allow_html=True)
