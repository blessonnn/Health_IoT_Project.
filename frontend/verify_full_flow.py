import joblib
import json
import os

def test_full_system():
    print("--- 🏥 FULL SYSTEM DIAGNOSTIC ---")

    # 1. Load the Model
    try:
        model_data = joblib.load('backend/health_model.pkl')
        model = model_data['model']
        feature_names = model_data['features']
        print("✅ Model loaded.")
    except Exception as e:
        print(f"❌ Model Error: {e}")
        return

    # 2. Load the Suggestions Database
    try:
        with open('backend/suggestions.json', 'r') as f:
            suggestions_db = json.load(f)
        print("✅ Suggestions Database loaded.")
    except Exception as e:
        print(f"❌ Database Error: {e}")
        return

    # 3. Simulate a Patient (High Fever + Chills = Malaria)
    print("\n🧪 Simulating Patient Data (Fever + Chills)...")
    
    # Create empty input
    input_values = [0] * len(feature_names)
    
    # Find indices for specific symptoms to turn them 'ON'
    # (We wrap in try/except in case column names differ slightly)
    try:
        if 'chills' in feature_names:
            idx = feature_names.index('chills')
            input_values[idx] = 1
        if 'high_fever' in feature_names:
            idx = feature_names.index('high_fever')
            input_values[idx] = 1
        if 'sweating' in feature_names:
            idx = feature_names.index('sweating')
            input_values[idx] = 1
            
        # Add IoT Sensor Data (Last 3 columns)
        # We manually set the last 3 values of the list
        input_values[-3] = 40.5  # Temp (High)
        input_values[-2] = 105   # HR (High)
        input_values[-1] = 96    # SpO2 (Normal)
        
    except Exception as e:
        print(f"⚠️ Warning during symptom mapping: {e}")

    # Load Target Encoder
    target_encoder = model_data.get('target_encoder')
    
    # 4. Predict
    prediction_idx = model.predict([input_values])[0]
    
    # DECISION: Decode the prediction if an encoder exists
    if target_encoder:
        prediction = target_encoder.inverse_transform([prediction_idx])[0]
    else:
        prediction = prediction_idx
        
    print(f"🧠 Model Prediction: {prediction}")

    # 5. Retrieve Suggestions
    # This is the critical step: Does the prediction key exist in the JSON?
    if prediction in suggestions_db:
        info = suggestions_db[prediction]
        print("\n--- 📄 FINAL REPORT GENERATED ---")
        print(f"DISEASE: {prediction}")
        print(f"DESCRIPTION: {info['description']}")
        print(f"PRECAUTIONS: {info['precautions']}")
        print("---------------------------------")
        print("\n✅ TEST PASSED: System is ready for Django integration.")
    else:
        print(f"\n❌ TEST FAILED: Model predicted '{prediction}', but it is NOT in suggestions.json.")
        print("   -> Check spelling in your CSV files.")

if __name__ == "__main__":
    test_full_system()