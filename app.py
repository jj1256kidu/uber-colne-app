import streamlit as st
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="RideBook",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Base styles */
    .stApp {
        margin: 0 auto;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide Streamlit components */
    #MainMenu, header, footer {
        display: none !important;
    }

    /* Custom styles */
    .css-1d391kg {  /* Streamlit containers */
        padding: 1rem 1rem 10rem 1rem;
        max-width: 414px;
        margin: 0 auto;
    }

    .stTextInput > div > div > input {
        border-radius: 28px;
        padding: 16px 20px;
        font-size: 16px;
        border: none;
        background: #f8f9fa;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .stTextInput > div > div > input:focus {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* Location cards */
    .location-card {
        background: #f8f9fa;
        padding: 16px;
        border-radius: 16px;
        margin-bottom: 12px;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .location-card:hover {
        transform: translateY(-2px);
        background: #f0f0f0;
    }

    /* Services grid */
    .services-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin: 20px 0;
    }

    .service-item {
        background: white;
        border: 1px solid #f0f0f0;
        border-radius: 16px;
        padding: 16px 12px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .service-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }

    /* Suggestions scroll */
    .suggestions {
        display: flex;
        overflow-x: auto;
        gap: 12px;
        padding: 8px 0;
        margin: 16px 0;
        scrollbar-width: none;
    }

    .suggestions::-webkit-scrollbar {
        display: none;
    }

    .suggestion-btn {
        background: white;
        border: 1px solid #f0f0f0;
        border-radius: 24px;
        padding: 8px 20px;
        white-space: nowrap;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .suggestion-btn.active {
        background: black;
        color: white;
        border-color: black;
    }

    /* Section titles */
    .section-title {
        font-size: 20px;
        font-weight: 600;
        margin: 24px 0 16px 0;
        color: #1a1a1a;
    }
</style>
""", unsafe_allow_html=True)

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
