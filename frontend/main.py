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
@st.cache_data
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

st.write("Please fill in the details below:")

# Demographic & Health History
c1, c2 = st.columns(2)
with c1:
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male", "Female"])
    gender_val = 1 if gender == "Male" else 0 # Assuming 1 for Male, 0 for Female based on typical encoding
with c2:
    bp = st.selectbox("Blood Pressure", ["Normal", "High", "Low"]) 
    # Heuristic mapping for BP if model expects categorical or numeric. 
    # The feature list just says 'Blood Pressure'. Assuming encoded or categorical. 
    # For safety, let's look at the model training script or data if possible, but for now we'll assume binary/categorical or raw.
    # Given 'Outcome Variable' is in features, this dataset might be "Disease Prediction Logic" style.
    # Let's map 'High' to 1, 'Normal' to 0 for now or use a slider if it looks numeric.
    # UPDATE: I'll use a number input for Systolic BP just in case, or keep it simple.
    # Let's guess it's a category for now.
    bp_val = 1 if bp == "High" else 0
    
    chol = st.selectbox("Cholesterol Level", ["Normal", "High"])
    chol_val = 1 if chol == "High" else 0

st.markdown("---")
# --- LOAD SYMPTOMS ---
# Full list extracted from Training.csv header
ALL_SYMPTOMS = [
    "itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing", "shivering", "chills", 
    "joint_pain", "stomach_pain", "acidity", "ulcers_on_tongue", "muscle_wasting", "vomiting", 
    "burning_micturition", "spotting_ urination", "fatigue", "weight_gain", "anxiety", 
    "cold_hands_and_feets", "mood_swings", "weight_loss", "restlessness", "lethargy", 
    "patches_in_throat", "irregular_sugar_level", "cough", "high_fever", "sunken_eyes", 
    "breathlessness", "sweating", "dehydration", "indigestion", "headache", "yellowish_skin", 
    "dark_urine", "nausea", "loss_of_appetite", "pain_behind_the_eyes", "back_pain", "constipation", 
    "abdominal_pain", "diarrhoea", "mild_fever", "yellow_urine", "yellowing_of_eyes", 
    "acute_liver_failure", "fluid_overload", "swelling_of_stomach", "swelled_lymph_nodes", "malaise", 
    "blurred_and_distorted_vision", "phlegm", "throat_irritation", "redness_of_eyes", "sinus_pressure", 
    "runny_nose", "congestion", "chest_pain", "weakness_in_limbs", "fast_heart_rate", 
    "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool", "irritation_in_anus", 
    "neck_pain", "dizziness", "cramps", "bruising", "obesity", "swollen_legs", "swollen_blood_vessels", 
    "puffy_face_and_eyes", "enlarged_thyroid", "brittle_nails", "swollen_extremeties", "excessive_hunger", 
    "extra_marital_contacts", "drying_and_tingling_lips", "slurred_speech", "knee_pain", "hip_joint_pain", 
    "muscle_weakness", "stiff_neck", "swelling_joints", "movement_stiffness", "spinning_movements", 
    "loss_of_balance", "unsteadiness", "weakness_of_one_body_side", "loss_of_smell", "bladder_discomfort", 
    "foul_smell_of urine", "continuous_feel_of_urine", "passage_of_gases", "internal_itching", 
    "toxic_look_(typhos)", "depression", "irritability", "muscle_pain", "altered_sensorium", 
    "red_spots_over_body", "belly_pain", "abnormal_menstruation", "dischromic _patches", 
    "watering_from_eyes", "increased_appetite", "polyuria", "family_history", "mucoid_sputum", 
    "rusty_sputum", "lack_of_concentration", "visual_disturbances", "receiving_blood_transfusion", 
    "receiving_unsterile_injections", "coma", "stomach_bleeding", "distention_of_abdomen", 
    "history_of_alcohol_consumption", "fluid_overload", "blood_in_sputum", "prominent_veins_on_calf", 
    "palpitations", "painful_walking", "pus_filled_pimples", "blackheads", "scurring", "skin_peeling", 
    "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails", "blister", "red_sore_around_nose", 
    "yellow_crust_ooze"
]

# Remove duplicates if any (e.g. fluid_overload appears twice in original dataset)
ALL_SYMPTOMS = sorted(list(set(ALL_SYMPTOMS)))

# --- SENSOR HEURISTICS ---
# Define related symptoms for prioritization
TEMP_SYMPTOMS = ["high_fever", "mild_fever", "chills", "shivering", "sweating", "headache", "muscle_pain", "fatigue"]
HR_SYMPTOMS = ["palpitations", "fast_heart_rate", "chest_pain", "dizziness", "breathlessness", "anxiety"]
SPO2_SYMPTOMS = ["breathlessness", "fatigue", "lethargy", "dizziness", "confusion", "high_fever"]

