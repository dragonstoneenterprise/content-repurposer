import streamlit as st
import requests
import os
import json
from datetime import datetime, timedelta

# Configuration
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
GUMROAD_PRO_LINK = "https://9245368029329.gumroad.com/l/tnlfjv"
GUMROAD_AGENCY_LINK = "https://dragonstone.gumroad.com/l/content-repurposer-agency"

# Page config
st.set_page_config(
    page_title="Content Repurposer",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .header h1 {
        color: #ffffff;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .header p {
        color: #a0a0a0;
        font-size: 1.1rem;
    }
    .feature-card {
        background: #0f0f23;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #2a2a4a;
        margin-bottom: 1rem;
        text-align: center;
    }
    .stTextArea textarea {
        background: #0f0f23;
        border: 1px solid #2a2a4a;
        border-radius: 8px;
        color: #ffffff;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        width: 100%;
    }
    .output-section {
        background: #0f0f23;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .pricing-card {
        background: #0f0f23;
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid #2a2a4a;
        text-align: center;
    }
    .pricing-card.featured {
        border-color: #667eea;
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
    }
    .price {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
    }
    .usage-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Session state for usage tracking
if 'usage_count' not in st.session_state:
    st.session_state.usage_count = 0
if 'usage_date' not in st.session_state:
    st.session_state.usage_date = datetime.now().date()
if 'is_pro' not in st.session_state:
    st.session_state.is_pro = False

# Reset monthly
if st.session_state.usage_date.month != datetime.now().month:
    st.session_state.usage_count = 0
    st.session_state.usage_date = datetime.now().date()

# Header
st.markdown("""
<div class="header">
    <h1>⚡ Content Repurposer</h1>
    <p>Turn 1 hour of transcript into a week of content — in 2 minutes</p>
</div>
""", unsafe_allow_html=True)

# Usage banner
if st.session_state.is_pro:
    st.markdown('<div class="usage-banner">⭐ Pro Member - Unlimited Access</div>', unsafe_allow_html=True)
else:
    remaining = 3 - st.session_state.usage_count
    if remaining > 0:
        st.info(f"Free: {remaining}/3 transformations remaining this month")
    else:
        st.warning("Monthly limit reached!")

# Features
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="feature-card"><h3>📝 Blog Post</h3><p>SEO-optimized article</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="feature-card"><h3>🐦 Twitter Thread</h3><p>5 engaging tweets</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="feature-card"><h3>📹 YouTube Shorts</h3><p>30-sec script with hook</p></div>', unsafe_allow_html=True)

st.markdown("---")

# Input
transcript = st.text_area(
    "Paste your transcript:",
    height=200,
    placeholder="Paste your podcast, video, or interview transcript here..."
)

# Transform button
if st.button("⚡ Transform Content", type="primary"):
    if not transcript:
        st.error("Please paste a transcript first")
    elif not st.session_state.is_pro and st.session_state.usage_count >= 3:
        st.error("Monthly limit reached. Upgrade below.")
        st.markdown(f"[→ Upgrade to Pro]({GUMROAD_PRO_LINK})")
    else:
        with st.spinner("Repurposing your content..."):
            prompt = f"""Transform this transcript into 3 formats:

1. BLOG POST (3-4 paragraphs, engaging intro, clear body, strong closing)
2. TWITTER THREAD (5 tweets, numbered 1/5 to 5/5, each standalone, engaging)
3. YOUTUBE SHORTS SCRIPT (30 seconds, hook first, punchy, call to action at end)

Transcript:
{transcript}

Output in this EXACT format:
---BLOG---
[your blog post here]
---THREAD---
1/ [tweet 1]
2/ [tweet 2]
3/ [tweet 3]
4/ [tweet 4]
5/ [tweet 5]
---SHORTS---
[your 30-second script]
---END---"""

            try:
                resp = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "moonshotai/kimi-k2.5",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 2500
                    },
                    timeout=90
                )
                result = resp.json()["choices"][0]["message"]["content"]
                
                sections = result.split("---")
                blog = sections[1].strip() if len(sections) > 1 else ""
                thread = sections[2].strip() if len(sections) > 2 else ""
                shorts = sections[3].strip() if len(sections) > 3 else ""
                
                st.session_state.usage_count += 1
                
                st.markdown("---")
                st.markdown("## 📝 Blog Post")
                st.markdown(f"<div class='output-section'>{blog}</div>", unsafe_allow_html=True)
                
                st.markdown("## 🐦 Twitter Thread")
                for line in thread.split('\n'):
                    if line.strip():
                        st.code(line.strip())
                
                st.markdown("## 📹 YouTube Shorts Script")
                st.code(shorts)
                
                remaining = 3 - st.session_state.usage_count
                st.success(f"Done! {remaining}/3 free used")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Pricing
st.markdown("---")
st.markdown("### 🚀 Upgrade for Unlimited")

p1, p2, p3 = st.columns(3)
with p1:
    st.markdown("""
    <div class="pricing-card">
        <h3>Free</h3>
        <p class="price">$0</p>
        <p>3 transformations/month</p>
        <p>Basic features</p>
    </div>
    """, unsafe_allow_html=True)
with p2:
    st.markdown("""
    <div class="pricing-card featured">
        <h3>⭐ Pro</h3>
        <p class="price">$19/mo</p>
        <p>Unlimited transformations</p>
        <p>Priority processing</p>
        <p><a href="{}">→ Get Pro</a></p>
    </div>
    """.format(GUMROAD_PRO_LINK), unsafe_allow_html=True)
with p3:
    st.markdown("""
    <div class="pricing-card">
        <h3>🏢 Agency</h3>
        <p class="price">$49/mo</p>
        <p>API access</p>
        <p>Bulk processing</p>
        <p><a href="{}">→ Get Agency</a></p>
    </div>
    """.format(GUMROAD_AGENCY_LINK), unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("*Built by Dragonstone Enterprises*")
