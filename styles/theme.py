def get_css_theme():
    return """
<style>
    /* Base Theme & Reset */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    .stApp {
        background: #f8f8f8 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
        color: #1a1a1a;
    }

    /* Hide Streamlit Elements */
    #MainMenu, header, footer {
        display: none !important;
    }

    /* Mobile Container */
    .mobile-container {
        max-width: 414px;
        margin: 0 auto;
        padding: 24px;
        background: white;
        min-height: 100vh;
    }

    /* Typography */
    .text-h1 {
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.4px;
        margin-bottom: 8px;
    }

    .text-subtitle {
        font-size: 15px;
        color: #666;
        margin-bottom: 24px;
    }

    .text-label {
        font-size: 14px;
        font-weight: 500;
    }

    /* Input Fields */
    .stTextInput > div > div > input {
        border-radius: 28px;
        padding: 16px 20px;
        height: 56px;
        font-size: 16px;
        border: none;
        background: #f8f8f8;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }

    .stTextInput > div > div > input:focus {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        background: white;
    }

    /* Cards */
    .card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }

    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* Service Grid */
    .services-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin: 24px 0;
    }

    .service-item {
        background: white;
        border-radius: 16px;
        padding: 20px 16px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid #f0f0f0;
    }

    .service-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .service-icon {
        font-size: 28px;
        margin-bottom: 8px;
    }

    .service-name {
        font-size: 13px;
        font-weight: 500;
    }

    /* Suggestions Scroll */
    .suggestions-scroll {
        display: flex;
        overflow-x: auto;
        gap: 12px;
        padding: 8px 0;
        margin: 16px 0;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
    }

    .suggestions-scroll::-webkit-scrollbar {
        display: none;
    }

    .suggestion-pill {
        background: white;
        border: 1px solid #f0f0f0;
        border-radius: 24px;
        padding: 12px 24px;
        font-size: 14px;
        font-weight: 500;
        white-space: nowrap;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .suggestion-pill:hover {
        background: #f8f8f8;
    }

    .suggestion-pill.active {
        background: #1a1a1a;
        color: white;
        border-color: #1a1a1a;
    }

    /* Location Cards */
    .location-card {
        background: #f8f8f8;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .location-card:hover {
        background: #f0f0f0;
    }

    .location-icon {
        font-size: 24px;
        margin-bottom: 12px;
    }

    .location-name {
        font-weight: 600;
        margin-bottom: 4px;
    }

    .location-address {
        font-size: 13px;
        color: #666;
    }

    /* Bottom Navigation */
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
        background: #f8f8f8;
    }

    /* Section Headers */
    .section-header {
        font-size: 20px;
        font-weight: 600;
        margin: 32px 0 16px 0;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animate-in {
        animation: fadeIn 0.3s ease forwards;
    }

    /* Touch Interactions */
    @media (hover: none) {
        .card:hover,
        .service-item:hover,
        .location-card:hover {
            transform: none;
        }
    }

    /* Active States */
    .button:active,
    .card:active,
    .service-item:active {
        transform: scale(0.98);
    }
</style>
""" 
