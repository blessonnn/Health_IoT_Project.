import joblib
import os

BASE_DIR = r"d:\project\Health_IoT_Project\backend"
MODEL_PATH = os.path.join(BASE_DIR, 'health_model.pkl')

try:
    model_data = joblib.load(MODEL_PATH)
    features = model_data['features']
    
    sensor_features = [f for f in features if 'sensor' in f.lower()]
    # Print one by one to avoid truncation
    print("SENSOR_FEATURES_START")
    for s in sensor_features:
        print(f"SENSOR: {s}")
    print("SENSOR_FEATURES_END")

except Exception as e:
    print(f"ERROR: {e}")