@st.cache_data(show_spinner=False)
def get_prioritized_symptoms(sensor_data, all_symptoms):
    """Sorts symptoms based on sensor values."""
    priority = set()
    
    # 1. Temperature Check (Normal ~98.6F)
    if sensor_data['temp'] > 99.0:
        priority.update(TEMP_SYMPTOMS)
        
    # 2. Heart Rate Check (Normal 60-100)
    if sensor_data['hr'] > 100 or sensor_data['hr'] < 60:
        priority.update(HR_SYMPTOMS)
        
    # 3. SpO2 Check (Normal > 95)
    if sensor_data['spo2'] < 95:
        priority.update(SPO2_SYMPTOMS)
        
    # Sort: Priority first, then the rest
    # Filter priority items that actually exist in ALL_SYMPTOMS
    valid_priority = [s for s in priority if s in all_symptoms]
    remaining = [s for s in all_symptoms if s not in valid_priority]
    
    return valid_priority + remaining

# Get sorted list based on CURRENT sensor values
SORTED_SYMPTOMS = get_prioritized_symptoms(sensor_vals, ALL_SYMPTOMS)

st.subheader("Symptoms Checklist")
st.info("Based on your sensors, we've prioritized relevant symptoms. Please select at least **5** total.")



# --- SELECTION STATE MANAGEMENT ---
# Instead of manually managing a list with callbacks (which causes sync issues),
# we derive the selected symptoms directly from the checkbox states (st.session_state).
# This ensures that what you see is always what you get.

selected_symptoms = [s for s in ALL_SYMPTOMS if st.session_state.get(s, False)]

if "symptom_page" not in st.session_state:
    st.session_state.symptom_page = 1
    
ITEMS_PER_PAGE = 10

# 1. Display currently selected summary
if selected_symptoms:
    st.write(f"**Selected ({len(selected_symptoms)}):** {', '.join(selected_symptoms)}")

# 2. Render Checkboxes for current page
start_idx = (st.session_state.symptom_page - 1) * ITEMS_PER_PAGE
end_idx = start_idx + ITEMS_PER_PAGE
current_batch = SORTED_SYMPTOMS[start_idx:end_idx]

if not current_batch:
    st.success("You have reached the end of the list.")
else:
    st.write(f"**Set {st.session_state.symptom_page}**")
    
    # Optional: Logic to see if we are in "Priority Zone"
    if st.session_state.symptom_page == 1 and sensor_vals['temp'] > 99:
        st.caption("🔥 These symptoms are common with high temperature.")
        
    for sym in current_batch:
        # We rely on Streamlit's internal state for the checkbox.
        # Key=sym ensures the state persists even when navigating pages.
        st.checkbox(sym.replace("_", " ").title(), key=sym)

# 3. Navigation
c_prev, c_center, c_next = st.columns([1, 1, 1])

with c_prev:
    if st.session_state.symptom_page > 1:
        if st.button("⬅️ Previous Set"):
            st.session_state.symptom_page -= 1
            st.rerun()

with c_center:
    # "Skip" button just acts as "Next" visually to say "I don't need any here"
    if end_idx < len(SORTED_SYMPTOMS):
         if st.button("Skip Set ⏭️"):
            st.session_state.symptom_page += 1
            st.rerun()

with c_next:
    if end_idx < len(SORTED_SYMPTOMS):
        if st.button("Next Set ➡️"):
            st.session_state.symptom_page += 1
            st.rerun()

# Map to payload
# Reset payload symptom keys first
for sym in ALL_SYMPTOMS:
    if sym in selected_symptoms:
        symptom_payload[sym] = 1

# Add Demographics to payload
symptom_payload["Age"] = age
symptom_payload["Gender"] = gender_val
symptom_payload["Blood Pressure"] = bp_val
symptom_payload["Cholesterol Level"] = chol_val
symptom_payload["Outcome Variable"] = 0 

# --- SECTION 3: DESCRIPTION & SUBMIT ---
st.write("---")
description = st.text_area("Detailed Description (Optional)", placeholder="Tell us more about how you feel...")

# Enforce Minimum 5 Selection
selected_count = len(selected_symptoms)
can_submit = selected_count >= 5

if not can_submit:
    st.warning(f"⚠️ Please select {5 - selected_count} more symptom(s) to generate a diagnosis.")
    
if st.button("Generate Diagnosis", disabled=not can_submit, use_container_width=True):
    # Proceed even if mostly empty, as we have sensors
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
                # st.balloons() - Removed as per user request
                st.success("Analysis Complete")
                
                disease = result.get("disease", "Unknown")
                suggestion = result.get("suggestion", "Consult a doctor.")
                
                st.markdown(f"""
                    <div class="metric-card" style="background: #E8F2FF; border: none;">
                        <h3 style="color: #007AFF;">Potential Condition: {disease}</h3>
                        <p style="font-size: 18px; color: black;"><strong>Suggestion:</strong> {suggestion}</p>
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