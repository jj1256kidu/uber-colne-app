import streamlit as st
from datetime import datetime
from styles.theme import get_css_theme

# Configure the page
st.set_page_config(
    page_title="RideBook",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply the theme
st.markdown(get_css_theme(), unsafe_allow_html=True)

# Get greeting
def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"

# Services data
SERVICES = [
    {"name": "Ride", "icon": "🚗"},
    {"name": "Package", "icon": "📦"},
    {"name": "Hourly", "icon": "⏰"},
    {"name": "Rent", "icon": "🔑"},
    {"name": "Transit", "icon": "🚇"},
    {"name": "Charter", "icon": "🚐"},
    {"name": "Explore", "icon": "🗺️"},
    {"name": "Travel", "icon": "✈️"}
]

# Suggestions
SUGGESTIONS = ["Ride", "Reserve", "Package", "Rent"]

# Main app
def main():
    # Header
    st.markdown(f"<h1 style='font-size: 24px; font-weight: 600; margin-bottom: 4px;'>{get_greeting()}, Joost</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; margin-bottom: 20px;'>Where are you going today?</p>", unsafe_allow_html=True)

    # Search box
    col1, col2 = st.columns([6, 1])
    with col1:
        st.text_input("", placeholder="Where to?", label_visibility="collapsed")
    with col2:
        st.markdown("<div style='text-align: center; padding-top: 15px;'>📍</div>", unsafe_allow_html=True)

    # Suggestions
    st.markdown("<div class='suggestions'>", unsafe_allow_html=True)
    for suggestion in SUGGESTIONS:
        st.markdown(
            f"<button class='suggestion-btn {'active' if suggestion == 'Ride' else ''}'>{suggestion}</button>",
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # Services section
    st.markdown("<div class='section-title'>Go Anywhere, Get Anything</div>", unsafe_allow_html=True)
    
    # Services grid
    st.markdown("<div class='services-grid'>", unsafe_allow_html=True)
    for service in SERVICES:
        st.markdown(f"""
            <div class='service-item'>
                <div style='font-size: 24px; margin-bottom: 8px;'>{service['icon']}</div>
                <div style='font-size: 14px; font-weight: 500;'>{service['name']}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Saved locations
    st.markdown("<div class='section-title'>Saved Places</div>", unsafe_allow_html=True)
    
    # Work location
    st.markdown("""
        <div class='location-card'>
            <div style='font-size: 24px; margin-bottom: 8px;'>🏢</div>
            <div style='font-weight: 600; margin-bottom: 4px;'>Work</div>
            <div style='font-size: 13px; color: #666;'>1455 Market Street</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Home location
    st.markdown("""
        <div class='location-card'>
            <div style='font-size: 24px; margin-bottom: 8px;'>🏠</div>
            <div style='font-weight: 600; margin-bottom: 4px;'>Home</div>
            <div style='font-size: 13px; color: #666;'>1600 Michigan Avenue</div>
        </div>
    """, unsafe_allow_html=True)

    # Bottom navigation
    st.markdown("""
        <div style='
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 414px;
            background: white;
            padding: 16px;
            display: flex;
            justify-content: space-around;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
        '>
            <div style='
                background: black;
                color: white;
                padding: 12px 32px;
                border-radius: 24px;
                font-weight: 500;
            '>🚗 Rides</div>
            <div style='
                padding: 12px 32px;
                border-radius: 24px;
                color: #666;
                font-weight: 500;
            '>🍔 Eats</div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 
