# backend/train_model.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train():
    # 1. Load the Hybrid Data
    try:
        data = pd.read_csv('data/final_train_data.csv')
    except FileNotFoundError:
        print("❌ Data not found. Run 'data/prepare_data.py' first.")
        return

    print(f"Loaded {len(data)} rows of data.")

    # 2. Preprocessing
    # Drop columns not needed for training (like empty columns if any)
    # The Kaggle dataset usually has an empty column at the end named "Unnamed: 133"
    if 'Unnamed: 133' in data.columns:
        data = data.drop('Unnamed: 133', axis=1)

    X = data.drop('Disease', axis=1) # Input Features
    y = data['Disease']              # Target Label

    # 3. Encoding Categorical Data
    from sklearn.preprocessing import LabelEncoder
    label_encoders = {}
    X_encoded = X.copy()
    
    for col in X.columns:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X_encoded[col] = le.fit_transform(X[col])
            label_encoders[col] = le
            
    # Encode Target as well if it's not already
    y_encoder = LabelEncoder()
    y_encoded = y_encoder.fit_transform(y)

    # 4. Split
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y_encoded, test_size=0.2, random_state=42)

    # 5. Train
    print("Training Random Forest Model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 6. Evaluate
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Model Trained. Accuracy: {acc*100:.2f}%")

    # 7. Save
    # We save the model AND the encoders to handle future data
    model_data = {
        'model': model,
        'features': list(X.columns),
        'encoders': label_encoders,
        'target_encoder': y_encoder
    }
    joblib.dump(model_data, 'backend/health_model.pkl')
    print("Model saved to 'backend/health_model.pkl'")

if __name__ == "__main__":
    train()