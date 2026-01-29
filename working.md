1. High-Level Architecture
The project is a Health Monitoring & Disease Prediction System composed of three main layers:

Frontend (User Interface): A Streamlit web application that acts as the patient portal. It visualizes real-time "IoT Sensor Data" and collects patient symptoms.
Backend (API): A Flask REST API that serves as the inference engine. It receives patient data, communicates with the ML model, and returns predictions.
Machine Learning Core: A Random Forest Classifier trained on a disease-symptom dataset. It powers the diagnostic capabilities of the system.
(Note: There is also a Django project structure in backend/backend, but it appears to be an inactive/skeleton framework for future expansion like User Management or Database logging. The active system currently runs entirely on the Streamlit + Flask flow.)

2. Component Breakdown
A. Frontend (frontend/main.py)
Technology: Streamlit (Python-based web UI framework).
Role: Client-facing interface.
Key Functions:
IoT Simulation (get_sensor_data): currently mocks standard IoT sensor readings:
Temperature (e.g., 99.1°F)
Heart Rate (e.g., 92 BPM)
SpO2 (Oxygen Saturation, e.g., 96%)
In a real deployment, this function would make an HTTP GET request to an ESP32 or Arduino web server to fetch real-time values.
Dynamic Symptom Prioritization:
It uses a heuristic function get_prioritized_symptoms to re-order the symptom checklist.
Example: If 'Temperature' > 99°F, it pushes fever-related symptoms (chills, shivering) to the top of the list for better UX.
API Integration:
It constructs a JSON payload containing both Sensor Data and Selected Symptoms.
Ideally sends a POST request to http://127.0.0.1:5000/predict.
B. Backend API (backend/server.py)
Technology: Flask (Micro-framework).
Role: Inference Server & API Gateway.
Key Functions:
Model Loading: On startup, it loads the pre-trained health_model.pkl (via joblib) and suggestions.json into memory. This ensures low-latency predictions since the model doesn't need to be re-loaded for every request.
Endpoint /predict:
Accepts JSON data.
Data Transformation: It maps the incoming raw JSON keys (e.g., "headache": 1) to the specific feature vector required by the Random Forest model. It handles case-insensitivity to ensure robustness.
Prediction: Runs model.predict() on the processed vector.
Post-Processing: Decodes the output class index (e.g., 0) back to a readable string (e.g., "Flu") using the saved target_encoder.
Enrichment: Fetches precautions/suggestions from suggestions.json based on the predicted disease.
C. Machine Learning Core (backend/train_model.py & health_model.pkl)
Technology: Scikit-Learn (Random Forest Classifier).
Role: The "Brain" of the system.
Workflow:
Data Loading: Reads data/final_train_data.csv.
Preprocessing: Encodes categorical variables (text inputs like "High Blood Pressure" -> 1) using LabelEncoder.
Training: Fits a Random Forest (an ensemble of decision trees) which is highly effective for classification tasks with many features (symptoms).
Serialization: Saves the trained model plus the encoders into health_model.pkl. This is crucial because the API needs the exact same encoders to process new data correctly.

3. Data Flow (The "Lifecycle" of a Request)
User Action: The user opens the web app. The app automatically fetches "Sensor Data".
Input: Users check specific symptoms (e.g., "Fatigue").
Transmission: The Frontend sends a payload:

    {
  "Sensor_Temp": 99.1,
  "Sensor_HR": 92,
  "fatigue": 1,
  "Age": 30,
  ...
    }

Processing: The Flask Backend converts this into a numeric array array [0, 1, 0, ... 99.1, ...] of size N (where N is total features).
Inference: The Array is passed through the Random Forest trees.
Response: The Backend returns:

    {
  "disease": "Typhoid",
  "suggestion": "Consult a doctor, Avoid oily food..."
    }

Display: The Frontend renders a "Metric Card" with the result and suggestions.

This architecture decouples the UI from the logic, allowing you to easily swap the frontend (e.g., to a Mobile App) without changing the core backend logic.