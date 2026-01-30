import streamlit as st
import pandas as pd
import altair as alt

# --- PAGE CONFIGURATION ---
# We use layout="wide" to utilize the full desktop screen space
st.set_page_config(
    page_title="ContractorFlow | Profit Calculator",
    page_icon="favicon.png",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #0f172a; font-weight: 800; }
    /* Make metrics huge */
    div[data-testid="stMetricValue"] { font-size: 3rem !important; color: #dc2626 !important; font-weight: 900; }
    /* Button Styling */
    div.stButton > button { background-color: #0d6efd; color: white; width: 100%; border-radius: 8px; padding: 0.75rem; border: none; }
    div.stButton > button:hover { background-color: #0b5ed7; color: white; border: none; }
    /* Center the Logo if possible */
    div[data-testid="stImage"] { margin-left: auto; margin-right: auto; display: block; }
    </style>
""", unsafe_allow_html=True)

# --- DYNAMIC PAIN LOGIC ---
def get_pain_analogy(loss_amount):
    if loss_amount < 5000: return "That's a really nice family vacation to Mexico."
    elif loss_amount < 12000: return "That's a brand new Honda ATV or two nice jet skis."
    elif loss_amount < 25000: return "You could have bought a brand new Harley Davidson."
    elif loss_amount < 50000: return "You literally threw away a brand new Ford F-150 work truck."
    elif loss_amount < 80000: return "That's a full-time Project Manager's salary you just burned."
    else: return "You could have bought a freaking vacation home / cabin."

# --- HEADER (Centered) ---
# We use columns to center the logo/header on the wide page
h_c1, h_c2, h_c3 = st.columns([1, 2, 1])
with h_c2:
    try:
        st.image("logo.png", width=250)
    except:
        st.title("ContractorFlow")
    st.markdown("<h3 style='text-align: center; color: #475569;'>Is Your Process Bleeding Profit?</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Most exterior remodelers lose 15-20% of their margin to inefficiency. Find out your number.</p>", unsafe_allow_html=True)

st.divider()

# --- THE DASHBOARD LAYOUT ---
# This creates the Side-by-Side view. On mobile, col_results drops below col_inputs automatically.
col_inputs, col_results = st.columns(2, gap="large")

# ========================
# LEFT COLUMN: THE INPUTS
# ========================
with col_inputs:
    st.subheader("1. Your Numbers")
    
    st.write("**A. Job Volume**")
    avg_jobs = st.slider("Jobs Completed Per Month", 1, 50, 8)

    st.write("**B. Average Invoice Amount (Total Job Price)**") 
    avg_revenue = st.slider("Avg Revenue", 5000, 50000, 15000, 500, format="$%d", label_visibility="collapsed")
    st.caption(f"Selected: **${avg_revenue:,.0f}** per job")

    st.write("**C. Target Net Profit Margin (%)**")
    profit_margin = st.slider("Profit Margin", 5, 50, 20, 1, format="%d%%", label_visibility="collapsed")
    st.caption(f"Calculating based on a **{profit_margin}%** healthy margin.")

    st.divider()
    
    st.subheader("2. The Chaos Factor")
    st.write("How often do crews wait on materials, return to the supply house, or fix paperwork errors per job?")
    
    chaos_factor = st.select_slider(
        "Incidents Per Job",
        options=[0, 1, 2, 3, 4, 5],
        value=2,
        help="0 = Perfect Robot Efficiency. 5 = Total Chaos."
    )

    st.write("**D. Cost Per 'Oh Sh*t' Moment**")
    st.caption("Includes: Crew labor (idle time), fuel, vehicle wear, and office time to fix it.")
    
    # Tooltip breakdown
    cost_breakdown = """
    HOW WE CALCULATE $250:
    ----------------------
    1. IDLE CREW (3 Guys x $35/hr x 1 hr lost) = $105
    2. FUEL & VEHICLE WEAR (Round trip) = $45
    3. OFFICE ADMIN (Rescheduling/Fixing) = $30
    4. OPPORTUNITY COST (Profit you didn't make) = $70
    ----------------------
    TOTAL = $250 per incident
    """
    
    cost_per_incident = st.slider(
        "Cost Per Incident", 50, 1000, 250, 50, format="$%d", 
        label_visibility="collapsed", help=cost_breakdown
    )
    st.info(f"Using **${cost_per_incident}** per incident. (Industry Avg is $250)")

# ==========================
# RIGHT COLUMN: THE RESULTS
# ==========================
with col_results:
    # Calculations
    monthly_bleed = (avg_jobs * chaos_factor * cost_per_incident)
    annual_bleed = monthly_bleed * 12
    monthly_revenue = avg_jobs * avg_revenue
    annual_revenue = monthly_revenue * 12
    potential_profit = annual_revenue * (profit_margin / 100)
    actual_profit = potential_profit - annual_bleed

    if chaos_factor > 0:
        st.subheader("3. The Damage Report")
        
        # The Metric
        st.metric(label="ANNUAL PROFIT LOST TO INEFFICIENCY", value=f"${annual_bleed:,.0f}")
        
        # The Pain Analogy
        pain_message = get_pain_analogy(annual_bleed)
        if annual_bleed > 20000:
            st.error(f"⚠️ {pain_message}")
        else:
            st.warning(f"⚠️ {pain_message}")

        # The Chart
        chart_data = pd.DataFrame({
            'Category': ['Money You Keep', 'Money You Burn'],
            'Amount': [actual_profit if actual_profit > 0 else 0, annual_bleed],
            'Color': ['#198754', '#dc2626'] 
        })
        
        # We increase the chart height for desktop impact
        c = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Category', sort=None, title=None, axis=alt.Axis(labels=True, labelAngle=0)),
            y=alt.Y('Amount', title='Annual Dollars'),
            color=alt.Color('Category', scale=alt.Scale(domain=['Money You Keep', 'Money You Burn'], range=['#198754', '#dc2626']), legend=None),
            tooltip=['Category', 'Amount']
        ).properties(height=400) # Taller chart for desktop
        
        st.altair_chart(c, use_container_width=True)
    else:
        st.success("You claimed 0 incidents. Either you are a robot, or you're lying to yourself! Try moving the slider to see reality.")


# --- LEAD CAPTURE (CENTERED) ---
st.divider()

# We use columns to center the form so it doesn't stretch across the whole wide screen
c_left, c_mid, c_right = st.columns([1, 2, 1])

with c_mid:
    st.subheader("Stop The Bleeding.")
    st.markdown("Get the full **'Profit Leak Analysis'** and our **Process Fix Checklist** sent to your inbox.")

    with st.form("lead_capture_form"):
        f1, f2 = st.columns(2)
        with f1: first_name = st.text_input("First Name")
        with f2: last_name = st.text_input("Last Name")
            
        company = st.text_input("Company Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Mobile Phone (Optional - for text alerts)")
        trade = st.selectbox("Primary Trade", ["Roofing", "Siding", "Windows/Doors", "General Contracting", "Other"])
        revenue = st.selectbox("Annual Revenue Range", ["Under $500k", "$500k - $1M", "$1M - $3M", "$3M - $5M", "$5M+"])

        submitted = st.form_submit_button("SEND ME THE FIX >>")

        if submitted:
            if not email or not first_name:
                st.error("Please fill in your Name and Email to get the report.")
            else:
                # PAYLOAD
                payload = {
                    "oid": "YOUR_SALESFORCE_ORG_ID_HERE",
                    "first_name": first_name,
                    "last_name": last_name,
                    "company": company,
                    "email": email,
                    "phone": phone,
                    "00N_DUMMY_TRADE_ID": trade,
                    "00N_DUMMY_REVENUE_ID": revenue,
                    "00N_DUMMY_ANNUAL_BLEED": annual_bleed,
                    "00N_DUMMY_CHAOS_FACTOR": chaos_factor,
                    "00N_DUMMY_COST_PER_INCIDENT": cost_per_incident,
                    "00N_DUMMY_TARGET_MARGIN": profit_margin,
                    "lead_source": "Profit Calculator App"
                }
                st.success(f"Report sent to {email}!")
                st.balloons()