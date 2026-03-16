# data/prepare_data.py
import pandas as pd
import numpy as np

def create_hybrid_dataset():
    # 1. Load the Kaggle Dataset
    try:
        # Load the larger dataset for better accuracy
        df = pd.read_csv('data/Training.csv')
        
        # Rename 'prognosis' to 'Disease' to match our logic
        if 'prognosis' in df.columns:
            df.rename(columns={'prognosis': 'Disease'}, inplace=True)
            
        print("✅ Raw dataset (Training.csv) loaded successfully.")
    except FileNotFoundError:
        print("❌ Error: 'Training.csv' not found in data/ folder. Please download it first.")
        return

    # 2. Define Logic for Sensors and Demographics based on Disease
    # We add randomness so the model learns realistic variations
    def get_patient_profile(row):
        disease = row['Disease'].strip()
        
        # --- DEFAULT VALUES ---
        temp = np.random.uniform(36.5, 37.2)
        hr = np.random.randint(70, 85)
        spo2 = np.random.randint(96, 100)
        
        # New Demographics
        age = np.random.randint(18, 70)
        gender = np.random.choice(['Male', 'Female'])
        bp = np.random.choice(['Normal', 'High', 'Low'], p=[0.7, 0.2, 0.1])
        chol = np.random.choice(['Normal', 'High'], p=[0.8, 0.2])

        # --- LOGIC: FEVER & INFECTION ---
        if disease in ['Viral Fever', 'Malaria', 'Typhoid', 'Pneumonia', 'Chicken pox', 'Dengue', 'Tuberculosis', 'Common Cold']:
            temp = np.random.uniform(38.0, 40.5) # High Fever
            hr = np.random.randint(90, 120)      # Elevated HR
        
        # --- LOGIC: RESPIRATORY ---
        if disease in ['Pneumonia', 'Tuberculosis', 'Bronchial Asthma']:
            spo2 = np.random.randint(88, 94)     # Low SpO2
            if disease == 'Bronchial Asthma':
                hr = np.random.randint(95, 115)  # Stress HR

        # --- LOGIC: HEART & VASCULAR ---
        if disease == 'Heart attack':
            hr = np.random.randint(110, 150)
            temp = np.random.uniform(35.5, 37.0)
            age = np.random.randint(45, 85)      # Older age affinity
            bp = 'High'
            chol = 'High'
        
        if disease == 'Hypertension ':
            bp = 'High'
            age = np.random.randint(40, 80)

        # --- LOGIC: THYROID ---
        if disease == 'Hyperthyroidism':
            hr = np.random.randint(100, 130)
            gender = 'Female' # More common in females
        if disease == 'Hypothyroidism':
            hr = np.random.randint(55, 65)
            gender = 'Female'

        # --- LOGIC: DIABETES ---
        if disease == 'Diabetes ':
            age = np.random.randint(35, 80)
            chol = np.random.choice(['Normal', 'High'], p=[0.4, 0.6])

        return pd.Series([temp, hr, spo2, age, gender, bp, chol])

    # 3. Apply the logic
    print("⚙️  Injecting sensor and demographic data...")
    new_cols = ['Sensor_Temp', 'Sensor_HR', 'Sensor_SpO2', 'Age', 'Gender', 'Blood Pressure', 'Cholesterol Level']
    df[new_cols] = df.apply(get_patient_profile, axis=1)

    # 4. Save the Final Training Data
    output_path = 'data/final_train_data.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ Hybrid dataset saved with demographics to: {output_path}")

if __name__ == "__main__":
    create_hybrid_dataset()