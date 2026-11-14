"""
AI Humanisation & Personalised Shopping & Productivity Agent - Streamlit UI
==========================================================================
A clean, interactive web application featuring:
1. User Profile & Preferences Sidebar (saved once: sizes, brands, budget, styles)
2. Natural Language Goal Input (Chat interface with sample prompts)
3. Multi-Step Agent Execution Stepper (Requirement Analyzer -> Deep Search -> Fake Review Filter -> Price Comparison)
4. Comparison Summary Table + Top 3 Genuine Recommendation Cards
"""

import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from agent import PersonalizedShoppingAgent, UserProfile

# Load environment
load_dotenv()

# Page setup
st.set_page_config(
    page_title="AI Humanisation & Shopping Agent",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #312E81 100%);
        padding: 2.2rem 2.2rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
    }
    
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
        background: linear-gradient(90deg, #FFFFFF, #93C5FD, #C7D2FE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.02rem;
        color: #CBD5E1;
        max-width: 850px;
        line-height: 1.5;
        margin-bottom: 0;
    }
    
    .metric-badge {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 0.5rem;
    }
    
    .card-container {
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.4rem;
        background: #FFFFFF;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .card-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.08);
    }
    
    .auth-badge {
        background: #DCFCE7;
        color: #166534;
        font-weight: 700;
        font-size: 0.82rem;
        padding: 4px 10px;
        border-radius: 8px;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    
    .platform-badge {
        background: #EEF2FF;
        color: #3730A3;
        font-weight: 700;
        font-size: 0.82rem;
        padding: 4px 10px;
        border-radius: 8px;
    }
    
    .price-offer {
        font-size: 1.5rem;
        font-weight: 800;
        color: #0F172A;
    }
    
    .price-mrp {
        text-decoration: line-through;
        color: #94A3B8;
        font-size: 0.95rem;
        margin-left: 0.4rem;
    }
    
    .discount-tag {
        color: #16A34A;
        font-weight: 700;
        font-size: 0.9rem;
        margin-left: 0.4rem;
    }
    
    .step-box {
        padding: 1rem 1.2rem;
        border-radius: 10px;
        background: #F8FAFC;
        border-left: 4px solid #4F46E5;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "user_profile" not in st.session_state:
    st.session_state.user_profile = UserProfile(
        gender="Men",
        top_size="L (40)",
        bottom_size="32",
        preferred_brands=["Manyavar", "Fabindia", "Tasva", "House of Pataudi", "Raymond"],
        budget_min=1500,
        budget_max=4000,
        currency="₹",
        style_preference="Traditional Festive / Wedding",
        preferred_platforms=["Myntra", "Amazon.in", "Ajio", "Flipkart", "Noon"]
    )

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

# =============================================================================
# SIDEBAR: USER PROFILE & PREFERENCES
# =============================================================================
with st.sidebar:
    st.markdown("### 👤 User Persona & Sizing")
    st.caption("Personal preferences saved here automatically calibrate all AI searches and eliminate manual filtering.")

    gender = st.selectbox(
        "Gender / Wardrobe Category",
        options=["Men", "Women", "Unisex"],
        index=0 if st.session_state.user_profile.gender == "Men" else 1
    )

    col_size1, col_size2 = st.columns(2)
    with col_size1:
        top_size = st.selectbox(
            "Top/Shirt Size",
            options=["S (38)", "M (40)", "L (42)", "XL (44)", "XXL (46)", "Custom"],
            index=1
        )
    with col_size2:
        bottom_size = st.selectbox(
            "Bottom Size",
            options=["28", "30", "32", "34", "36", "38", "40"],
            index=2
        )

    style_pref = st.selectbox(
        "Style Preference",
        options=[
            "Traditional Festive / Wedding",
            "Royal Indo-Western & Bandhgala",
            "Contemporary Minimalist",
            "Classic Formal",
            "Modern Fusion / Casual Ethnic"
        ],
        index=0
    )

    available_brands = [
        "Manyavar", "Fabindia", "Tasva", "House of Pataudi",
        "Raymond", "Peter England", "WLS", "Biba", "Kalki Fashion", "Zara"
    ]
    selected_brands = st.multiselect(
        "Preferred Brands",
        options=available_brands,
        default=[b for b in st.session_state.user_profile.preferred_brands if b in available_brands]
    )

    st.markdown("#### 💰 Budget Range (₹)")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        budget_min = st.number_input("Min Price", min_value=500, max_value=20000, value=int(st.session_state.user_profile.budget_min), step=500)
    with col_b2:
        budget_max = st.number_input("Max Price", min_value=1000, max_value=50000, value=int(st.session_state.user_profile.budget_max), step=500)

    target_platforms = st.multiselect(
        "E-Commerce Platforms to Scan",
        options=["Amazon.in", "Myntra", "Ajio", "Flipkart", "Noon (Dubai/UAE)", "Tata CLiQ"],
        default=["Amazon.in", "Myntra", "Ajio", "Flipkart", "Noon (Dubai/UAE)"]
    )

    if st.button("💾 Save Profile Preferences", use_container_width=True, type="primary"):
        st.session_state.user_profile = UserProfile(
            gender=gender,
            top_size=top_size,
            bottom_size=bottom_size,
            preferred_brands=selected_brands if selected_brands else ["Manyavar", "House of Pataudi"],
            budget_min=float(budget_min),
            budget_max=float(budget_max),
            currency="₹",
            style_preference=style_pref,
            preferred_platforms=target_platforms
        )
        st.success("Preferences updated successfully!")

    st.divider()

    # API Keys Configuration
    st.markdown("### 🔑 API Keys Status")
    env_gemini = os.getenv("GEMINI_API_KEY", "").strip()
    env_tavily = os.getenv("TAVILY_API_KEY", "").strip()

    gemini_key_input = st.text_input(
        "Gemini API Key",
        value=env_gemini,
        type="password",
        placeholder="Enter AI Studio Key",
        help="Stored in .env or supplied here"
    )
    tavily_key_input = st.text_input(
        "Tavily Search API Key",
        value=env_tavily,
        type="password",
        placeholder="Enter Tavily Search Key",
        help="Get from tavily.com for deep e-commerce search"
    )

    if gemini_key_input and tavily_key_input:
        st.success("🟢 Live Agent Mode Ready")
    elif gemini_key_input or tavily_key_input:
        st.warning("🟡 Partial API Keys provided")
    else:
        st.info("🔵 Interactive Prototype Mode (Ready to test or configure)")

# =============================================================================
# MAIN INTERFACE
# =============================================================================

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🛍️ AI Humanisation & Personal Shopping Agent</div>
    <p class="hero-subtitle">
        Your high-productivity personal stylist & fraud-detection buyer. Finds the exact outfit for any occasion, 
        screens out fake bot reviews, checks verified buyer fabrics, and compares genuine offers across Amazon, Myntra, Ajio, Flipkart & Noon.
    </p>
</div>
""", unsafe_allow_html=True)

# Personal Persona Summary Banner
profile = st.session_state.user_profile
st.markdown(f"""
<div style="background: #F1F5F9; padding: 0.8rem 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; border: 1px solid #E2E8F0;">
    <span style="font-weight: 700; color: #1E293B;">Active Profile:</span>
    <span class="metric-badge" style="background: #E0E7FF; color: #3730A3;">Top: {profile.top_size}</span>
    <span class="metric-badge" style="background: #E0E7FF; color: #3730A3;">Bottom: {profile.bottom_size}</span>
    <span class="metric-badge" style="background: #FEF3C7; color: #92400E;">Budget: {profile.currency}{profile.budget_min:,.0f} - {profile.currency}{profile.budget_max:,.0f}</span>
    <span class="metric-badge" style="background: #DCFCE7; color: #166534;">Style: {profile.style_preference}</span>
    <span class="metric-badge" style="background: #F3E8FF; color: #6B21A8;">Brands: {', '.join(profile.preferred_brands[:3])}</span>
</div>
""", unsafe_allow_html=True)

# Goal Input Section
st.markdown("### 🎯 What do you need to find today?")

# Prompt Suggestions
st.caption("Quick suggestions (click to use):")
col_s1, col_s2, col_s3 = st.columns(3)
selected_prompt = None

with col_s1:
    if st.button("💍 Traditional kurta set for best friend's wedding under ₹4000", use_container_width=True):
        selected_prompt = "Find a traditional kurta set for my best friend's wedding under ₹4000"
with col_s2:
    if st.button("✨ Royal Indo-Western Bandhgala for Sangeet under ₹6000", use_container_width=True):
        selected_prompt = "Find a royal Indo-Western Bandhgala outfit for wedding sangeet under ₹6000"
with col_s3:
    if st.button("🌿 Designer Tussar Silk Kurta Set under ₹3500", use_container_width=True):
        selected_prompt = "Find a designer Tussar silk kurta set with verified fabric reviews under ₹3500"

user_query = st.chat_input("E.g., Find a traditional kurta set for my best friend's wedding under ₹4000...")
if selected_prompt:
    user_query = selected_prompt

# Execution Trigger
if user_query:
    active_gemini_key = gemini_key_input.strip() if gemini_key_input else env_gemini
    active_tavily_key = tavily_key_input.strip() if tavily_key_input else env_tavily

    agent = PersonalizedShoppingAgent(
        gemini_api_key=active_gemini_key,
        tavily_api_key=active_tavily_key
    )

    with st.status("🤖 AI Agent Executing Multi-Step Humanisation & Search Workflow...", expanded=True) as status:
        st.write("🔍 **Step 1:** Analyzing Occasion & Personal Size Mapping...")
        st.write("🌐 **Step 2:** Deep searching Amazon, Myntra, Ajio, Flipkart, and Noon...")
        st.write("🛡️ **Step 3:** Running Forensic Fake Review & Verified Fabric Authenticity Filter...")
        st.write("🏷️ **Step 4:** Calculating Cross-Platform Bank Offers, Instant Coupons & Effective Prices...")

        result = agent.execute_workflow(user_query, st.session_state.user_profile)
        st.session_state.latest_result = result
        status.update(label="✅ Agent Execution Complete! Top Verified Deals Found.", state="complete", expanded=False)

# Display Results
if st.session_state.latest_result:
    res = st.session_state.latest_result

    # Status notification
    if res.is_live_execution:
        st.success(f"🟢 {res.execution_message}")
    else:
        st.info(f"💡 {res.execution_message}")

    # Productivity Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("⏱️ Time Saved", f"{res.productivity_metrics.get('hours_saved', 3.8)} hrs", "Zero manual browsing")
    with m2:
        st.metric("🛡️ Fake Reviews Filtered", f"{res.productivity_metrics.get('fake_reviews_purged', 19)} listings", "Bot spam purged")
    with m3:
        st.metric("🌐 Platforms Vetted", f"{res.productivity_metrics.get('platforms_scanned', 5)} platforms", "Cross-compared")
    with m4:
        st.metric("💰 Max Savings Found", res.productivity_metrics.get("max_discount_identified", "₹2,200"), res.productivity_metrics.get("average_savings_percent", "38% OFF"))

    st.divider()

    # SECTION 1: TOP 3 GENUINE RECOMMENDATIONS
    st.markdown("## 🏆 Top 3 Genuine Verified Recommendations")
    st.caption("Screened for authentic fabric quality, seller reliability, user size availability, and genuine verified reviews.")

    rec_cols = st.columns(3)
    for idx, rec in enumerate(res.top_recommendations[:3]):
        with rec_cols[idx]:
            st.markdown(f"""
            <div class="card-container">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.8rem;">
                        <span class="platform-badge">🛒 {rec.best_platform}</span>
                        <span class="auth-badge">🛡️ {rec.authenticity_score}/100 Authentic</span>
                    </div>
                    <img src="{rec.image_url}" style="width: 100%; height: 210px; object-fit: cover; border-radius: 10px; margin-bottom: 0.9rem;" alt="{rec.product_name}" />
                    <div style="font-size: 0.82rem; font-weight: 700; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.5px;">{rec.brand}</div>
                    <h4 style="margin: 0.3rem 0 0.6rem 0; font-size: 1.05rem; line-height: 1.35; color: #0F172A;">{rec.product_name}</h4>
                    <div style="margin-bottom: 0.7rem;">
                        <span class="price-offer">{rec.actual_offer_price}</span>
                        <span class="price-mrp">{rec.original_mrp}</span>
                        <span class="discount-tag">({rec.discount_percentage})</span>
                    </div>
                    <div style="background: #F8FAFC; border-radius: 8px; padding: 0.65rem; margin-bottom: 0.8rem; font-size: 0.85rem; color: #334155;">
                        <strong>📏 Sizing & Stock:</strong> {rec.size_match_note}
                    </div>
                    <div style="font-size: 0.84rem; color: #475569; line-height: 1.45; margin-bottom: 0.9rem;">
                        <strong>🔎 Authenticity & Review Audit:</strong><br/>
                        {rec.quality_review_note}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.link_button(f"🛒 Buy on {rec.best_platform} for {rec.actual_offer_price}", rec.direct_buy_link, use_container_width=True, type="primary")

    st.divider()

    # SECTION 2: CROSS-PLATFORM PRICE & GENUINE OFFER COMPARISON TABLE
    st.markdown("## 📊 Cross-Platform Price & Genuine Offer Comparison")
    st.caption("Side-by-side comparison across Amazon, Myntra, Ajio, Flipkart, and Noon including bank offers and effective final price.")

    table_data = []
    for item in res.comparison_table:
        table_data.append({
            "Platform": item.platform,
            "Product / Brand": f"{item.brand} - {item.product_name}",
            "Listed Price": item.listed_price,
            "Applicable Coupon / Bank Offer": item.coupon_or_bank_offer,
            "Effective Best Price": item.effective_price,
            "Authenticity Audit": item.authenticity_score,
            "Delivery & Returns": item.delivery_and_returns,
            "Deal Verdict": item.verdict,
            "Direct Link": item.direct_link
        })

    df = pd.DataFrame(table_data)
    st.dataframe(
        df[["Platform", "Product / Brand", "Listed Price", "Applicable Coupon / Bank Offer", "Effective Best Price", "Authenticity Audit", "Delivery & Returns", "Deal Verdict"]],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # SECTION 3: STEP-BY-STEP AGENT REASONING TRACE
    with st.expander("🔬 View Multi-Step Agent Execution & Forensic Analysis Trace", expanded=False):
        for log in res.step_logs:
            st.markdown(f"#### Step {log.get('step')}: {log.get('title')}")
            st.markdown(f"**Status:** `{log.get('status')}`")
            if "data" in log:
                st.json(log["data"])
            elif "warning" in log:
                st.warning(log["warning"])
            st.markdown("---")

else:
    # Initial State / Guide
    st.markdown("---")
    st.markdown("### 💡 How the Agent Saves You Time & Guarantees Quality:")
    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    with col_g1:
        st.markdown("""
        **1. Persona Calibration**  
        Reads your saved size (e.g. L/40), preferred brands, and budget. No need to re-enter filters on 5 different websites.
        """)
    with col_g2:
        st.markdown("""
        **2. Deep Platform Search**  
        Queries Amazon.in, Myntra, Ajio, Flipkart, and Noon simultaneously using targeted search syntax.
        """)
    with col_g3:
        st.markdown("""
        **3. Fake Review Screening**  
        Forensically detects bot reviews, 5-star rating clusters, unverified sellers, and misleading fabric descriptions.
        """)
    with col_g4:
        st.markdown("""
        **4. True Effective Price**  
        Calculates active promo codes, ICICI/HDFC bank card discounts, and highlights the single best deal with direct links.
        """)
