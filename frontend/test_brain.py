import joblib
import pandas as pd
import numpy as np

def test_the_model():
    print("--- 🩺 STARTING BRAIN TEST ---")

    # 1. Load the Brain (Model)
    try:
        import os
        # Get the directory where this script looks (frontend folder)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to project root, then into backend
        model_path = os.path.join(script_dir, '..', 'backend', 'health_model.pkl')
        
        # We load the dictionary we saved earlier
        model_data = joblib.load(model_path)
        model = model_data['model']
        feature_names = model_data['features'] # These are the columns the model expects
        print("✅ Model loaded successfully!")
        print(f"ℹ️  The model expects {len(feature_names)} inputs (Symptoms + Sensors).")
    except FileNotFoundError:
        print(f"❌ CRITICAL ERROR: Model not found at {model_path}")
        print("   -> Did you run 'python backend/train_model.py' yet?")
        return

    # 2. Create a Fake Patient
    # We create a dictionary with all 0s (no symptoms)
    input_data = {feature: 0 for feature in feature_names}

    # Now we simulate a specific case: High Fever (Malaria-like)
    # We turn ON specific symptoms if they exist in your dataset
    if 'chills' in input_data: input_data['chills'] = 1
    if 'vomiting' in input_data: input_data['vomiting'] = 1
    if 'high_fever' in input_data: input_data['high_fever'] = 1
    
    # We Add Sensor Data (This MUST match the columns we created in prepare_data.py)
    input_data['Sensor_Temp'] = 40.2  # High Fever
    input_data['Sensor_HR'] = 115     # High Heart Rate
    input_data['Sensor_SpO2'] = 98    # Normal Oxygen

    # Convert the dictionary to the list values in the correct order
    # (The model needs a simple list like [0, 1, 0, 40.2, ...])
    patient_values = [input_data[feature] for feature in feature_names]

    # 3. Ask the Brain
    try:
        print("🤔 Asking the model for a diagnosis...")
        prediction = model.predict([patient_values])
        print(f"\n🎉 SUCCESS! The model predicts: \033[1m{prediction[0]}\033[0m")
        print("(If you see a disease name above, your project is WORKING.)")
    except Exception as e:
        print(f"❌ Prediction Error: {e}")

if __name__ == "__main__":
    test_the_model()