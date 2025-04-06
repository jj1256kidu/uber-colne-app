/* Main theme colors */
:root {
    --primary-color: #276EF1;
    --secondary-color: #95A5A6;
    --background-color: #FFFFFF;
    --text-color: #2C3E50;
}

/* Card styles */
.metric-card {
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
}

.driver-card {
    background-color: white;
    border-radius: 15px;
    padding: 25px;
    margin: 15px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    text-align: center;
}

.driver-card img {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    margin-bottom: 10px;
}

.status-card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 15px;
    margin: 15px 0;
}

/* Progress bar */
.progress-bar {
    width: 100%;
    height: 10px;
    background-color: #e9ecef;
    border-radius: 5px;
    overflow: hidden;
    margin-top: 10px;
}

.progress {
    height: 100%;
    background-color: var(--primary-color);
    transition: width 0.3s ease;
}

/* Button styles */
.stButton button {
    border-radius: 25px;
    padding: 10px 25px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Dark mode adjustments */
@media (prefers-color-scheme: dark) {
    .metric-card, .driver-card {
        background-color: #2C3E50;
        color: white;
    }
    
    .status-card {
        background-color: #34495E;
        color: white;
    }
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.animate-fade-in {
    animation: fadeIn 0.5s ease-in;
}

/* Mobile responsiveness */
@media screen and (max-width: 768px) {
    .metric-card, .driver-card, .status-card {
        padding: 15px;
        margin: 8px 0;
    }
}

/* Ride options styling */
.ride-option {
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #ddd;
    margin: 10px 0;
    cursor: pointer;
}

.ride-option:hover {
    background-color: #f8f9fa;
}

/* Payment form styling */
.payment-card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Fare display */
.fare-card {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    margin: 20px 0;
}

/* Login form styling */
.login-container {
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    max-width: 400px;
    margin: 0 auto;
}

/* Rating stars */
.rating {
    color: #ffd700;
    font-size: 24px;
}

/* History item styling */
.history-item {
    border-left: 4px solid var(--primary-color);
    padding-left: 15px;
    margin: 10px 0;
} 
