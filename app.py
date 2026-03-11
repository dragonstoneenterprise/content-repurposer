import streamlit as st
import requests
import os

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

st.title("Content Repurposer")
transcript = st.text_area("Paste your transcript", height=200)

if st.button("Transform") and transcript:
    with st.spinner("Repurposing..."):
        prompt = f"""Transform this transcript into 3 formats:

1. BLOG POST (3-4 paragraphs, engaging intro, clear body, strong closing)
2. TWITTER THREAD (5 tweets, numbered 1/5 to 5/5, each standalone)
3. YOUTUBE SHORTS SCRIPT (30 seconds, hook first, punchy, call to action)

Transcript:
{transcript}

Output in this format:
---BLOG---
[content]
---THREAD---
1/ [tweet]
2/ [tweet]
3/ [tweet]
4/ [tweet]
5/ [tweet]
---SHORTS---
[30 sec script]
---END---"""

        try:
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
                json={"model": "minimax/minimax-m2.1", "messages": [{"role": "user", "content": prompt}], "max_tokens": 2000},
                timeout=60
            )
            result = resp.json()["choices"][0]["message"]["content"]
            
            sections = result.split("---")
            blog = sections[2].strip() if len(sections) > 2 else ""
            thread = sections[4].strip() if len(sections) > 4 else ""
            shorts = sections[6].strip() if len(sections) > 6 else ""
            
            st.subheader("📝 Blog Post")
            st.write(blog)
            st.subheader("🐦 Twitter Thread")
            st.code(thread)
            st.subheader("🎬 YouTube Shorts")
            st.code(shorts)
            
        except Exception as e:
            st.error(f"Error: {e}")
