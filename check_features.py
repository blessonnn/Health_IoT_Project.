import joblib
import os

try:
    model_data = joblib.load('backend/health_model.pkl')
    for f in model_data['features']:
        print(f)
except Exception as e:
    print(e)
