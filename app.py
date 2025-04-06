
import streamlit as st
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title="Cab Booking App", layout="centered")

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Custom CSS for mobile UI
st.markdown("""
    <style>
    body {
        background-color: #f8f8f8;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .service-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 10px;
        box-shadow: 0px 0px 5px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 10px;
    }
    .rounded-input {
        border-radius: 30px !important;
        padding: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 🚗 Rides   🍜 Delivery")

# Where to input
col1, col2 = st.columns([4, 1])
with col1:
    where_to = st.text_input("Where to?", placeholder="Where to?", label_visibility="collapsed")
with col2:
    st.button("Now ⏰")

# Saved Places
st.write("###")
st.markdown("#### 📍 Saved Places")
with st.container():
    st.markdown("**🏢 Work**  
1455 Market St", unsafe_allow_html=True)
    st.markdown("**🏠 Home**  
903 Sunrise Terr", unsafe_allow_html=True)

# Suggestions section
st.write("###")
st.markdown("#### 🔁 Suggestions")
sug1, sug2, sug3, sug4 = st.columns(4)
sug1.markdown('<div class="service-card">🚗<br>Ride</div>', unsafe_allow_html=True)
sug2.markdown('<div class="service-card">📦<br>Package</div>', unsafe_allow_html=True)
sug3.markdown('<div class="service-card">🕒<br>Reserve</div>', unsafe_allow_html=True)
sug4.markdown('<div class="service-card">🚘<br>Rent</div>', unsafe_allow_html=True)

# Service grid
st.write("###")
st.markdown("#### 🧭 Go Anywhere")
cols = st.columns(3)
services = [
    ("🚗", "Ride"), ("📦", "Package"), ("🕒", "Reserve"),
    ("🧑‍💻", "Hourly"), ("🔑", "Rent"), ("🚲", "2-Wheels"),
    ("🚆", "Transit"), ("🚌", "Charter"), ("🌍", "Explore")
]
for i in range(0, len(services), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(services):
            icon, label = services[i + j]
            cols[j].markdown(f'<div class="service-card">{icon}<br>{label}</div>', unsafe_allow_html=True)

# Optional: Add a ride planning section with images
st.write("###")
st.markdown("#### 🗓️ Ways to plan your trip")
img_cols = st.columns(2)
img_cols[0].image("https://source.unsplash.com/400x200/?calendar", caption="Plan your week")
img_cols[1].image("https://source.unsplash.com/400x200/?festival", caption="Festival Rides")

st.write("###")
st.success("✅ UI replicated. You can now add map, booking, and animation logic.")
