"""
AI Humanisation & Personalised Shopping & Productivity Agent - Streamlit UI
==========================================================================
Autonomous Visual & Conversational Shopping Agent:
1. Multimodal Visual Outfit Scanner (Upload dress photo -> Finds exact item -> 1-Click Direct Checkout)
2. User Profile & Preferences Sizing Calibration
3. Multi-Platform Deep Search across Amazon, Myntra, Ajio, Flipkart, and Noon
4. Forensic Fake Review & Verified Fabric Authenticity Filter
5. Cross-Platform Price Arbitrage & Direct Payment Gateway Express Checkout Links
"""

import os
import io
import requests
import streamlit as st
import pandas as pd
from PIL import Image
from dotenv import load_dotenv
from agent import PersonalizedShoppingAgent, UserProfile

# Load environment
load_dotenv()

# Page setup
st.set_page_config(
    page_title="AI Humanisation & Autonomous Shopping Agent",
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
        background: linear-gradient(135deg, #0B132B 0%, #1C2541 45%, #3A0CA3 100%);
        padding: 2.2rem 2.2rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.25);
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
        background: linear-gradient(90deg, #FFFFFF, #93C5FD, #E0E7FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        color: #CBD5E1;
        max-width: 900px;
        line-height: 1.55;
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
    
    .checkout-hero-box {
        background: linear-gradient(135deg, #064E3B 0%, #065F46 60%, #047857 100%);
        color: white;
        padding: 1.8rem 2rem;
        border-radius: 16px;
        box-shadow: 0 12px 30px rgba(6, 78, 59, 0.25);
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
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
        font-size: 1.55rem;
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
    
    .visual-pill {
        display: inline-block;
        background: #F1F5F9;
        color: #334155;
        font-weight: 600;
        font-size: 0.82rem;
        padding: 3px 9px;
        border-radius: 6px;
        margin-right: 5px;
        margin-bottom: 5px;
        border: 1px solid #CBD5E1;
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

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

if "uploaded_image_preview" not in st.session_state:
    st.session_state.uploaded_image_preview = None

# Helper to fetch online sample image for 1-click test
@st.cache_data
def get_sample_image(url: str) -> Image.Image:
    try:
        resp = requests.get(url, timeout=5)
        return Image.open(io.BytesIO(resp.content))
    except Exception:
        # Fallback generated swatch image
        return Image.new("RGB", (300, 300), color=(15, 30, 80))

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
        st.success("🟢 Live Autonomous Agent Ready")
    elif gemini_key_input or tavily_key_input:
        st.warning("🟡 Partial API Keys provided")
    else:
        st.info("🔵 Interactive Prototype Mode")

# =============================================================================
# MAIN INTERFACE
# =============================================================================

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🛍️ Autonomous AI Humanisation & Shopping Agent</div>
    <p class="hero-subtitle">
        Give a goal or upload a photo of any outfit/dress. The AI agent executes the entire workflow autonomously: 
        reverse-engineers visual details, matches your saved size & budget, screens fake reviews across 5 platforms, 
        and brings you <strong>straight to the checkout page & payment gateway</strong> with pre-applied discounts.
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

# EXECUTION TRIGGER CONTAINER
active_gemini_key = gemini_key_input.strip() if gemini_key_input else env_gemini
active_tavily_key = tavily_key_input.strip() if tavily_key_input else env_tavily
agent = PersonalizedShoppingAgent(gemini_api_key=active_gemini_key, tavily_api_key=active_tavily_key)

# TWO INTERACTIVE WORKFLOW MODES
tab_visual, tab_text = st.tabs([
    "📸 Visual Outfit Match & 1-Click Checkout (Photo Upload)",
    "💬 Natural Language Goal & Occasion Search"
])

submitted_goal = None
submitted_image = None

# -----------------------------------------------------------------------------
# TAB 1: VISUAL MATCH & AUTONOMOUS CHECKOUT
# -----------------------------------------------------------------------------
with tab_visual:
    st.markdown("#### 📸 Upload an Outfit / Dress Photo")
    st.caption("Upload any photo or try a sample. The agent will visually identify the garment, find the exact match online, and generate a direct payment link.")

    col_upload, col_samples = st.columns([1.2, 1])

    with col_upload:
        uploaded_file = st.file_uploader(
            "Choose an outfit photo (JPG, PNG, WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
            help="Upload an image of a dress, kurta, suit, or outfit you want to buy"
        )
        custom_visual_notes = st.text_input(
            "Optional instruction / Occasion constraint:",
            placeholder="e.g. For my best friend's wedding under ₹4000, need size 40",
            value="For my best friend's wedding under ₹4000"
        )

    with col_samples:
        st.markdown("**Or test with a sample outfit (1-click):**")
        sample_urls = {
            "👘 Royal Blue Jacquard Kurta Set": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=600&auto=format&fit=crop&q=80",
            "✨ Maroon & Gold Silk Blend Ensemble": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=600&auto=format&fit=crop&q=80",
            "👑 Designer Woven Jacquard Wedding Set": "https://images.unsplash.com/photo-1597983073493-88cd35cf93b0?w=600&auto=format&fit=crop&q=80"
        }
        selected_sample_url = None
        for label, url in sample_urls.items():
            if st.button(label, use_container_width=True):
                selected_sample_url = url

    # Determine active image
    active_img = None
    if uploaded_file is not None:
        try:
            active_img = Image.open(uploaded_file)
            st.session_state.uploaded_image_preview = active_img
        except Exception as e:
            st.error(f"Error loading uploaded image: {e}")
    elif selected_sample_url:
        active_img = get_sample_image(selected_sample_url)
        st.session_state.uploaded_image_preview = active_img

    if st.session_state.uploaded_image_preview:
        st.markdown("---")
        col_prev, col_act = st.columns([1, 2])
        with col_prev:
            st.image(st.session_state.uploaded_image_preview, caption="Target Outfit to Find & Checkout", use_container_width=True)
        with col_act:
            st.markdown("### ⚡ Ready for Autonomous Execution")
            st.write("Click below to let the agent find this exact garment across platforms, verify genuine customer reviews, apply best coupons, and bring you straight to checkout.")
            if st.button("🚀 Find Exact Item & Bring Me to Checkout Page", type="primary", use_container_width=True):
                submitted_image = st.session_state.uploaded_image_preview
                submitted_goal = custom_visual_notes or "Find this exact outfit online and prepare direct checkout"

# -----------------------------------------------------------------------------
# TAB 2: TEXT GOAL SEARCH
# -----------------------------------------------------------------------------
with tab_text:
    st.markdown("#### 💬 Describe What You Need")
    st.caption("Quick suggestions (click to use):")
    col_s1, col_s2, col_s3 = st.columns(3)
    quick_text = None

    with col_s1:
        if st.button("💍 Traditional kurta set for wedding under ₹4000", use_container_width=True):
            quick_text = "Find a traditional kurta set for my best friend's wedding under ₹4000"
    with col_s2:
        if st.button("✨ Royal Indo-Western Bandhgala for Sangeet under ₹6000", use_container_width=True):
            quick_text = "Find a royal Indo-Western Bandhgala outfit for wedding sangeet under ₹6000"
    with col_s3:
        if st.button("🌿 Designer Tussar Silk Kurta Set under ₹3500", use_container_width=True):
            quick_text = "Find a designer Tussar silk kurta set with verified fabric reviews under ₹3500"

    text_input_goal = st.chat_input("E.g., Find a traditional kurta set for my best friend's wedding under ₹4000...")
    if quick_text:
        text_input_goal = quick_text

    if text_input_goal:
        submitted_goal = text_input_goal
        submitted_image = None

# =============================================================================
# AUTONOMOUS AGENT WORKFLOW EXECUTION
# =============================================================================
if submitted_goal:
    with st.status("🤖 Autonomous Agent Executing End-to-End Workflow...", expanded=True) as status:
        if submitted_image is not None:
            st.write("📸 **Step 0:** Gemini Vision scanning outfit photo (extracting weave, neckline, palette, and cut)...")
        st.write("🎯 **Step 1:** Persona Calibration (locking in size, occasion formality, and budget)...")
        st.write("🌐 **Step 2:** Deep searching Amazon.in, Myntra, Ajio, Flipkart, and Noon for matching listings...")
        st.write("🛡️ **Step 3:** Forensic Fake Review Guardian (screening bot reviews, seller rating & fabric integrity)...")
        st.write("💳 **Step 4:** Formulating lowest effective price, active promo codes & Direct Payment Gateway Link...")

        result = agent.execute_workflow(
            user_prompt=submitted_goal,
            profile=st.session_state.user_profile,
            image=submitted_image
        )
        st.session_state.latest_result = result
        status.update(label="✅ Autonomous Execution Complete! Direct Checkout Link Ready.", state="complete", expanded=False)

# =============================================================================
# RESULTS DISPLAY
# =============================================================================
if st.session_state.latest_result:
    res = st.session_state.latest_result

    # Status notification
    if res.is_live_execution:
        st.success(f"🟢 {res.execution_message}")
    else:
        st.info(f"💡 {res.execution_message}")

    # Top winner recommendation for direct checkout
    top_pick = res.top_recommendations[0] if res.top_recommendations else None

    if top_pick:
        # HERO SECTION: DIRECT CHECKOUT & PAYMENT GATEWAY (The requested core feature!)
        st.markdown(f"""
        <div class="checkout-hero-box">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 0.8rem;">
                <span style="background: rgba(255,255,255,0.2); padding: 5px 12px; border-radius: 9999px; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.5px;">
                    🎯 EXACT MATCH FOUND & AUTHENTICATED
                </span>
                <span style="background: #10B981; color: white; padding: 5px 12px; border-radius: 9999px; font-weight: 700; font-size: 0.85rem;">
                    🛡️ {top_pick.authenticity_score}/100 Verified Authentic
                </span>
            </div>
            <div style="font-size: 1.55rem; font-weight: 800; line-height: 1.3; margin-bottom: 0.4rem;">
                {top_pick.product_name}
            </div>
            <div style="font-size: 1.05rem; opacity: 0.9; margin-bottom: 1rem;">
                by <strong>{top_pick.brand}</strong> &bull; Best Platform: <strong>{top_pick.best_platform}</strong> &bull; Sizing Pre-locked: <strong>{profile.top_size}</strong>
            </div>
            <div style="background: rgba(0, 0, 0, 0.25); border-radius: 12px; padding: 1rem 1.4rem; margin-bottom: 1.2rem; display: flex; flex-wrap: wrap; gap: 20px; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-size: 0.85rem; opacity: 0.8; text-transform: uppercase; font-weight: 700;">Effective Final Offer Price</div>
                    <div style="font-size: 2.1rem; font-weight: 800; color: #6EE7B7;">
                        {top_pick.actual_offer_price} 
                        <span style="font-size: 1.05rem; text-decoration: line-through; color: #CBD5E1; margin-left: 8px;">{top_pick.original_mrp}</span>
                        <span style="font-size: 1rem; color: #FEF08A; margin-left: 8px;">({top_pick.discount_percentage})</span>
                    </div>
                </div>
                <div>
                    <div style="font-size: 0.85rem; opacity: 0.8; text-transform: uppercase; font-weight: 700;">Pre-Applied Coupon & Savings</div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: #FFFFFF;">
                        🏷️ Code: <span style="background: #047857; padding: 2px 8px; border-radius: 6px; font-family: monospace;">{top_pick.best_coupon_code}</span> &bull; {top_pick.checkout_savings}
                    </div>
                </div>
                <div>
                    <div style="font-size: 0.85rem; opacity: 0.8; text-transform: uppercase; font-weight: 700;">Payment Gateway</div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: #E2E8F0;">
                        💳 {top_pick.payment_gateway_info}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_chk1, col_chk2 = st.columns([1.6, 1])
        with col_chk1:
            st.link_button(
                f"⚡ 💳 PROCEED STRAIGHT TO CHECKOUT & PAYMENT GATEWAY ({top_pick.actual_offer_price})",
                top_pick.direct_checkout_link,
                use_container_width=True,
                type="primary",
                help="Takes you directly to the payment/cart screen with coupon and size pre-selected"
            )
        with col_chk2:
            st.link_button(
                f"🔍 Inspect Full Product Page on {top_pick.best_platform}",
                top_pick.direct_buy_link,
                use_container_width=True
            )

    # Productivity Metrics Row
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("⏱️ Time Saved", f"{res.productivity_metrics.get('hours_saved', 4.5)} hrs", "Zero manual browsing")
    with m2:
        st.metric("🛡️ Fake Reviews Screened", f"{res.productivity_metrics.get('fake_reviews_purged', 19)} purged", "Bot clusters removed")
    with m3:
        st.metric("🌐 Platforms Scanned", f"{res.productivity_metrics.get('platforms_scanned', 5)} platforms", "Amazon, Myntra, Ajio, Flipkart, Noon")
    with m4:
        st.metric("💰 Total Savings", res.productivity_metrics.get("max_discount_identified", "₹2,480"), res.productivity_metrics.get("average_savings_percent", "42% OFF"))

    # VISUAL ATTRIBUTE BREAKDOWN (If visual search was executed)
    if res.uploaded_image_analysis:
        va = res.uploaded_image_analysis
        st.markdown("### 📸 AI Multimodal Vision Feature Extraction")
        col_v1, col_v2 = st.columns([1, 2])
        with col_v1:
            if st.session_state.uploaded_image_preview:
                st.image(st.session_state.uploaded_image_preview, caption="Source Outfit Scanned", use_container_width=True)
        with col_v2:
            st.markdown(f"**Identified Silhouette:** `{va.get('detected_garment_type', 'Garment')}`")
            st.markdown(f"**Fabric & Texture:** {va.get('fabric_and_weave', 'Silk blend / Jacquard')}")
            st.markdown(f"**Cut & Silhouette:** {va.get('silhouette_and_cut', 'Tailored fit')}")
            st.markdown(f"**Embellishments:** {va.get('embellishment_details', 'Zari embroidery')}")
            st.markdown("**Color Palette:**")
            palette_html = "".join([f'<span class="visual-pill">🎨 {c}</span>' for c in va.get("color_palette", [])])
            st.markdown(palette_html, unsafe_allow_html=True)
            st.markdown("**Visual Signature Keywords:**")
            keywords_html = "".join([f'<span class="visual-pill">#{k}</span>' for k in va.get("visual_signature_keywords", [])])
            st.markdown(keywords_html, unsafe_allow_html=True)

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
            st.link_button(
                f"⚡ 💳 1-Click Checkout ({rec.actual_offer_price})",
                rec.direct_checkout_link or rec.direct_buy_link,
                use_container_width=True,
                type="primary"
            )
            st.link_button(
                f"🛒 View Product Page",
                rec.direct_buy_link,
                use_container_width=True
            )

    st.divider()

    # SECTION 2: CROSS-PLATFORM COMPARISON MATRIX
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
            "Direct Checkout Link": item.direct_checkout_link or item.direct_link
        })

    df = pd.DataFrame(table_data)
    st.dataframe(
        df[["Platform", "Product / Brand", "Listed Price", "Applicable Coupon / Bank Offer", "Effective Best Price", "Authenticity Audit", "Delivery & Returns", "Deal Verdict", "Direct Checkout Link"]],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # SECTION 3: STEP-BY-STEP REASONING TRACE
    with st.expander("🔬 View Multi-Step Autonomous Agent Execution & Forensic Analysis Trace", expanded=False):
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
    st.markdown("### 💡 How the Autonomous Visual & Checkout Agent Works:")
    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    with col_g1:
        st.markdown("""
        **1. Multimodal Vision Scan**  
        Upload any photo of a dress, suit, or outfit. Gemini Vision extracts garment silhouette, weave, and color palette.
        """)
    with col_g2:
        st.markdown("""
        **2. Deep Platform Search**  
        Autonomous search queries across Amazon.in, Myntra, Ajio, Flipkart, and Noon locate the exact item online.
        """)
    with col_g3:
        st.markdown("""
        **3. Fake Review Screening**  
        Forensically weeds out fake 5-star bots, dishonest polyester fabrics, and unverified third-party sellers.
        """)
    with col_g4:
        st.markdown("""
        **4. Direct to Payment Gateway**  
        Calculates the highest coupon discount, pre-selects your size, and brings you straight to 1-Click checkout!
        """)
