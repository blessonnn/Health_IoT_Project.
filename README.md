# Health Monitoring & Disease Prediction System (VitalPulse)

## 📌 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Current Status & Recent Updates](#2-current-status--recent-updates)
3. [How It Works](#3-how-it-works)
4. [Technology Stack & Tools Used](#4-technology-stack--tools-used)
5. [System Architecture](#5-system-architecture)
6. [Frontend to Backend Connection](#6-frontend-to-backend-connection)
7. [Machine Learning Model Build Process](#7-machine-learning-model-build-process)
8. [API Details](#8-api-details)
9. [Detailed Code Walkthrough](#9-detailed-code-walkthrough)
10. [How to Run the Project](#10-how-to-run-the-project)

---

## 10. How to Run the Project

Yes, since this project relies on specific Python libraries (like Flask, Streamlit, Scikit-Learn, and Pandas), you need to activate the Virtual Environment (`venv`) where these dependencies are installed before running anything.

### Step 1: Activate the Virtual Environment
Open your terminal (Command Prompt or PowerShell) inside the `Health_IoT_Project` folder and run:
```bash
# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```
*(You will see `(venv)` appear at the beginning of your terminal prompt once it's activated.)*

### Step 2: Start the Backend (Flask API)
The backend must be running for the frontend to make predictions. Run this in your terminal:
```bash
python backend/server.py
```
*(Leave this terminal running. It will start the server on `http://127.0.0.1:5000`)*

### Step 3: Start the Frontend (Streamlit Portal)
Open a **new** terminal window, activate the `venv` again, and run the frontend app:
```bash
# Don't forget to activate venv in the new terminal!
venv\Scripts\activate

streamlit run frontend/main.py
```
*(This will automatically open the Patient Portal in your web browser.)*

---

## 1. Project Overview

**VitalPulse** is a Health Monitoring & Disease Prediction System designed to bridge the gap between real-time physiological data (like temperature, heart rate, and oxygen levels from IoT sensors) and patient-reported symptoms. 

By taking both numeric vitals and qualitative symptoms, the system uses an AI-powered Machine Learning classification model to predict potential diseases and prescribe preliminary precautions or health suggestions to the patient.

---

## 2. Current Status & Recent Updates

**Current Build Version:** v2.1.0 (Stable)

### ✅ **Milestones Achieved:**
- **100% Model Accuracy**: The Random Forest Classifier has reached the highest possible accuracy on the current training dataset (4920 records), ensuring high-confidence predictions.
- **Natural Language Symptom Extraction**: Users can now describe their symptoms in plain English. The system automatically extracts key symptoms from the text using a keyword-mapping algorithm, reducing the need for manual checkbox selection.
- **Dynamic UX Prioritization**: The interface now intelligently re-orders the symptom list based on real-time IoT sensor data. (e.g., Fever-related symptoms move to the top if the temperature is high).
- **Premium Apple-Style UI**: The portal features a modern "Glassmorphism" design, a dynamic splash screen with pulse animations, and interactive metric cards.
- **Robust Feature Mapping**: The backend now supports case-insensitive mapping and dynamic encoding for demographic data (Gender, BP, Cholesterol).

### 🛠️ **In Progress:**
- [ ] **Real-time ESP32 Integration**: Transitioning from mock sensor data to real-time HTTP streams from IoT hardware.
- [ ] **Multi-language Support**: Expanding the symptom extraction to support more languages.
- [ ] **User History Dashboard**: Adding a database layer to track patient diagnostics over time.

---

## 3. How It Works

The lifecycle of a single user request follows these steps:

1. **User Action:** The patient opens the Patient Portal (built with Streamlit).
2. **Data Mocking/Fetching:** The app fetches simulated or real "Sensor Data" (Temperature, Heart Rate, SpO2) representing IoT wearables.
3. **Dynamic Assessment:** Depending on the vitals, the system dynamically prioritizes specific symptoms (e.g., if temperature > 99.0°F, fever-related symptoms appear first).
4. **Data Input:** The user inputs their age, gender, blood pressure, cholesterol, and checks applicable symptom boxes.
5. **Transmission:** The frontend packages this mixed data into a JSON payload and sends it via an HTTP POST request to the backend.
6. **Processing & Inference:** The Flask Backend maps these inputs to a feature vector (an array of numbers). This array is fed into a pre-trained Random Forest model.
7. **Response & Display:** The model predicts a disease index, which is decoded into a readable string (e.g., "Flu"). The backend fetches a relevant suggestion from a JSON database and sends it back to the frontend, which displays a metric card with the diagnosis.

---

## 3. Technology Stack & Tools Used

### **Languages**
* **Python 3:** The entire stack, from frontend interface to backend routing and machine learning, is built using Python.

### **Frontend Tools**
* **Streamlit:** A fast, Python-based web UI framework used to build the interactive patient portal.
* **Requests:** A Python HTTP library used to communicate with the backend.
* **Streamlit-Lottie:** Used to insert dynamic animations (e.g., pulse animations) into the web app.

### **Backend Tools**
* **Flask:** A lightweight WSGI web application micro-framework used to build the REST API.
* **JSON:** Used as the medium of data transfer between the frontend and backend, as well as for storing the suggestions database (`suggestions.json`).

### **Machine Learning Tools**
* **Scikit-Learn (sklearn):** Used for creating, training, and evaluating the Random Forest Classifier.
* **Pandas:** Used for data manipulation, cleaning, and preprocessing of the CSV datasets.
* **Joblib:** Used for serializing (saving) and deserializing (loading) the trained machine learning model and label encoders securely.

---

## 4. System Architecture

The architecture relies on decoupling the UI from the processing logic:

1. **Frontend (User Interface):** Found in `frontend/main.py`. This layer represents the client-side logic and visualization.
2. **Backend (API Gateway & Inference Server):** Found in `backend/server.py`. Handles data formatting and model invocation.
3. **Machine Learning Core:** Found in `backend/train_model.py` and saved natively as `health_model.pkl`. This is the intelligence or "Brain" of the project that handles the actual prediction logic based on training datasets.

---

## 5. Frontend to Backend Connection

The connection between the frontend and backend works via standard RESTful API communication.

**1. The Request (Frontend)**
Inside `frontend/main.py`, once the user clicks "Generate Diagnosis", the UI bundles all inputs into a Python dictionary:
```python
final_payload = {
    "Sensor_Temp": 99.1,
    "Sensor_HR": 92,
    "Sensor_SpO2": 96,
    "Age": 30,
    "itching": 1,
    ...
}
```
It uses the `requests` library to make a `POST` request to the backend's exposed endpoint:
```python
response = requests.post("http://127.0.0.1:5000/predict", json=final_payload)
```

**2. The Response (Backend)**
Inside `backend/server.py`, Flask listens to requests on the `/predict` route. It receives the JSON payload:
```python
data = request.json
```
After making a prediction, it returns a JSON response back to the frontend:
```python
return jsonify({
    "disease": "Typhoid",
    "description": "Information about the disease.",
    "suggestion": "Consult a doctor..."
})
```
The frontend parses `response.json()` and updates the visual UI accordingly.

---

## 6. Machine Learning Model Build Process

The ML model is built using `backend/train_model.py`. Here is how the "Brain" is trained:

1. **Data Loading:** The script reads historical patient data from `data/final_train_data.csv` using Pandas.
2. **Feature vs. Target Separation:** It drops unnecessary columns, storing input features (like sensor values and symptoms) in `X` and the target disease label in `y`.
3. **Data Encoding:** Machine learning models only understand numbers. The script uses Scikit-Learn’s `LabelEncoder` to convert categorical text (like "Male"/"Female" or disease names like "Diabetes") into integers.
4. **Train/Test Split:** The dataset is split into 80% training data and 20% testing data (`train_test_split`).
5. **Model Initialization:** A `RandomForestClassifier` with 100 decision trees (`n_estimators=100`) is highly effective for medical symptoms because it resists overfitting on datasets with many features.
6. **Training & Evaluation:** The model runs `.fit(X_train, y_train)` to learn the patterns. It is then tested against `X_test` using `accuracy_score`.
7. **Serialization:** Finally, the model, the feature list, and all the encoders required to properly map text-to-numbers in the future are grouped in a dictionary and saved into `health_model.pkl` using `joblib.dump()`.

---

## 7. API Details

### `POST /predict`
* **Purpose:** Submit user vitals and symptoms to receive a disease prediction.
* **URL:** `http://127.0.0.1:5000/predict`
* **Headers:** `Content-Type: application/json`
* **Request Body (JSON):** 
Expected dynamic keys that represent IoT sensors and symptoms from the dataset. Values for symptoms are binary (1 for present, 0 for missing), and sensor values are floats.
* **Response (JSON):**
```json
{
    "disease": "Predicted Disease Name",
    "description": "Disease description",
    "suggestion": "List of precautions as a string"
}
```

---

## 9. Detailed Code Walkthrough

### A. Frontend (`frontend/main.py`)
This file is the Streamlit web application.
* **Lines 1-5:** Imports for Streamlit, Requests, and Lottie animations.
* **Lines 12-160:** **Splash Screen & Persistence**: Injects a premium full-screen splash animation with JavaScript to handle session-based dismissal.
* **Lines 163-187:** **Apple-Style CSS**: Custom styles for Glassmorphism, metric cards, and Inter typography.
* **Lines 202-209:** **IoT Emulation**: Mock function simulating sensor readings (Temp, HR, SpO2).
* **Lines 237-255:** **Demographics**: Collects Age, Gender, BP, and Cholesterol levels.
* **Lines 298-323:** **Sensor Heuristics**: Sorts 130+ symptoms dynamically to show relevant ones first based on current vitals.
* **Lines 330-354:** **NLP Symptom Extraction**: A text area where users can describe their condition. The code automatically parses the text and checks corresponding symptom boxes.
* **Lines 356-404:** **Paginated Checklist**: Organizes the massive symptom list into manageable pages of 10 items for a cleaner UX.
* **Lines 422-466:** **Inference Logic**: Triggered by "Generate Diagnosis". Converts Fahrenheit to Celsius, bundles the JSON payload, calls the Flask API, and renders the result on a stylized card.

### B. Backend API (`backend/server.py`)
The inference engine and API bridge.
* **Lines 10-33:** **Cold-Start Optimization**: Loads the `.pkl` model and `suggestions.json` once on startup, ensuring sub-100ms response times.
* **Lines 35-43:** **Route Handler**: Listens for POST requests at `/predict`.
* **Lines 44-73:** **Feature Alignment**: Maps incoming JSON keys to the model's expected 0/1 vector. Includes robust case-insensitive matching and categorical encoding for Gender/BP/Cholesterol.
* **Lines 74-84:** **ML Inference**: Passes the vector to the Random Forest model and decodes the numeric prediction back into a disease name.
* **Lines 85-96:** **Response Enrichment**: Matches the disease to a suggestion in the database and returns a complete diagnostic package.

### C. ML Training (`backend/train_model.py`)
The script used to build the intelligence.
* **Data Sources**: Processes the cleaned training CSV.
* **System**: Uses a `RandomForestClassifier` for its ability to handle high-dimensional symptom data without overfitting.
* **Artifacts**: Bundles the `model`, `feature_names`, and `LabelEncoders` into a single `health_model.pkl` for portable deployment.
