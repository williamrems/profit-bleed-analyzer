import streamlit as st
import pandas as pd
import altair as alt

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ContractorFlow | Profit Calculator",
    page_icon="favicon.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS FOR MOBILE OPTIMIZATION ---
st.markdown("""
    <style>
    /* Make the mobile experience cleaner */
    .stApp {
        background-color: #f8f9fa;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        font-family: 'Helvetica', sans-serif;
        color: #0f172a;
        font-size: 1.8rem !important;
        font-weight: 800;
    }
    /* Style the big metrics */
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        color: #dc2626 !important; /* Profit Bleed Red */
        font-weight: 900;
    }
    /* Style the submit button */
    div.stButton > button {
        background-color: #0d6efd;
        color: white;
        width: 100%;
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #0b5ed7;
        color: white;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER & LOGO ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("logo.png", width=200)
    except:
        st.header("ContractorFlow") # Fallback if image missing

st.title("Is Your Process Bleeding Profit?")
st.caption("Most exterior remodelers lose 15-20% of their margin to inefficiency. Find out your number.")

st.divider()

# --- INPUT SECTION (THE CALCULATOR) ---
st.subheader("1. Your Numbers")

# Sliders for easy mobile input
avg_jobs = st.slider("Jobs Completed Per Month", min_value=1, max_value=50, value=8)
avg_revenue = st.slider("Average Revenue Per Job ($)", min_value=5000, max_value=50000, value=15000, step=500)

st.markdown("### 2. The Chaos Factor")
st.info("Be honest. How often do crews wait on materials, return to the supply house, or fix paperwork errors per job?")

chaos_factor = st.select_slider(
    "Incidents Per Job",
    options=[0, 1, 2, 3, 4, 5],
    value=2,
    help="0 = Perfect Robot Efficiency. 5 = Total Chaos."
)

# --- THE MATH (THE LOGIC) ---
# Industry assumptions
cost_per_incident = 250  # Labor, fuel, opportunity cost
monthly_bleed = (avg_jobs * chaos_factor * cost_per_incident)
annual_bleed = monthly_bleed * 12

# Revenue context
monthly_revenue = avg_jobs * avg_revenue
annual_revenue = monthly_revenue * 12
# Assuming a healthy 20% net margin for context (before bleed)
potential_profit = annual_revenue * 0.20
actual_profit = potential_profit - annual_bleed

# --- THE REVEAL (THE VISUALS) ---
st.divider()

if chaos_factor > 0:
    st.subheader("3. The Damage Report")
    
    # big red metric
    st.metric(label="ANNUAL PROFIT LOST TO INEFFICIENCY", value=f"${annual_bleed:,.0f}")
    
    # Contextual note
    if annual_bleed > 20000:
        st.error(f"⚠️ You are throwing away a brand new truck every year.")
    else:
        st.warning(f"⚠️ That's ${monthly_bleed:,.0f} missing from your pocket every single month.")

    # Visual Chart (Stacked Bar)
    # We create a simple dataframe for the chart
    chart_data = pd.DataFrame({
        'Category': ['Money You Keep', 'Money You Burn'],
        'Amount': [actual_profit if actual_profit > 0 else 0, annual_bleed],
        'Color': ['#198754', '#dc2626'] # Green vs Red
    })
    
    # Altair chart for custom colors
    c = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Category', sort=None, title=None),
        y=alt.Y('Amount', title='Annual Dollars'),
        color=alt.Color('Category', scale=alt.Scale(domain=['Money You Keep', 'Money You Burn'], range=['#198754', '#dc2626']), legend=None),
        tooltip=['Category', 'Amount']
    ).properties(height=300)
    
    st.altair_chart(c, use_container_width=True)

else:
    st.success("You claimed 0 incidents. Either you are a robot, or you're lying to yourself! Try moving the slider to see reality.")


# --- LEAD CAPTURE (WEB-TO-LEAD SIMULATION) ---
st.divider()
st.subheader("Stop The Bleeding.")
st.markdown("Get the full **'Profit Leak Analysis'** and our **Process Fix Checklist** sent to your inbox.")

with st.form("lead_capture_form"):
    # Two column layout for names
    c1, c2 = st.columns(2)
    with c1:
        first_name = st.text_input("First Name")
    with c2:
        last_name = st.text_input("Last Name")
        
    company = st.text_input("Company Name")
    email = st.text_input("Email Address")
    
    # Optional Phone
    phone = st.text_input("Mobile Phone (Optional - for text alerts)")

    # Qualification Dropdowns
    trade = st.selectbox("Primary Trade", ["Roofing", "Siding", "Windows/Doors", "General Contracting", "Other"])
    revenue = st.selectbox("Annual Revenue Range", ["Under $500k", "$500k - $1M", "$1M - $3M", "$3M - $5M", "$5M+"])

    # Hidden Field Simulation (The Calculator Results passed to Salesforce)
    # We don't show these, but we would send them
    
    submitted = st.form_submit_button("SEND ME THE FIX >>")

    if submitted:
        if not email or not first_name:
            st.error("Please fill in your Name and Email to get the report.")
        else:
            # --- SALESFORCE WEB-TO-LEAD MOCKUP ---
            # This is where the magic happens. 
            # In a real deployment, you would POST this payload to: https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8
            
            payload = {
                # Standard Salesforce Fields (These names are standard)
                "oid": "YOUR_SALESFORCE_ORG_ID_HERE",  # IMPORTANT: Swap this later
                "first_name": first_name,
                "last_name": last_name,
                "company": company,
                "email": email,
                "phone": phone,
                
                # Custom Fields (You need to create these in Salesforce Object Manager -> Leads)
                # Format is usually: 00Nxxxxxxxxxxxx
                "00N_DUMMY_TRADE_ID": trade,
                "00N_DUMMY_REVENUE_ID": revenue,
                "00N_DUMMY_ANNUAL_BLEED": annual_bleed, # Pass the calculator result!
                "00N_DUMMY_CHAOS_FACTOR": chaos_factor,
                
                # Campaign tracking
                "lead_source": "Profit Calculator App"
            }
            
            # Placeholder success message
            st.success(f"Report sent to {email}!")
            st.balloons()
            
            # In production, uncomment the requests line below:
            # import requests
            # response = requests.post("https://webto.salesforce.com/servlet/servlet.WebToLead?encoding=UTF-8", data=payload)