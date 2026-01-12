import streamlit as st
import requests
import time
from streamlit_lottie import st_lottie

# --- PAGE CONFIG ---
st.set_page_config(page_title="VitalPulse | Patient Portal", page_icon="🏥", layout="wide")

# --- APPLE STYLE CSS ---
st.markdown("""
    <style>
    /* Import Apple-like Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F5F5F7; /* Apple Off-White */
    }

    /* Glassmorphism Card Effect */
    .metric-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }

    .main-title {
        font-size: 42px;
        font-weight: 600;
        color: #1D1D1F;
        text-align: center;
        margin-bottom: 40px;
    }

    /* Hide Streamlit elements for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- LOAD ANIMATIONS ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

pulse_anim = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")

# --- HEADER ---
st.markdown('<p class="main-title">Health Overview</p>', unsafe_allow_html=True)

# --- SECTION 1: IOT VITALS ---
# In a real app, these would come from your backend via requests.get()
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""<div class="metric-card">
        <p style="color: #86868B; font-size: 14px; text-transform: uppercase;">Temperature</p>
        <p style="font-size: 32px; font-weight: 600; color: #1D1D1F;">98.6°F</p>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class="metric-card">
        <p style="color: #86868B; font-size: 14px; text-transform: uppercase;">Heart Rate</p>
        <p style="font-size: 32px; font-weight: 600; color: #FF2D55;">72 BPM</p>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class="metric-card">
        <p style="color: #86868B; font-size: 14px; text-transform: uppercase;">Oxygen (SpO2)</p>
        <p style="font-size: 32px; font-weight: 600; color: #007AFF;">98%</p>
    </div>""", unsafe_allow_html=True)

st.write("---")

# --- SECTION 2: DYNAMIC QUESTIONNAIRE ---
st.subheader("Symptom Assessment")
st.info("Please complete the following mandatory steps.")

with st.container():
    # Apple-style minimal checkboxes
    symptoms = []
    
    q1 = st.checkbox("Are you experiencing any physical discomfort?")
    
    if q1:
        symptoms.append("Discomfort")
        st.markdown("---")
        q2 = st.radio("Where is the discomfort located?", ["Chest", "Head", "Limbs", "Other"])
        
        if q2 == "Chest":
            symptoms.append("Chest Pain")
            q3 = st.checkbox("Is it a sharp, stabbing pain?")
            if q3: symptoms.append("Sharp Chest Pain")
        
        elif q2 == "Head":
            symptoms.append("Headache")
            st.select_slider("Severity of headache", options=["Mild", "Moderate", "Severe"])

# --- SECTION 3: DESCRIPTION & SUBMIT ---
st.write("---")
description = st.text_area("Detailed Description (Optional)", placeholder="Tell us more about how you feel...")

if st.button("Generate Diagnosis", use_container_width=True):
    if not q1:
        st.error("Please answer the mandatory questions.")
    else:
        with st.spinner("Analyzing data with AI..."):
            # Prepare data for backend
            payload = {
                "temp": 98.6,
                "hr": 72,
                "spo2": 98,
                "symptoms": symptoms,
                "text": description
            }
            
            # SIMULATING BACKEND CALL
            time.sleep(2) 
            
            # Display Result
            st.balloons()
            st.success("Analysis Complete")
            st.markdown("""
                <div class="metric-card" style="background: #E8F2FF; border: none;">
                    <h3 style="color: #007AFF;">Potential Condition: Mild Fatigue</h3>
                    <p>Suggested Action: Rest for 24 hours and monitor heart rate.</p>
                </div>
            """, unsafe_allow_html=True)

# Add a subtle animation at the bottom
st_lottie(pulse_anim, height=150, key="pulse")