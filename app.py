import streamlit as st
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="RideBook",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-style UI
st.markdown("""
<style>
    /* Reset and base styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* Hide Streamlit components */
    #MainMenu, header, footer {
        display: none !important;
    }

    .stApp {
        background: #f8f9fa !important;
    }

    /* Mobile container */
    .mobile-container {
        max-width: 414px;
        margin: 0 auto;
        padding: 24px;
        background: white;
        min-height: 100vh;
        position: relative;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Header section */
    .header {
        margin-bottom: 32px;
    }

    .greeting {
        font-size: 28px;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 4px;
    }

    .subtitle {
        color: #666;
        font-size: 15px;
    }

    /* Search section */
    .search-box {
        background: #f8f9fa;
        border-radius: 28px;
        padding: 16px 24px;
        display: flex;
        align-items: center;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }

    .search-box:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .search-input {
        border: none;
        background: none;
        font-size: 16px;
        width: 100%;
        padding-right: 16px;
    }

    .search-icon {
        color: #1a1a1a;
        font-size: 20px;
    }

    /* Location cards */
    .locations-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        margin-bottom: 32px;
    }

    .location-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 16px;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .location-card:hover {
        transform: translateY(-2px);
        background: #f0f0f0;
    }

    .location-icon {
        font-size: 24px;
        margin-bottom: 12px;
    }

    .location-name {
        font-weight: 600;
        margin-bottom: 4px;
        color: #1a1a1a;
    }

    .location-address {
        font-size: 13px;
        color: #666;
        line-height: 1.4;
    }

    /* Bottom navigation */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 414px;
        background: white;
        padding: 16px 24px;
        display: flex;
        justify-content: space-between;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.05);
        border-top-left-radius: 24px;
        border-top-right-radius: 24px;
    }

    .nav-button {
        padding: 12px 32px;
        border-radius: 24px;
        font-weight: 500;
        font-size: 15px;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .nav-button.active {
        background: #1a1a1a;
        color: white;
    }

    .nav-button:not(.active) {
        color: #666;
    }

    .nav-button:not(.active):hover {
        background: #f0f0f0;
    }

    /* Recent rides section */
    .section-title {
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 16px;
    }

    .recent-rides {
        margin-bottom: 80px;  /* Space for bottom nav */
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'rides'

# Get greeting based on time of day
def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"

# Main app layout
st.markdown(f"""
<div class="mobile-container">
    <!-- Header section -->
    <div class="header">
        <div class="greeting">{get_greeting()}, Joost</div>
        <div class="subtitle">Where are you going today?</div>
    </div>

    <!-- Search box -->
    <div class="search-box">
        <input type="text" class="search-input" placeholder="Where to?">
        <span class="search-icon">📍</span>
    </div>

    <!-- Saved locations -->
    <div class="locations-grid">
        <!-- Work location -->
        <div class="location-card">
            <div class="location-icon">🏢</div>
            <div class="location-name">Work</div>
            <div class="location-address">1455 Market Street</div>
        </div>

        <!-- Home location -->
        <div class="location-card">
            <div class="location-icon">🏠</div>
            <div class="location-name">Home</div>
            <div class="location-address">1600 Michigan Avenue</div>
        </div>
    </div>

    <!-- Recent rides section -->
    <div class="recent-rides">
        <div class="section-title">Recent Rides</div>
        <div class="location-card">
            <div class="location-icon">📍</div>
            <div class="location-name">Central Park</div>
            <div class="location-address">New York, NY 10024</div>
        </div>
    </div>

    <!-- Bottom navigation -->
    <div class="bottom-nav">
        <div class="nav-button active">🚗 Rides</div>
        <div class="nav-button">🍔 Eats</div>
    </div>
</div>
""", unsafe_allow_html=True) 
