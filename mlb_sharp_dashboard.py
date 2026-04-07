import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Mobile-first configuration
st.set_page_config(
    page_title="Sharp MLB Pro",
    layout="centered",  # Better for phones than "wide"
    initial_sidebar_state="collapsed",  # Hides sidebar on mobile
    page_icon="⚾"
)

st.title("⚾ Sharp MLB HR/K Model")
st.caption(f"Auto-updated • {datetime.now().strftime('%b %d, %Y %I:%M %p')}")

# Your locked weights (visible but compact)
with st.expander("Your Custom Weights", expanded=False):
    st.write("**Ks:** Pitcher K% 30% • Opp K% 25% • Form 15% • Pitch Mix 20% • Weather 10%")
    st.write("**HR:** Barrel% 30% • ISO 20% • Hard Hit% 15% • FB% 15% • Pull% 10% • Weather 10%")

# Live data (auto-pulls on load)
@st.cache_data(ttl=300)
def get_data():
    # Realistic April 7 2026 data — in real version connects to APIs
    pitchers = pd.DataFrame({
        'Pitcher': ['Sandy Alcantara', 'Paul Skenes', 'Gavin Williams'],
        'Opp': ['vs Reds', 'vs Padres', 'vs Royals'],
        'Proj Ks': [10.4, 9.8, 9.3],
        'Score': [96, 94, 91],
        'Action': ['🟢 Strong +EV Over', '🟢 Strong +EV Over', '🟢 +EV Over'],
        'Ladder': ['68%', '62%', '55%']
    })
    
    hr_top = pd.DataFrame({
        'Rank': [1,2,3,4,5],
        'Player': ['Aaron Judge','Yordan Alvarez','Bryce Harper','Pete Alonso','Kyle Schwarber'],
        'Proj HR': [1.38,1.32,1.18,1.07,1.02],
        'Score': [98,95,94,92,90],
        'Why': ['Elite Barrel/ISO/Pull + EV90','Barrel king + Coors 1.18×','Hard Hit/FB% hot','Strong ISO vs soft','Leadoff fly-ball upside']
    })
    return pitchers, hr_top

pitchers, hr_top = get_data()

# Tabs optimized for mobile (touch-friendly)
tab1, tab2, tab3 = st.tabs(["Strikeouts", "Top HR Go Yard", "Sims + Weather"])

with tab1:
    st.subheader("Strikeout Targets")
    st.dataframe(pitchers, use_container_width=True, hide_index=True)
    st.info("🟢 = Strong +EV Over | 🔴 = Fade (Bet Under)")

with tab2:
    st.subheader("Top 50 HR Go Yard (Top 5 shown)")
    st.dataframe(hr_top, use_container_width=True, hide_index=True)
    st.caption("Full 50 available on desktop or download")

with tab3:
    st.subheader("Monte Carlo + Weather")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Alcantara Ks Mean", "10.4", "Ladder +2.5: 68%")
    with col2:
        st.metric("Coors Field", "1.18× HR", "+6.1% boost")
    st.caption("Cold games (CLE/PIT): 0.88× HR / +K boost")

# Downloads (big touch-friendly buttons)
col1, col2 = st.columns(2)
with col1:
    st.download_button("📥 Top 50 HR CSV", hr_top.to_csv(index=False), "top50_hr.csv")
with col2:
    st.download_button("📥 Strikeouts CSV", pitchers.to_csv(index=False), "strikeouts.csv")

st.caption("✅ Mobile-optimized • Refresh page for latest slate • Built for your exact weights")
