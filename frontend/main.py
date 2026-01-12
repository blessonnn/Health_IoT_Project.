import streamlit as st
import requests
import time
import json
from streamlit_lottie import st_lottie

# --- CONFIGURATION ---
BACKEND_URL = "http://127.0.0.1:5000/predict"  # Point to your Flask API

st.set_page_config(page_title="VitalPulse | Patient Portal", page_icon="🏥", layout="wide")

# --- APPLE STYLE CSS (Kept exactly as you wrote it) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F5F5F7;
    }
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
    .metric-card:hover { transform: translateY(-5px); }
    .main-title {
        font-size: 42px; font-weight: 600; color: #1D1D1F; text-align: center; margin-bottom: 40px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

pulse_anim = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")

# --- MOCK IOT DATA FETCH ---
# In the future, replace this with requests.get('http://esp32-ip-address/data')
def get_sensor_data():
    return {
        "temp": 99.1,  # Example: Slightly high
        "hr": 92,      # Example: Elevated
        "spo2": 96
    }

sensor_vals = get_sensor_data()

# --- HEADER ---
st.markdown('<p class="main-title">Health Overview</p>', unsafe_allow_html=True)

# --- SECTION 1: IOT VITALS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""<div class="metric-card">
        <p style="color: #86868B; font-size: 14px; text-transform: uppercase;">Temperature</p>
        <p style="font-size: 32px; font-weight: 600; color: #1D1D1F;">{sensor_vals['temp']}°F</p>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class="metric-card">
        <p style="color: #86868B; font-size: 14px; text-transform: uppercase;">Heart Rate</p>
        <p style="font-size: 32px; font-weight: 600; color: #FF2D55;">{sensor_vals['hr']} BPM</p>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class="metric-card">
        <p style="color: #86868B; font-size: 14px; text-transform: uppercase;">Oxygen (SpO2)</p>
        <p style="font-size: 32px; font-weight: 600; color: #007AFF;">{sensor_vals['spo2']}%</p>
    </div>""", unsafe_allow_html=True)

st.write("---")

# --- SECTION 2: DYNAMIC QUESTIONNAIRE ---
st.subheader("Symptom Assessment")
st.info("Please complete the following mandatory steps.")

# We will build a dictionary to send to the backend
# Keys MUST match the CSV column names from your Kaggle dataset!
symptom_payload = {}

with st.container():
    q1 = st.checkbox("Are you experiencing any physical discomfort?")
    
    if q1:
        st.markdown("---")
        q2 = st.radio("Where is the discomfort located?", ["Chest", "Head", "Stomach", "Other"])
        
        # MAPPING LOGIC: User Choice -> Model Feature Name
        if q2 == "Chest":
            symptom_payload["chest_pain"] = 1
            q3 = st.checkbox("Is it a sharp, stabbing pain?")
            # Note: Ensure 'sharp_chest_pain' exists in your CSV, or map it to a known column
            if q3: symptom_payload["stomach_pain"] = 1 # Example mapping, adjust to your CSV
        
        elif q2 == "Head":
            symptom_payload["headache"] = 1
            severity = st.select_slider("Severity", options=["Mild", "Moderate", "Severe"])
        
        elif q2 == "Stomach":
             symptom_payload["stomach_pain"] = 1
             if st.checkbox("Are you vomiting?"):
                 symptom_payload["vomiting"] = 1

# --- SECTION 3: DESCRIPTION & SUBMIT ---
st.write("---")
description = st.text_area("Detailed Description (Optional)", placeholder="Tell us more about how you feel...")

if st.button("Generate Diagnosis", use_container_width=True):
    if not q1 and not symptom_payload:
         # It's okay if they just have sensors, but usually we want at least one symptom
         # For this demo, we allow it to proceed with just sensor data
         pass

    with st.spinner("Analyzing Vitals & Symptoms with AI..."):
        
        # 1. CONSTRUCT FINAL PAYLOAD
        # Combine Sensor Data + Symptom Data
        final_payload = {
            "Sensor_Temp": sensor_vals['temp'], # Must match backend expectation
            "Sensor_HR": sensor_vals['hr'],
            "Sensor_SpO2": sensor_vals['spo2']
        }
        # Merge the symptoms into the payload
        final_payload.update(symptom_payload)

        # 2. SEND TO BACKEND
        try:
            response = requests.post(BACKEND_URL, json=final_payload)
            
            if response.status_code == 200:
                result = response.json()
                
                # 3. DISPLAY RESULTS
                st.balloons()
                st.success("Analysis Complete")
                
                disease = result.get("disease", "Unknown")
                suggestion = result.get("suggestion", "Consult a doctor.")
                
                st.markdown(f"""
                    <div class="metric-card" style="background: #E8F2FF; border: none;">
                        <h3 style="color: #007AFF;">Potential Condition: {disease}</h3>
                        <p style="font-size: 18px;"><strong>Suggestion:</strong> {suggestion}</p>
                        <p style="font-size: 12px; color: gray; margin-top: 10px;">Based on HR: {sensor_vals['hr']} and reported symptoms.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"Server Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the Backend. Is 'main.py' (Flask) running?")

# Animation
if pulse_anim:
    st_lottie(pulse_anim, height=150, key="pulse")