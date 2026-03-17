import streamlit as st
import requests
import time
import json
from streamlit_lottie import st_lottie

# --- CONFIGURATION ---
BACKEND_URL = "http://10.255.199.23:5000/predict"
SENSOR_URL = "http://10.255.199.23:5000/sensors"

st.set_page_config(page_title="VitalPulse | Patient Portal", page_icon="🏥", layout="wide")

# --- PREMIUM SPLASH SCREEN ---
st.markdown("""
<div id="vitalpulse-splash">
    <div class="splash-container">
        <h1 class="splash-text">VitalPulse</h1>
        <div class="pulse-ring"></div>
        <p class="tap-hint">Click anywhere to explore</p>
    </div>
</div>

<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');

/* Force-remove Streamlit margins and the white background 'bleeding' */
html, body, [data-testid="stAppViewContainer"] {
    margin: 0 !important;
    padding: 0 !important;
    background-color: #000000 !important; /* Prevents white edges when blurring */
}

#vitalpulse-splash {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.4); /* Darker backdrop for better contrast */
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    z-index: 9999999;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    font-family: 'Outfit', sans-serif;
}

.splash-container {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
}

.splash-text {
    font-size: clamp(60px, 12vw, 120px);
    font-weight: 900;
    margin: 0;
    letter-spacing: -4px;
    line-height: 1;
    color: #FFFFFF;
    text-shadow: 0 10px 30px rgba(0,0,0,0.2);
    /* High contrast gradient for visibility on any background */
    background: linear-gradient(180deg, #FFFFFF 0%, #E0E0E0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: textEntrance 1.2s cubic-bezier(0.23, 1, 0.32, 1) forwards;
}

.pulse-ring {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 200px;
    height: 200px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    z-index: -1;
    animation: ringPulse 4s infinite cubic-bezier(0.4, 0, 0.6, 1);
}

.tap-hint {
    margin-top: 40px;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 8px;
    color: rgba(255, 255, 255, 0.7);
    opacity: 0;
    animation: fadeIn 1s ease 0.8s forwards;
}

@keyframes textEntrance {
    0% { opacity: 0; transform: scale(0.95) translateY(20px); filter: blur(10px); }
    100% { opacity: 1; transform: scale(1) translateY(0); filter: blur(0); }
}

@keyframes ringPulse {
    0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
    50% { opacity: 0.4; }
    100% { transform: translate(-50%, -50%) scale(1.5); opacity: 0; }
}

@keyframes fadeIn {
    to { opacity: 1; }
}

/* Background App State */
/* Removing the double blur on .stApp to keep it 'glassy' not 'foggy' */
.stApp {
    transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.splash-active .stApp {
    transform: scale(1.02); /* Slight zoom for depth */
}

.splash-hidden {
    opacity: 0 !important;
    visibility: hidden !important;
    transform: scale(1.1) !important;
    pointer-events: none !important;
}
</style>
""", unsafe_allow_html=True)

# Inject the JavaScript to handle clicks and session persistence
# This targets the parent document to ensure the splash screen 
# can be controlled across Streamlit reruns.
import streamlit.components.v1 as components
components.html("""
<script>
    const parentDoc = window.parent.document;
    const splash = parentDoc.getElementById('vitalpulse-splash');

    function initSplash() {
        // Check if user already dismissed it in this session
        if (sessionStorage.getItem('splash_dismiss_vp') === 'true') {
            if (splash) splash.classList.add('splash-hidden');
            parentDoc.body.classList.remove('splash-active');
        } else {
            parentDoc.body.classList.add('splash-active');
            if (splash) splash.classList.remove('splash-hidden');
        }
    }

    if (splash) {
        splash.addEventListener('click', () => {
            splash.classList.add('splash-hidden');
            parentDoc.body.classList.remove('splash-active');
            sessionStorage.setItem('splash_dismiss_vp', 'true');
        });
    }

    initSplash();
</script>
""", height=0)

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
# --- REAL IOT DATA FETCH ---
def get_sensor_data():
    try:
        # Using localhost instead of 127.0.0.1 and increasing timeout to 2s
        response = requests.get(SENSOR_URL, timeout=2)
        if response.status_code == 200:
            data = response.json()
            temp_c = data.get("Sensor_Temp", 37.0)
            temp_f = (temp_c * 9/5) + 32
            return {
                "temp_c": round(temp_c, 1),
                "temp_f": round(temp_f, 1),
                "hr": data.get("Sensor_HR", 75),
                "spo2": data.get("Sensor_SpO2", 98)
            }
        else:
            print(f"Backend returned error: {response.status_code}")
    except Exception as e:
        # We use print instead of st.error here to avoid Threading/ScriptRunContext warnings
        print(f"📡 [STREAMLIT SYNC ERROR]: {e}")
    
    # Fallback values
    return {"temp_c": 0.0, "temp_f": 0.0, "hr": 0, "spo2": 0} 

# --- INITIALIZE SESSION STATE ---
if "latest_sensors" not in st.session_state:
    st.session_state.latest_sensors = get_sensor_data()

# --- HEADER ---
st.markdown('<p class="main-title">Health Overview</p>', unsafe_allow_html=True)

