import pandas as pd
import json
import os

def build_suggestions_file():
    print("--- 🔨 BUILDING SUGGESTIONS DATABASE ---")

    # 1. Load the CSV files
    # We use 'try' to make sure the files actually exist
    try:
        desc_df = pd.read_csv('data/symptom_Description.csv')
        prec_df = pd.read_csv('data/symptom_precaution.csv')
        print("✅ CSV files loaded successfully.")
    except FileNotFoundError:
        print("❌ CRITICAL ERROR: Could not find the CSV files.")
        print("   -> Did you run 'python data/generate_missing_files.py'?")
        return

    # 2. Initialize the Dictionary
    # This will look like: { "Malaria": { "description": "...", "precautions": [...] } }
    suggestions_db = {}

    # Get a master list of all diseases from both files to be safe
    all_diseases = set(desc_df['Disease']).union(set(prec_df['Disease']))

    print(f"⚙️  Processing {len(all_diseases)} diseases...")

    for disease in all_diseases:
        # Create a default entry
        entry = {
            "description": "No description available for this condition.",
            "precautions": ["Consult a doctor immediately."]
        }
        
        # A. Find Description
        # We look for the row where 'Disease' matches the current loop variable
        d_row = desc_df[desc_df['Disease'] == disease]
        if not d_row.empty:
            # Grab the text from the 'Description' column
            entry["description"] = d_row.iloc[0]['Description']

        # B. Find Precautions
        # The CSV has columns: Precaution_1, Precaution_2, Precaution_3, Precaution_4
        p_row = prec_df[prec_df['Disease'] == disease]
        if not p_row.empty:
            # We select columns 1 to 5 (ignoring the 'Disease' column at index 0)
            # dropna() removes empty cells if a disease only has 2 precautions
            actions = p_row.iloc[0, 1:].dropna().tolist()
            
            # Clean the text (capitalize first letter, strip spaces)
            clean_actions = [str(act).strip().capitalize() for act in actions if str(act).strip() != ""]
            
            if clean_actions:
                entry["precautions"] = clean_actions

        # Save to our master dictionary
        suggestions_db[disease] = entry

    # 3. Save as JSON for the Backend
    # We save it in the 'backend' folder so your Django app can find it easily
    output_dir = 'backend'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, 'suggestions.json')
    
    with open(output_path, 'w') as f:
        json.dump(suggestions_db, f, indent=4)
    
    print(f"✅ SUCCESS! Database saved to: {output_path}")
    print("   (You can now run 'python backend/train_model.py')")

if __name__ == "__main__":
    build_suggestions_file()