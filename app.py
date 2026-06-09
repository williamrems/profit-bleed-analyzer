# ==========================================
# 1. BULLETPROOF DUAL-MODE LOGIC & UTMS
# ==========================================
# This try/except block guarantees URL parsing works 
# regardless of what Streamlit version your server is running.
try:
    # Modern Streamlit (v1.30.0+)
    raw_mode = st.query_params.get("mode", "")
    u_source = st.query_params.get("utm_source", "direct")
    u_medium = st.query_params.get("utm_medium", "organic")
    u_campaign = st.query_params.get("utm_campaign", "profit-bleed-analyzer")
except AttributeError:
    # Legacy Streamlit (< v1.30.0)
    params = st.experimental_get_query_params()
    raw_mode = params.get("mode", [""])[0] if "mode" in params else ""
    u_source = params.get("utm_source", ["direct"])[0] if "utm_source" in params else "direct"
    u_medium = params.get("utm_medium", ["organic"])[0] if "utm_medium" in params else "organic"
    u_campaign = params.get("utm_campaign", ["profit-bleed-analyzer"])[0] if "utm_campaign" in params else "profit-bleed-analyzer"

# Sanitize inputs (handle lists if Streamlit acts weird, force lowercase)
if isinstance(raw_mode, list): 
    raw_mode = raw_mode[0] if raw_mode else ""

# The UI Rule: Form is ALWAYS ON, unless explicitly disabled by a rep.
is_rep_mode = str(raw_mode).strip().lower() == "rep"
show_lead_form = not is_rep_mode

# Sanitize UTMs
u_source = str(u_source).lower()
u_medium = str(u_medium).lower()
u_campaign = str(u_campaign).lower()
