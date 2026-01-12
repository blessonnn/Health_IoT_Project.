import pandas as pd
import os

def create_lookup_files():
    # 1. Define the Description Data
    # (Disease -> Description)
    descriptions = {
        "Drug Reaction": "An adverse drug reaction (ADR) is an injury caused by taking medication. ADRs may occur following a single dose or prolonged administration of a drug or result from the combination of two or more drugs.",
        "Malaria": "An infectious disease caused by protozoan parasites from the Plasmodium family that can be transmitted by the bite of the Anopheles mosquito or by a contaminated needle or transfusion. Falciparum malaria is the most deadly type.",
        "Allergy": "An allergy is an immune system response to a foreign substance that's not typically harmful to your body. They can include certain foods, pollen, or pet dander.",
        "Hypothyroidism": "Hypothyroidism, also called underactive thyroid or low thyroid, is a disorder of the endocrine system in which the thyroid gland does not produce enough thyroid hormone.",
        "Psoriasis": "Psoriasis is a common skin disorder that forms thick, red, bumpy patches covered with silvery scales. They can pop up anywhere, but most appear on the scalp, elbows, knees, and lower back.",
        "GERD": "Gastroesophageal reflux disease (GERD) is a digestive disorder that occurs when acidic stomach juices, or food and fluids, back up from the stomach into the esophagus.",
        "Chronic cholestasis": "Chronic cholestasis is a condition where bile flow from the liver is reduced or blocked for a prolonged period.",
        "Hepatitis A": "Hepatitis A is a highly contagious liver infection caused by the hepatitis A virus. The virus is one of several types of hepatitis viruses that cause inflammation and affect your liver's ability to function.",
        "Osteoarthristis": "Osteoarthritis is the most common form of arthritis, affecting millions of people worldwide. It occurs when the protective cartilage that cushions the ends of your bones wears down over time.",
        "(vertigo) Paroymsal  Positional Vertigo": "Benign paroxysmal positional vertigo (BPPV) is one of the most common causes of vertigo — the sudden sensation that you're spinning or that the inside of your head is spinning.",
        "Hypoglycemia": "Hypoglycemia is a condition in which your blood sugar (glucose) level is lower than normal. Glucose is your body's main energy source.",
        "Acne": "Acne is a skin condition that occurs when your hair follicles become plugged with oil and dead skin cells. It causes whiteheads, blackheads or pimples.",
        "Diabetes": "Diabetes is a disease that occurs when your blood glucose, also called blood sugar, is too high. Blood glucose is your main source of energy and comes from the food you eat.",
        "Impetigo": "Impetigo is a common and highly contagious skin infection that mainly affects infants and children. Impetigo usually appears as red sores on the face, especially around a child's nose and mouth, and on hands and feet.",
        "Hypertension": "Hypertension (HTN or HT), also known as high blood pressure (HBP), is a long-term medical condition in which the blood pressure in the arteries is persistently elevated.",
        "Peptic ulcer diseae": "Peptic ulcers are open sores that develop on the inside lining of your stomach and the upper portion of your small intestine. The most common symptom of a peptic ulcer is stomach pain.",
        "Dimorphic hemmorhoids(piles)": "Hemorrhoids, also called piles, are swollen veins in your anus and lower rectum, similar to varicose veins.",
        "Common Cold": "The common cold is a viral infection of your nose and throat (upper respiratory tract). It's usually harmless, although it might not feel that way.",
        "Chicken pox": "Chickenpox is a highly contagious disease caused by the varicella-zoster virus (VZV). It can cause an itchy, blister-like rash. The rash first appears on the chest, back, and face, and then spreads over the entire body.",
        "Cervical spondylosis": "Cervical spondylosis is a general term for age-related wear and tear affecting the spinal disks in your neck. As the disks dehydrate and shrink, signs of osteoarthritis develop, including bony projections along the edges of bones (bone spurs).",
        "Hyperthyroidism": "Hyperthyroidism (overactive thyroid) occurs when your thyroid gland produces too much of the hormone thyroxine. Hyperthyroidism can accelerate your body's metabolism, causing unintentional weight loss and a rapid or irregular heartbeat.",
        "Urinary tract infection": "A urinary tract infection (UTI) is an infection in any part of your urinary system — your kidneys, ureters, bladder and urethra. Most infections involve the lower urinary tract — the bladder and the urethra.",
        "Varicose veins": "Varicose veins are gnarled, enlarged veins. Any vein may become varicose, but the veins most commonly affected are those in your legs and feet.",
        "AIDS": "Acquired immunodeficiency syndrome (AIDS) is a chronic, potentially life-threatening condition caused by the human immunodeficiency virus (HIV). By damaging your immune system, HIV interferes with your body's ability to fight infection and disease.",
        "Paralysis (brain hemorrhage)": "Intracerebral hemorrhage (ICH) is a type of stroke caused by bleeding within the brain tissue itself. A brain hemorrhage can be life-threatening and requires immediate medical attention.",
        "Typhoid": "Typhoid fever is an acute illness associated with fever caused by the Salmonella enterica serotype Typhi bacteria.",
        "Hepatitis B": "Hepatitis B is a serious liver infection caused by the hepatitis B virus (HBV). For some people, hepatitis B infection becomes chronic, meaning it lasts more than six months.",
        "Fungal infection": "A fungal infection, also called mycosis, is a skin disease caused by a fungus. There are millions of species of fungi. They live in the dirt, on plants, on household surfaces, and on your skin.",
        "Hepatitis C": "Hepatitis C is a viral infection that causes liver inflammation, sometimes leading to serious liver damage. The hepatitis C virus (HCV) spreads through contaminated blood.",
        "Migraine": "A migraine is a headache that can cause severe throbbing pain or a pulsing sensation, usually on one side of the head. It's often accompanied by nausea, vomiting, and extreme sensitivity to light and sound.",
        "Bronchial Asthma": "Asthma is a condition in which your airways narrow and swell and may produce extra mucus. This can make breathing difficult and trigger coughing, a whistling sound (wheezing) when you breathe out and shortness of breath.",
        "Alcoholic hepatitis": "Alcoholic hepatitis is inflammation of the liver caused by drinking alcohol. Alcoholic hepatitis is most likely to occur in people who drink heavily over many years.",
        "Jaundice": "Jaundice, a sign of elevated bilirubin levels, is common during the first weeks of life, especially in premature newborns. Bilirubin, a product from the normal breakdown of red blood cells, is elevated in newborns for several reasons.",
        "Hepatitis E": "Hepatitis E is a liver disease caused by the hepatitis E virus (HEV). The virus is shed in the stool of infected persons and enters the human body through the intestine.",
        "Dengue": "Dengue fever is a mosquito-borne tropical disease caused by the dengue virus. Symptoms typically begin three to fourteen days after infection.",
        "Hepatitis D": "Hepatitis D is a liver infection you can get if you have hepatitis B. It can cause serious symptoms that can lead to lifelong liver damage and even death.",
        "Heart Attack": "A heart attack occurs when the flow of blood to the heart is blocked. The blockage is most often a buildup of fat, cholesterol and other substances, which form a plaque in the arteries that feed the heart (coronary arteries).",
        "Pneumonia": "Pneumonia is an infection that inflames the air sacs in one or both lungs. The air sacs may fill with fluid or pus (purulent material), causing cough with phlegm or pus, fever, chills, and difficulty breathing.",
        "Arthritis": "Arthritis is the swelling and tenderness of one or more of your joints. The main symptoms of arthritis are joint pain and stiffness, which typically worsen with age.",
        "Gastroenteritis": "Gastroenteritis is an inflammation of the lining of the intestines caused by a virus, bacteria or parasites. Viral gastroenteritis is the second most common illness in the U.S.",
        "Tuberculosis": "Tuberculosis (TB) is a potentially serious infectious disease that mainly affects your lungs. The bacteria that cause tuberculosis are spread from one person to another through tiny droplets released into the air via coughs and sneezes.",
        "Viral Fever": "Viral fever refers to a wide range of viral infections, characterized by high body temperature and body aches."
    }

    # 2. Define the Precaution Data
    # (Disease -> [Precaution1, Precaution2, Precaution3, Precaution4])
    precautions = {
        "Drug Reaction": ["stop irritation", "consult nearest hospital", "stop taking drug", "follow up"],
        "Malaria": ["Consult Doctor", "Avoid oily food", "keep mosquitos out", "warm water"],
        "Allergy": ["apply calamine", "cover area with bandage", "use ice to compress itching", "take anti-histamines"],
        "Hypothyroidism": ["reduce stress", "exercise", "eat healthy", "get proper sleep"],
        "Psoriasis": ["wash hands with warm soapy water", "stop bleeding using pressure", "consult doctor", "salt baths"],
        "GERD": ["avoid fatty spicy food", "avoid lying down after eating", "maintain healthy weight", "exercise"],
        "Chronic cholestasis": ["cold baths", "anti itch medicine", "consult doctor", "eat healthy"],
        "Hepatitis A": ["Consult Doctor", "wash hands throughly", "avoid fatty spicy food", "medication"],
        "Osteoarthristis": ["acetaminophen", "consult doctor", "follow up", "salt baths"],
        "(vertigo) Paroymsal  Positional Vertigo": ["lie down", "avoid sudden change in body", "avoid abrupt head movment", "relax"],
        "Hypoglycemia": ["lie down on side", "check in pulse", "drink sugary drinks", "consult doctor"],
        "Acne": ["bath twice", "avoid fatty spicy food", "drink plenty of water", "avoid too many products"],
        "Diabetes": ["have balanced diet", "exercise", "consult doctor", "follow up"],
        "Impetigo": ["soak affected area in warm water", "use antibiotics", "remove scabs with wet compressed cloth", "consult doctor"],
        "Hypertension": ["meditation", "salt baths", "reduce stress", "get proper sleep"],
        "Peptic ulcer diseae": ["avoid fatty spicy food", "consume probiotic food", "eliminate milk", "limit alcohol"],
        "Dimorphic hemmorhoids(piles)": ["avoid fatty spicy food", "consume witch hazel", "warm bath with epsom salt", "consume alovera juice"],
        "Common Cold": ["drink vitamin c rich drinks", "take vapour", "avoid cold food", "keep fever in check"],
        "Chicken pox": ["use neem in bathing", "consume neem leaves", "take vaccine", "avoid public places"],
        "Cervical spondylosis": ["use heating pad or cold pack", "exercise", "take otc pain reliver", "consult doctor"],
        "Hyperthyroidism": ["eat healthy", "massage", "use lemon balm", "take radioactive iodine treatment"],
        "Urinary tract infection": ["drink plenty of water", "increase vitamin c intake", "drink cranberry juice", "take probiotics"],
        "Varicose veins": ["lie down flat and raise the leg high", "use oinments", "use vein compression", "dont stand still for long"],
        "AIDS": ["avoid open cuts", "wear ppe if possible", "consult doctor", "follow up"],
        "Paralysis (brain hemorrhage)": ["massage", "eat healthy", "exercise", "consult doctor"],
        "Typhoid": ["eat high calorie vegitables", "antiboitic therapy", "consult doctor", "medication"],
        "Hepatitis B": ["consult nearest hospital", "vaccination", "eat healthy", "medication"],
        "Fungal infection": ["bath twice", "use detol or neem in bathing water", "keep infected area dry", "use clean cloths"],
        "Hepatitis C": ["Consult Doctor", "vaccination", "eat healthy", "medication"],
        "Migraine": ["meditation", "reduce stress", "use poloroid glasses in sun", "consult doctor"],
        "Bronchial Asthma": ["switch to loose cloothing", "take deep breaths", "get away from trigger", "seek help"],
        "Alcoholic hepatitis": ["stop alcohol consumption", "consult doctor", "medication", "follow up"],
        "Jaundice": ["drink plenty of water", "consume milk thistle", "eat fruits and high fiberous food", "medication"],
        "Hepatitis E": ["stop alcohol consumption", "rest", "consult doctor", "medication"],
        "Dengue": ["drink papaya leaf juice", "avoid fatty spicy food", "keep mosquitos out", "keep hydrated"],
        "Hepatitis D": ["consult doctor", "medication", "eat healthy", "follow up"],
        "Heart Attack": ["call ambulance", "chew aspirin", "keep calm", "wait for help"],
        "Pneumonia": ["consult doctor", "medication", "rest", "follow up"],
        "Arthritis": ["exercise", "use hot and cold therapy", "try acupuncture", "massage"],
        "Gastroenteritis": ["stop eating solid food for while", "try sip of water", "rest", "ease back into eating"],
        "Tuberculosis": ["cover mouth", "consult doctor", "medication", "rest"],
        "Viral Fever": ["rest", "drink plenty of fluids", "take fever medication", "consult doctor"]
    }

    # 3. Create DataFrames
    df_desc = pd.DataFrame(list(descriptions.items()), columns=['Disease', 'Description'])
    
    # Precaution is tricky because it has 4 columns. We convert the list to columns.
    prec_data = []
    for disease, precs in precautions.items():
        row = [disease] + precs
        # Pad with None if fewer than 4 precautions (just in case)
        while len(row) < 5:
            row.append(None)
        prec_data.append(row)
    
    df_prec = pd.DataFrame(prec_data, columns=['Disease', 'Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4'])

    # 4. Save to CSV
    if not os.path.exists('data'):
        os.makedirs('data')
        
    df_desc.to_csv('data/symptom_Description.csv', index=False)
    df_prec.to_csv('data/symptom_precaution.csv', index=False)
    
    print("✅ Created 'data/symptom_Description.csv'")
    print("✅ Created 'data/symptom_precaution.csv'")

if __name__ == "__main__":
    create_lookup_files()