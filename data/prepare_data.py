# data/prepare_data.py
import pandas as pd
import numpy as np

def create_hybrid_dataset():
    # 1. Load the Kaggle Dataset
    try:
        # Load the larger dataset for better accuracy
        df = pd.read_csv(r'B:\project\Health_IoT_Project\data\Training.csv')
        
        # Rename 'prognosis' to 'Disease' to match our logic
        if 'prognosis' in df.columns:
            df.rename(columns={'prognosis': 'Disease'}, inplace=True)
            
        print("✅ Raw dataset (Training.csv) loaded successfully.")
    except FileNotFoundError:
        print("❌ Error: 'Training.csv' not found in data/ folder. Please download it first.")
        return

    # 2. Define Logic for Sensors based on Disease
    # We add randomness so the model learns realistic variations
    def get_vitals(row):
        disease = row['Disease']
        
        # DEFAULT VALUES (Healthy-ish)
        temp = np.random.uniform(36.5, 37.2)
        hr = np.random.randint(70, 85)
        spo2 = np.random.randint(96, 100)
        
        # LOGIC: FEVER & INFECTION
        if disease in ['Viral Fever', 'Malaria', 'Typhoid', 'Pneumonia', 'Chicken pox', 'Dengue', 'Tuberculosis']:
            temp = np.random.uniform(38.0, 40.5) # High Fever
            hr = np.random.randint(90, 120)      # Elevated HR
        
        # LOGIC: RESPIRATORY (Low Oxygen)
        if disease in ['Pneumonia', 'Tuberculosis', 'Covid', 'Asthma']:
            spo2 = np.random.randint(88, 94)     # Low SpO2
            if disease == 'Asthma':
                hr = np.random.randint(95, 115)  # Stress HR

        # LOGIC: HEART CONDITIONS
        if disease == 'Heart Attack':
            hr = np.random.randint(110, 150)
            temp = np.random.uniform(35.5, 37.0) # Cold sweat/normal temp
        
        # LOGIC: THYROID
        if disease == 'Hyperthyroidism':
            hr = np.random.randint(100, 130)
        if disease == 'Hypothyroidism':
            hr = np.random.randint(55, 65)

        return pd.Series([temp, hr, spo2])

    # 3. Apply the logic
    print("⚙️  Injecting sensor data...")
    df[['Sensor_Temp', 'Sensor_HR', 'Sensor_SpO2']] = df.apply(get_vitals, axis=1)

    # 4. Save the Final Training Data
    output_path = 'data/final_train_data.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ Hybrid dataset saved to: {output_path}")

if __name__ == "__main__":
    create_hybrid_dataset()