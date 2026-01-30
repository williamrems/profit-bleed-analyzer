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

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #0f172a; font-weight: 800; }
    div[data-testid="stMetricValue"] { font-size: 2.5rem !important; color: #dc2626 !important; font-weight: 900; }
    div.stButton > button { background-color: #0d6efd; color: white; width: 100%; border-radius: 8px; padding: 0.75rem; border: none; }
    div.stButton > button:hover { background-color: #0b5ed7; color: white; border: none; }
    </style>
""", unsafe_allow_html=True)

# --- DYNAMIC PAIN LOGIC ---
def get_pain_analogy(loss_amount):
    """Returns a relatable purchase based on the amount of money lost."""
    if loss_amount < 5000:
        return "That's a really nice family vacation to Mexico."
    elif loss_amount < 12000:
        return "That's a brand new Honda ATV or two nice jet skis."
    elif loss_amount < 25000:
        return "You could have bought a brand new Harley Davidson."
    elif loss_amount < 50000:
        return "You literally threw away a brand new Ford F-150 work truck."
    elif loss_amount < 80000:
        return "That's a full-time Project Manager's salary you just burned."
    else:
        return "You could have bought a freaking vacation home / cabin."

# --- HEADER ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("logo.png", width=200)
    except:
        st.header("ContractorFlow")

st.title("Is Your Process Bleeding Profit?")
st.caption("Most exterior remodelers lose 15-20% of their margin to inefficiency. Find out your number.")
st.divider()

# --- INPUT SECTION ---
st.subheader("1. Your Numbers")

avg_jobs = st.slider("Jobs Completed Per Month", min_value=1, max_value=50, value=8)

# DYNAMIC CURRENCY HEADER
# Streamlit sliders are tricky with commas, so we show the formatted number clearly above
# SWAP THIS
st.write(f"**Average Invoice Amount (Total Job Price):**") 
avg_revenue = st.slider(
    "Select Revenue", 
    min_value=5000, 
    max_value=50000, 
    value=15000, 
    step=500,
    format="$%d",
    label_visibility="collapsed"
)
# Display the big clean number with commas
st.info(f"Selected Average Job Size: **${avg_revenue:,.0f}**")


st.markdown("### 2. The Chaos Factor")
st.write("How often do crews wait on materials, return to the supply house, or fix paperwork errors per job?")

chaos_factor = st.select_slider(
    "Incidents Per Job",
    options=[0, 1, 2, 3, 4, 5],
    value=2,
    help="0 = Perfect Robot Efficiency. 5 = Total Chaos."
)

# --- THE MATH ---
cost_per_incident = 250 
monthly_bleed = (avg_jobs * chaos_factor * cost_per_incident)
annual_bleed = monthly_bleed * 12

monthly_revenue = avg_jobs * avg_revenue
annual_revenue = monthly_revenue * 12
potential_profit = annual_revenue * 0.20
actual_profit = potential_profit - annual_bleed

# --- THE REVEAL ---
st.divider()

if chaos_factor > 0:
    st.subheader("3. The Damage Report")
    
    st.metric(label="ANNUAL PROFIT LOST TO INEFFICIENCY", value=f"${annual_bleed:,.0f}")
    
    # --- DYNAMIC ANALOGY CALL ---
    pain_message = get_pain_analogy(annual_bleed)
    
    if annual_bleed > 20000:
        st.error(f"⚠️ {pain_message}")
    else:
        st.warning(f"⚠️ {pain_message}")

    # Chart
    chart_data = pd.DataFrame({
        'Category': ['Money You Keep', 'Money You Burn'],
        'Amount': [actual_profit if actual_profit > 0 else 0, annual_bleed],
        'Color': ['#198754', '#dc2626'] 
    })
    
    c = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Category', sort=None, title=None),
        y=alt.Y('Amount', title='Annual Dollars'),
        color=alt.Color('Category', scale=alt.Scale(domain=['Money You Keep', 'Money You Burn'], range=['#198754', '#dc2626']), legend=None),
        tooltip=['Category', 'Amount']
    ).properties(height=300)
    
    st.altair_chart(c, use_container_width=True)

else:
    st.success("You claimed 0 incidents. Either you are a robot, or you're lying to yourself! Try moving the slider to see reality.")


# --- LEAD CAPTURE ---
st.divider()
st.subheader("Stop The Bleeding.")
st.markdown("Get the full **'Profit Leak Analysis'** and our **Process Fix Checklist** sent to your inbox.")

with st.form("lead_capture_form"):
    c1, c2 = st.columns(2)
    with c1:
        first_name = st.text_input("First Name")
    with c2:
        last_name = st.text_input("Last Name")
        
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
            # PAYLOAD WITH DYNAMIC ANALOGY INCLUDED (Optional)
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
                "lead_source": "Profit Calculator App"
            }
            
            st.success(f"Report sent to {email}!")
            st.balloons()