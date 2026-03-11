import streamlit as st
import requests
import os
import json
from datetime import datetime, timedelta

# Configuration
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
GUMROAD_PRO_LINK = "https://gumroad.com/l/YOUR_PRO_LINK"
GUMROAD_AGENCY_LINK = "https://gumroad.com/l/YOUR_AGENCY_LINK"

# Page config
st.set_page_config(
    Repurposer",
 page_title="Content    page_icon="⚡",
    layout="wide"
)

# Custom CSS for professional look
st.markdown("""
<style>
    /* Main gradient header */
    .header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
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
    
    /* Feature cards */
    .feature-card {
        background: #0f0f23;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #2a2a4a;
        margin-bottom: 1rem;
    }
    
    /* Input area styling */
    .stTextArea textarea {
        background: #0f0f23;
        border: 1px solid #2a2a4a;
        border-radius: 8px;
        color: #ffffff;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
    }
    
    /* Output sections */
    .output-section {
        background: #0f0f23;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    /* Usage meter */
    .usage-meter {
        background: #1a1a2e;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    /* Pricing cards */
    .pricing-card {
        background: #0f0f23;
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid #2a2a4a;
        text-align: center;
    }
    .pricing-card.featured {
        border-color: #667eea;
    }
    .price {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for usage tracking
if 'usage_count' not in st.session_state:
    st.session_state.usage_count = 0
if 'usage_date' not in st.session_state:
    st.session_state.usage_date = datetime.now().date()
if 'is_pro' not in st.session_state:
    st.session_state.is_pro = False

# Reset usage if new month
if st.session_state.usage_date.month != datetime.now().month:
    st.session_state.usage_count = 0
    st.session_state.usage_date = datetime.now().date()

# Header
st.markdown("""
<div class="header">
    <h1>⚡ Content Repurposer</h1>
    <p>Transform any transcript into a blog post, Twitter thread, and YouTube Shorts — in under 2 minutes.</p>
</div>
""", unsafe_allow_html=True)

# Usage meter
col1, col2, col3 = st.columns(3)
with col1:
    if st.session_state.is_pro:
        st.success("Pro Member - Unlimited")
    else:
        st.info(f"Free: {3 - st.session_state.usage_count}/3 remaining this month")
        if st.session_state.usage_count >= 3:
            st.warning("Monthly limit reached!")

# Feature columns
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>📝 Blog Post</h3>
        <p>SEO-optimized article ready to publish</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🐦 Twitter Thread</h3>
        <p>5 engaging tweets threaded together</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>📹 YouTube Shorts</h3>
        <p>30-second script with hook and CTA</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Input section
transcript = st.text_area(
    "Paste your transcript here:",
    height=200,
    placeholder="Paste your podcast or video transcript..."
)

# Transform button
if st.button("⚡ Transform Content", type="primary"):
    if not transcript:
        st.error("Please paste a transcript first")
    elif not st.session_state.is_pro and st.session_state.usage_count >= 3:
        st.error("Monthly limit reached. Upgrade to Pro for unlimited.")
        st.markdown(f"[Upgrade to Pro →]({GUMROAD_PRO_LINK})")
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
                        "model": "openai/gpt-3.5-turbo",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 2500
                    },
                    timeout=90
                )
                result = resp.json()["choices"][0]["message"]["content"]
                
                # Parse sections
                sections = result.split("---")
                blog = sections[1].strip() if len(sections) > 1 else ""
                thread = sections[2].strip() if len(sections) > 2 else ""
                shorts = sections[3].strip() if len(sections) > 3 else ""
                
                # Increment usage
                st.session_state.usage_count += 1
                
                # Display results
                st.markdown("---")
                st.markdown("## 📝 Blog Post")
                st.markdown(f"<div class='output-section'>{blog}</div>", unsafe_allow_html=True)
                
                st.markdown("## 🐦 Twitter Thread")
                thread_lines = thread.split('\n')
                for line in thread_lines:
                    if line.strip():
                        st.code(line.strip())
                
                st.markdown("## 📹 YouTube Shorts Script")
                st.code(shorts)
                
                st.success(f"Transformation complete! ({st.session_state.usage_count}/3 free used)")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Upgrade section
st.markdown("---")
st.markdown("### 🚀 Upgrade to Pro")

pc1, pc2, pc3 = st.columns(3)
with pc1:
    st.markdown(f"""
    <div class="pricing-card">
        <h3>Free</h3>
        <p class="price">$0</p>
        <p>3 transformations/month</p>
        <p>Basic features</p>
    </div>
    """, unsafe_allow_html=True)

with pc2:
    st.markdown(f"""
    <div class="pricing-card featured">
        <h3>⭐ Pro</h3>
        <p class="price">$19/mo</p>
        <p>Unlimited transformations</p>
        <p>Priority processing</p>
    </div>
    """, unsafe_allow_html=True)
    st.button("Get Pro", key="pro_btn")

with pc3:
    st.markdown(f"""
    <div class="pricing-card">
        <h3>🏢 Agency</h3>
        <p class="price">$49/mo</p>
        <p>API access</p>
        <p>Bulk processing</p>
    </div>
    """, unsafe_allow_html=True)
    st.button("Get Agency", key="agency_btn")

# Footer
st.markdown("---")
st.markdown("*Built by Dragonstone Enterprises*")
st.markdown("---")
st.subheader("🚀 Need unlimited transformations?")
st.markdown("[Get Pro — $19/month →](https://9245368029329.gumroad.com/l/tnlfjv)")
