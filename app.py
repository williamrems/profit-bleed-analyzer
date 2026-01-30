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

# --- CSS SURGERY (THE TIGHTENING) ---
st.markdown("""
    <style>
    /* 1. AGGRESSIVE PADDING REDUCTION */
    .main .block-container {
        padding-top: 1rem !important; /* Was 4rem+ */
        padding-bottom: 1rem !important;
        max-width: 95% !important;
    }
    
    /* 2. COMPACT HEADERS */
    h1 { font-size: 1.5rem !important; margin-bottom: 0 !important; }
    h3 { font-size: 1.2rem !important; margin-top: 0 !important; margin-bottom: 0.5rem !important; }
    p { margin-bottom: 0.5rem !important; font-size: 0.95rem; }
    
    /* 3. TIGHTEN WIDGET SPACING */
    div[data-testid="stVerticalBlock"] {
        gap: 0.5rem !important; /* Shrinks gap between elements */
    }
    
    /* 4. MAKE METRICS STAND OUT BUT NOT TAKE UP HALF THE PAGE */
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        color: #dc2626 !important;
        font-weight: 900;
        padding-bottom: 0 !important;
    }
    
    /* 5. BUTTON STYLING */
    div.stButton > button {
        background-color: #0d6efd;
        color: white;
        width: 100%;
        border-radius: 6px;
        padding: 0.5rem;
        border: none;
    }
    div.stButton > button:hover { background-color: #0b5ed7; color: white; border: none; }
    
    /* 6. CENTER IMAGES */
    div[data-testid="stImage"] { display: flex; justify-content: center; }
    </style>
""", unsafe_allow_html=True)

# --- DYNAMIC PAIN LOGIC ---
def get_pain_analogy(loss_amount):
    if loss_amount < 5000: return "That's a nice family vacation to Mexico."
    elif loss_amount < 12000: return "That's a brand new Honda ATV or two jet skis."
    elif loss_amount < 25000: return "You could have bought a brand new Harley."
    elif loss_amount < 50000: return "You threw away a brand new Ford F-150."
    elif loss_amount < 80000: return "That's a full-time PM's salary burned."
    else: return "You could have bought a vacation cabin."

# --- COMPACT HEADER ---
# Using columns to put Logo side-by-side with Title to save vertical space
h1, h2 = st.columns([1, 4])
with h1:
    try:
        st.image("logo.png", width=120) # Smaller logo
    except:
        st.write("LOGO")
with h2:
    st.markdown("<h1 style='padding-top: 10px;'>Is Your Process Bleeding Profit?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569;'>Most exterior remodelers lose 15-20% of their margin to inefficiency. Find out your number.</p>", unsafe_allow_html=True)

st.divider()

# --- THE DASHBOARD ---
col_inputs, col_results = st.columns([1, 1], gap="medium")

# ========================
# LEFT COLUMN: INPUTS
# ========================
with col_inputs:
    st.markdown("### 1. Your Numbers")
    
    # Using markdown for labels allows tighter spacing than st.write
    st.markdown("**A. Job Volume**")
    avg_jobs = st.slider("Jobs/Month", 1, 50, 8, label_visibility="collapsed")
    st.caption(f"Doing **{avg_jobs}** jobs per month.")

    st.markdown("**B. Average Job Price**") 
    avg_revenue = st.slider("Revenue", 5000, 50000, 15000, 500, format="$%d", label_visibility="collapsed")
    st.caption(f"Avg Ticket: **${avg_revenue:,.0f}**")

    st.markdown("**C. Target Profit Margin (%)**")
    profit_margin = st.slider("Margin", 5, 50, 20, 1, format="%d%%", label_visibility="collapsed")
    st.caption(f"Healthy Margin: **{profit_margin}%**")

    st.markdown("---") # Tighter divider
    
    st.markdown("### 2. The Chaos Factor")
    st.markdown("**D. 'Oh Sh*t' Moments Per Job**")
    chaos_factor = st.select_slider(
        "Incidents",
        options=[0, 1, 2, 3, 4, 5],
        value=2,
        label_visibility="collapsed"
    )
    st.caption(f"Values: 0 (Perfect) to 5 (Total Chaos). You picked: **{chaos_factor}**")

    st.markdown("**E. Cost Per Incident**")
    # Compact tooltip
    breakdown = "IDLE CREW ($105) + FUEL ($45) + OFFICE ($30) + OPPORTUNITY ($70) = $250"
    cost_per_incident = st.slider("Cost", 50, 1000, 250, 50, format="$%d", label_visibility="collapsed", help=breakdown)
    st.caption(f"Using **${cost_per_incident}** per incident.")

# ==========================
# RIGHT COLUMN: RESULTS
# ==========================
with col_results:
    # Math
    monthly_bleed = (avg_jobs * chaos_factor * cost_per_incident)
    annual_bleed = monthly_bleed * 12
    monthly_revenue = avg_jobs * avg_revenue
    annual_revenue = monthly_revenue * 12
    potential_profit = annual_revenue * (profit_margin / 100)
    actual_profit = potential_profit - annual_bleed

    if chaos_factor > 0:
        st.markdown("### 3. The Damage Report")
        
        # Metric
        st.metric(label="ANNUAL PROFIT LOST", value=f"${annual_bleed:,.0f}")
        
        # Alert Box
        pain = get_pain_analogy(annual_bleed)
        if annual_bleed > 20000: st.error(f"⚠️ {pain}")
        else: st.warning(f"⚠️ {pain}")

        # Chart - Height reduced to 280 to fit screen better
        chart_data = pd.DataFrame({
            'Category': ['Money You Keep', 'Money You Burn'],
            'Amount': [max(0, actual_profit), annual_bleed],
            'Color': ['#198754', '#dc2626'] 
        })
        
        c = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Category', title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Amount', title='Dollars', axis=alt.Axis(format='$,.0f')),
            color=alt.Color('Category', scale=alt.Scale(domain=['Money You Keep', 'Money You Burn'], range=['#198754', '#dc2626']), legend=None),
            tooltip=['Category', 'Amount']
        ).properties(height=280) # Reduced height
        
        st.altair_chart(c, use_container_width=True)
    else:
        st.success("You claimed 0 incidents. Move the slider to see reality!")


# --- LEAD CAPTURE ---
st.markdown("---")

# Compact Lead Form
c_left, c_mid, c_right = st.columns([1, 3, 1]) # Slightly wider mid column for better form fit

with c_mid:
    st.markdown("#### Stop The Bleeding.")
    st.caption("Get the full **'Profit Leak Analysis'** sent to your inbox.")

    with st.form("lead_capture_form"):
        f1, f2 = st.columns(2)
        with f1: first_name = st.text_input("First Name")
        with f2: last_name = st.text_input("Last Name")
            
        company = st.text_input("Company Name")
        email = st.text_input("Email Address")
        # Removed extra fields to make it shorter/cleaner
        
        submitted = st.form_submit_button("SEND ME THE FIX >>")

        if submitted:
            if not email or not first_name:
                st.error("Missing Info.")
            else:
                st.success(f"Report sent to {email}!")
