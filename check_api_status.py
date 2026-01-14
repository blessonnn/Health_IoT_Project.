import requests
import json
import time

url = "http://127.0.0.1:5000/predict"
# Payload matching the updated frontend logic
payload = {
    "Fever": 1,
    "Cough": 0,
    "Fatigue": 1,
    "Difficulty Breathing": 0,
    "Age": 30,
    "Gender": 1,
    "Blood Pressure": 0,
    "Cholesterol Level": 0,
    "Outcome Variable": 0,
    "Sensor_Temp": 99.5,
    "Sensor_HR": 80,
    "Sensor_SpO2": 98
}

print("Attempting to connect to", url)
for i in range(5):
    try:
        response = requests.post(url, json=payload)
        print("Status Code:", response.status_code)
        print("Response:", response.json())
        if response.status_code == 200:
            print("✅ API is working!")
            break
    except Exception as e:
        print(f"Attempt {i+1}: Failed to connect ({e})")
        time.sleep(2)
