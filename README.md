# Health Monitoring & Disease Prediction System (VitalPulse)

## 📌 Table of Contents

1. [Project Overview](#project-overview)
2. [How It Works](#how-it-works)
3. [Technology Stack & Tools Used](#technology-stack--tools-used)
4. [System Architecture](#system-architecture)
5. [Frontend to Backend Connection](#frontend-to-backend-connection)
6. [Machine Learning Model Build Process](#machine-learning-model-build-process)
7. [API Details](#api-details)
8. [Detailed Code Walkthrough](#detailed-code-walkthrough)

---

## 1. Project Overview

**VitalPulse** is a Health Monitoring & Disease Prediction System designed to bridge the gap between real-time physiological data (like temperature, heart rate, and oxygen levels from IoT sensors) and patient-reported symptoms. 

By taking both numeric vitals and qualitative symptoms, the system uses an AI-powered Machine Learning classification model to predict potential diseases and prescribe preliminary precautions or health suggestions to the patient.

---

## 2. How It Works

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

## 8. Detailed Code Walkthrough

### A. Frontend (`frontend/main.py`)
This file is the Streamlit web application.
* **Lines 1-10:** Imports necessary libraries (`streamlit`, `requests`, `json`) and sets the page configuration.
* **Lines 12-37:** Injects custom Apple-style CSS to make the web app look modern (blur effects, fonts, card styling).
* **Lines 52-60:** A mock function `get_sensor_data()` acts as a placeholder for real IoT data fetching.
* **Lines 61-86:** Streamlit UI configuration that sets up 3 visually appealing Metric Cards for generic Temperature, Heart Rate, and SpO2 inputs.
* **Lines 97-151:** Sets up the UI for Demographics (Age, Gender) and lists over 100 possible textual symptoms defined in an `ALL_SYMPTOMS` list.
* **Lines 153-184 `get_prioritized_symptoms()`:** A brilliant UX inclusion. A heuristic function that grabs the current vitals and pushes related symptoms to the front of the list. E.g., if heart rate is >100, it prioritizing showing "palpitations" and "anxiety" checkboxes first.
* **Lines 191-260 (Pagination & Selection):** Handles Streamlit session states to group 130+ symptoms into paginated lists of 10 items per page with Next/Previous buttons so the user isn't overwhelmed. Checkbox selections are dynamically bundled into the payload array.
* **Lines 267-312 (Submission Logic):** Triggers when the user clicks "Generate Diagnosis". It compiles `final_payload` merging Sensors and Symptoms, pushes a `POST` request using `requests`, handles HTTP errors or connection loss, unpacks the response data, and dynamically renders the response on a stylized card.

### B. Backend API (`backend/server.py`)
This file acts as the inference server using Flask.
* **Lines 1-8:** Imports `flask`, `joblib` (for loading the model) and starts the app.
* **Lines 10-34 (Resource Initialization):** Highly optimized. The API loads the large `health_model.pkl` and `suggestions.json` specifically during server startup instead of at response time. This ensures extremely fast (<100ms) prediction times.
* **Line 35 `@app.route('/predict')`:** Maps incoming POST requests.
* **Lines 44-46:** Prepares a completely flat vector/array initialized with zeros (`[0, 0, 0...]`). Its length exactly matches the number of features the machine learning model was trained on.
* **Lines 47-63 (Vector Mapping):** A critical part. The payload dictionary from frontend contains keys that might be randomly ordered or in different cases. The backend loops through the payload, matches keys case-insensitively with the original model's feature names, and flips the index in the flat vector (e.g., changing index 24 from 0 to 1 if "headache" is provided).
* **Lines 64-74 (Prediction & Decoding):** `.predict()` is run on this formatted vector. The output is a number, which the exact same `LabelEncoder` (passed within the `.pkl` file) converts back into the disease text format.
* **Lines 75-87:** Looks alongside the `suggestions.json` database based on the disease, and constructs a completely enriched `jsonify` response containing descriptions and formatted precautions back to the frontend.

### C. ML Training (`backend/train_model.py`)
Creates the intelligence module. 
* **Lines 8-16:** Reads the Kaggle-format `final_train_data.csv` dataset.
* **Lines 18-26:** Scrapes away garbage/empty data rows ("Unnamed: 133"). Splits "Disease" into the target Label (`y`), and everything else into the Features list (`X`).
* **Lines 27-41 (Data Encoding System):** Strings cannot be multiplied in Random Forest logic. Loops over all String (`object`) columns, trains a `LabelEncoder()` specifically for that column to convert strings to deterministic integers, and stores the encoder explicitly into a `label_encoders` dictionary.
* **Lines 42-53:** Splits 80/20. Initializes standard Scikit `RandomForestClassifier`, calls `.fit`, and prints accuracy against the 20% validation chunk.
* **Lines 54-64 (Artifact Export):** Prepares a dictionary named `model_data` consisting of the trained `model`, the exact `features` array, input `encoders`, and output/target `y_encoder`. Running `joblib.dump()` on this bundles all parts into `health_model.pkl` to safely serve the backend.