# --- SECTION 1: IOT VITALS (Live Fragment) ---
@st.fragment(run_every=2) # 2 seconds refresh
def sync_vitals():
    sensor_vals = get_sensor_data()
    # Check if we have real data (non-zero)
    if sensor_vals['temp_c'] > 0:
        badge_style = "background: #34C759; color: white; padding: 2px 8px; border-radius: 10px; font-size: 10px;"
        badge_text = "LIVE"
    else:
        badge_style = "background: #FF9500; color: white; padding: 2px 8px; border-radius: 10px; font-size: 10px;"
        badge_text = "SYNCING"

    st.markdown(f'<span style="{badge_style}">{badge_text}</span> <span style="font-size: 12px; color: gray;">Last Check: {time.strftime("%H:%M:%S")}</span>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        temp_c = sensor_vals['temp_c']
        temp_f = sensor_vals['temp_f']
        if temp_c > 0:
            temp_display = f"{temp_c}°C / {temp_f}°F"
        else:
            temp_display = "---"
            
        st.markdown(f"""<div class="metric-card">
            <p style="color: #86868B; font-size: 14px; text-transform: uppercase;">Temperature</p>
            <p style="font-size: 28px; font-weight: 600; color: #1D1D1F;">{temp_display}</p>
        </div>""", unsafe_allow_html=True)
        
    with col2:
        hr_display = f"{sensor_vals['hr']} BPM" if sensor_vals['hr'] > 0 else "---"
        st.markdown(f"""<div class="metric-card">
            <p style="color: #86868B; font-size: 14px; text-transform: uppercase;">Heart Rate</p>
            <p style="font-size: 32px; font-weight: 600; color: #FF2D55;">{hr_display}</p>
        </div>""", unsafe_allow_html=True)
        
    with col3:
        spo2_display = f"{sensor_vals['spo2']}%" if sensor_vals['spo2'] > 0 else "---"
        st.markdown(f"""<div class="metric-card">
            <p style="color: #86868B; font-size: 14px; text-transform: uppercase;">Oxygen (SpO2)</p>
            <p style="font-size: 32px; font-weight: 600; color: #007AFF;">{spo2_display}</p>
        </div>""", unsafe_allow_html=True)
    st.caption(f"✨ Live Sync active | Last Check: {time.strftime('%H:%M:%S')}")
    # Store in session state so the rest of the app (like Diagnosis button) can see it
    st.session_state.latest_sensors = sensor_vals
    return sensor_vals

# Render the fragment
sync_vitals()

# Use session state for the rest of the script
sensor_vals_for_logic = st.session_state.latest_sensors

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
    gender_val = st.selectbox("Gender", ["Male", "Female"])
with c2:
    bp_val = st.selectbox("Blood Pressure", ["Normal", "High", "Low"]) 
    chol_val = st.selectbox("Cholesterol Level", ["Normal", "High"])

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

# Get sorted list based on CURRENT sensor values (from session state)
SORTED_SYMPTOMS = get_prioritized_symptoms({
    "temp": sensor_vals_for_logic.get("temp_f", 0),
    "hr": sensor_vals_for_logic.get("hr", 0),
    "spo2": sensor_vals_for_logic.get("spo2", 0)
}, ALL_SYMPTOMS)

st.subheader("Symptoms Checklist")
st.info("Based on your sensors, we've prioritized relevant symptoms. Please select any applicable symptoms.")



# --- SECTION 3: DESCRIPTION & SYMPTOMS ---
# We place the description first so it can influence the selections
description = st.text_area("Detailed Description (Optional)", placeholder="Tell us more about how you feel... e.g., 'I have a high fever and my chest hurts'")

# Extraction logic from text description
def extract_symptoms_from_text(text, all_symptoms):
    extracted = set()
    if not text:
        return extracted
    text = text.lower().replace("-", " ").replace(",", " ")
    for sym in all_symptoms:
        # Match symptom parts (e.g., 'chest_pain' matches 'chest pain' or 'pain in chest')
        search_term = sym.replace("_", " ")
        if search_term in text:
            extracted.add(sym)
    return extracted

symptoms_from_text = extract_symptoms_from_text(description, ALL_SYMPTOMS)

# Checklist selections
selected_symptoms_from_checklist = [s for s in ALL_SYMPTOMS if st.session_state.get(s, False)]

# Final merged list for calculation
# Union of checklist selections + text-extracted keywords
selected_symptoms = list(set(selected_symptoms_from_checklist) | symptoms_from_text)

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

# --- SECTION 4: DIAGNOSIS GENERATION ---
st.write("---")
    
if st.button("Generate Diagnosis", use_container_width=True):
    if not selected_symptoms:
        st.warning("⚠️ Please select at least one symptom to get a prediction.")
    else:
        with st.spinner("Analyzing Vitals & Symptoms with AI..."):
            # 1. CONSTRUCT FINAL PAYLOAD
            # We use the LATEST data captured in session state
            current_vitals = st.session_state.latest_sensors
            
            final_payload = {
                "Sensor_Temp": current_vitals.get('temp_c', 0), 
                "Sensor_HR": current_vitals.get('hr', 0),
                "Sensor_SpO2": current_vitals.get('spo2', 0)
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
                            <p style="font-size: 12px; color: gray; margin-top: 10px;">Based on HR: {current_vitals.get('hr', 0)} and reported symptoms.</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"Server Error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the Backend. Is 'server.py' (Flask) running?")