import flask
from flask import request, jsonify
import joblib
import numpy as np
import json
import os

app = flask.Flask(__name__)

# --- GLOBAL STORE FOR LATEST SENSOR DATA ---
latest_sensors = {
    "Sensor_Temp": 37.0,
    "Sensor_HR": 75,
    "Sensor_SpO2": 98
}

def update_sensor_cache(data):
    """Helper to update the global cache whenever sensor keys are seen."""
    global latest_sensors
    updated = False
    if data:
        print(f"🔥 [RAW DATA RECEIVED]: {data}")
        for key in ["Sensor_Temp", "Sensor_HR", "Sensor_SpO2"]:
            if key in data:
                try:
                    latest_sensors[key] = float(data[key])
                    updated = True
                except: pass
    if updated:
        print(f"✅ [CACHE SYNCED]: {latest_sensors}")


# --- LOAD RESOURCES ON STARTUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'health_model.pkl')
SUGGESTIONS_PATH = os.path.join(BASE_DIR, 'suggestions.json')

print("Loading Model...")
try:
    model_data = joblib.load(MODEL_PATH)
    model = model_data['model']
    feature_names = model_data['features']
    target_encoder = model_data.get('target_encoder')
    print("Model Loaded.")
except Exception as e:
    print(f"Failed to load model: {e}")
    model = None

print("Loading Suggestions...")
try:
    with open(SUGGESTIONS_PATH, 'r') as f:
        suggestions_db = json.load(f)
    print("✅ Suggestions Database Loaded.")
except Exception as e:
    print(f"Failed to load suggestions: {e}")
    suggestions_db = {}

@app.route('/sensors', methods=['POST', 'GET'])
def sensors():
    if request.method == 'POST':
        # Try to get JSON first, if not, try form data
        data = request.get_json(silent=True)
        if not data:
            data = request.form.to_dict()
        
        if data:
            update_sensor_cache(data)
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "No data received"}), 400
    else:
        # GET request: return ONLY the latest values
        # We do NOT touch request.json here to avoid 415 errors
        return jsonify(latest_sensors), 200

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        # Use get_json(silent=True) to be safer
        data = request.get_json(silent=True) or {}
        # Catch sensor data here too!
        update_sensor_cache(data)
        
        print(f"Received Prediction Request: {data}")

        # 1. Prepare Input Vector (all zeros initially)
        input_vector = [0] * len(feature_names)

        # 2. Map Payload to Features
        feature_map = {name.lower(): i for i, name in enumerate(feature_names)}
        encoders = model_data.get('encoders', {})
        # Create a lowercase map for encoders too
        encoder_map = {k.lower(): v for k, v in encoders.items()}

        for key, value in data.items():
            key_lower = key.lower()
            if key_lower in feature_map:
                idx = feature_map[key_lower]
                
                # Check if we have an encoder for this column
                if key_lower in encoder_map:
                    try:
                        # Value should be a string (e.g., 'Male', 'High')
                        encoded_val = encoder_map[key_lower].transform([str(value)])[0]
                        input_vector[idx] = float(encoded_val)
                    except Exception as e:
                        print(f"Encoding error for {key}: {e}")
                        input_vector[idx] = 0.0
                else:
                    # For sensors and symptoms, value is float or int
                    input_vector[idx] = float(value)
            else:
                if key != "Outcome Variable":
                    print(f"Warning: input '{key}' not found in model features.")

        # 3. Predict
        prediction_idx = model.predict([input_vector])[0]
        
        # 4. Decode
        if target_encoder:
            disease = target_encoder.inverse_transform([prediction_idx])[0]
        else:
            disease = str(prediction_idx)

        print(f"Predicted: {disease}")

        # 5. Get Suggestions
        suggestion_info = suggestions_db.get(disease, {
            "description": "Unknown condition.",
            "precautions": ["Consult a doctor."]
        })
        
        # 6. Return Response
        return jsonify({
            "disease": disease,
            "description": suggestion_info.get("description", ""),
            "suggestion": ", ".join(suggestion_info.get("precautions", []))
        })

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    print("Server starting on port 5000...")
    # The 'use_reloader=False' stops the infinite restart loop!
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
