"""
MediSense AI — Disease Knowledge Base
Complete database of 41 diseases with symptoms, treatment costs (INR),
severity ratings, specialist recommendations, and descriptions.
"""

DISEASE_INFO = {
    "Fungal infection": {
        "description": "A skin infection caused by fungi, commonly affecting skin folds, nails, and mucous membranes.",
        "severity": 3,
        "specialist": "Dermatologist",
        "avg_cost_inr": {"min": 500, "max": 3000, "avg": 1500},
        "duration": "2–4 weeks",
        "precautions": ["Keep skin dry and clean", "Avoid sharing personal items", "Use antifungal powder", "Wear breathable clothing"],
        "emoji": "🍄",
        "color": "#f59e0b"
    },
    "Allergy": {
        "description": "An immune system reaction to foreign substances like pollen, pet dander, or certain foods.",
        "severity": 4,
        "specialist": "Allergist / Immunologist",
        "avg_cost_inr": {"min": 1000, "max": 8000, "avg": 4000},
        "duration": "Variable — depends on trigger",
        "precautions": ["Identify and avoid allergens", "Carry antihistamines", "Use air purifiers", "Keep windows closed during pollen season"],
        "emoji": "🤧",
        "color": "#8b5cf6"
    },
    "GERD": {
        "description": "Gastroesophageal Reflux Disease — chronic acid reflux causing heartburn and esophageal irritation.",
        "severity": 5,
        "specialist": "Gastroenterologist",
        "avg_cost_inr": {"min": 2000, "max": 15000, "avg": 7000},
        "duration": "Chronic — lifelong management",
        "precautions": ["Avoid spicy/fatty foods", "Eat smaller meals", "Don't lie down after eating", "Elevate head while sleeping"],
        "emoji": "🔥",
        "color": "#ef4444"
    },
    "Chronic cholestasis": {
        "description": "A liver condition where bile flow is reduced or blocked, causing jaundice and itching.",
        "severity": 7,
        "specialist": "Hepatologist / Gastroenterologist",
        "avg_cost_inr": {"min": 10000, "max": 60000, "avg": 30000},
        "duration": "Chronic — requires ongoing treatment",
        "precautions": ["Avoid alcohol", "Follow low-fat diet", "Regular liver checkups", "Take prescribed bile acid supplements"],
        "emoji": "🫀",
        "color": "#f97316"
    },
    "Drug Reaction": {
        "description": "An adverse immune response to a medication, ranging from mild rash to severe anaphylaxis.",
        "severity": 6,
        "specialist": "Allergist / Emergency Physician",
        "avg_cost_inr": {"min": 2000, "max": 25000, "avg": 10000},
        "duration": "Days to weeks after stopping medication",
        "precautions": ["Stop the suspected drug immediately", "Inform all doctors about drug allergies", "Carry medical alert ID", "Seek emergency care if symptoms worsen"],
        "emoji": "💊",
        "color": "#ec4899"
    },
    "Peptic ulcer disease": {
        "description": "Painful sores in the stomach lining or small intestine, often caused by H. pylori bacteria or NSAIDs.",
        "severity": 6,
        "specialist": "Gastroenterologist",
        "avg_cost_inr": {"min": 3000, "max": 20000, "avg": 10000},
        "duration": "4–8 weeks with treatment",
        "precautions": ["Avoid NSAIDs and aspirin", "Quit smoking", "Limit alcohol", "Eat small frequent meals"],
        "emoji": "🤢",
        "color": "#f59e0b"
    },
    "AIDS": {
        "description": "Advanced stage of HIV infection that severely damages the immune system.",
        "severity": 10,
        "specialist": "Infectious Disease Specialist",
        "avg_cost_inr": {"min": 15000, "max": 100000, "avg": 50000},
        "duration": "Lifelong — managed with ART",
        "precautions": ["Consistent ART medication", "Regular CD4 count monitoring", "Safe sex practices", "Avoid opportunistic infections"],
        "emoji": "🔴",
        "color": "#dc2626"
    },
    "Diabetes": {
        "description": "A metabolic disorder causing high blood sugar levels due to insulin deficiency or resistance.",
        "severity": 7,
        "specialist": "Endocrinologist / Diabetologist",
        "avg_cost_inr": {"min": 5000, "max": 30000, "avg": 15000},
        "duration": "Lifelong management",
        "precautions": ["Monitor blood sugar regularly", "Follow diabetic diet", "Exercise daily", "Take insulin/medication as prescribed"],
        "emoji": "🩸",
        "color": "#0ea5e9"
    },
    "Gastroenteritis": {
        "description": "Inflammation of the stomach and intestines, typically caused by viral or bacterial infection.",
        "severity": 5,
        "specialist": "Gastroenterologist / General Physician",
        "avg_cost_inr": {"min": 1000, "max": 8000, "avg": 4000},
        "duration": "3–7 days",
        "precautions": ["Stay well hydrated (ORS)", "Eat bland foods (BRAT diet)", "Practice good hand hygiene", "Avoid dairy and fatty foods"],
        "emoji": "🤮",
        "color": "#84cc16"
    },
    "Bronchial Asthma": {
        "description": "A chronic respiratory condition causing airway inflammation, wheezing, and breathing difficulty.",
        "severity": 7,
        "specialist": "Pulmonologist",
        "avg_cost_inr": {"min": 3000, "max": 20000, "avg": 8000},
        "duration": "Lifelong — controlled with inhalers",
        "precautions": ["Avoid triggers (dust, smoke, pets)", "Always carry rescue inhaler", "Use air purifiers at home", "Get flu vaccine annually"],
        "emoji": "😮‍💨",
        "color": "#06b6d4"
    },
    "Hypertension": {
        "description": "Persistently elevated blood pressure that increases risk of heart disease and stroke.",
        "severity": 7,
        "specialist": "Cardiologist",
        "avg_cost_inr": {"min": 2000, "max": 15000, "avg": 8000},
        "duration": "Lifelong management",
        "precautions": ["Reduce salt intake", "Exercise regularly", "Manage stress", "Monitor BP daily"],
        "emoji": "❤️‍🔥",
        "color": "#ef4444"
    },
    "Migraine": {
        "description": "A neurological disorder causing severe recurring headaches, often with nausea and sensitivity to light.",
        "severity": 6,
        "specialist": "Neurologist",
        "avg_cost_inr": {"min": 2000, "max": 15000, "avg": 7000},
        "duration": "Episodes last 4–72 hours",
        "precautions": ["Identify and avoid triggers", "Maintain regular sleep schedule", "Stay hydrated", "Manage stress with relaxation techniques"],
        "emoji": "🧠",
        "color": "#7c3aed"
    },
    "Cervical spondylosis": {
        "description": "Age-related wear and tear of spinal disks in the neck causing neck pain and stiffness.",
        "severity": 5,
        "specialist": "Orthopedic Surgeon / Neurologist",
        "avg_cost_inr": {"min": 5000, "max": 40000, "avg": 18000},
        "duration": "Chronic — progressive",
        "precautions": ["Maintain good posture", "Neck exercises daily", "Avoid heavy lifting", "Use ergonomic furniture"],
        "emoji": "🦴",
        "color": "#d97706"
    },
    "Paralysis (brain hemorrhage)": {
        "description": "Loss of muscle function caused by bleeding in the brain, requiring emergency medical care.",
        "severity": 10,
        "specialist": "Neurologist / Neurosurgeon",
        "avg_cost_inr": {"min": 50000, "max": 500000, "avg": 200000},
        "duration": "Weeks to months of rehabilitation",
        "precautions": ["Control blood pressure", "Avoid blood thinners without prescription", "Regular brain scans", "Physical therapy"],
        "emoji": "🚨",
        "color": "#dc2626"
    },
    "Jaundice": {
        "description": "Yellowing of skin and eyes due to excess bilirubin, caused by liver disease or bile duct obstruction.",
        "severity": 7,
        "specialist": "Hepatologist / Gastroenterologist",
        "avg_cost_inr": {"min": 3000, "max": 25000, "avg": 12000},
        "duration": "2–6 weeks depending on cause",
        "precautions": ["Avoid alcohol", "Rest adequately", "Eat light easily digestible food", "Stay hydrated"],
        "emoji": "🟡",
        "color": "#eab308"
    },
    "Malaria": {
        "description": "A mosquito-borne infectious disease causing fever, chills, and flu-like illness.",
        "severity": 8,
        "specialist": "Infectious Disease Specialist",
        "avg_cost_inr": {"min": 2000, "max": 15000, "avg": 6000},
        "duration": "1–4 weeks with treatment",
        "precautions": ["Use mosquito nets and repellents", "Take antimalarial prophylaxis when traveling", "Eliminate standing water", "Wear protective clothing"],
        "emoji": "🦟",
        "color": "#10b981"
    },
    "Chicken pox": {
        "description": "A highly contagious viral infection causing an itchy blister-like rash on the skin.",
        "severity": 5,
        "specialist": "Dermatologist / General Physician",
        "avg_cost_inr": {"min": 1000, "max": 8000, "avg": 3000},
        "duration": "7–14 days",
        "precautions": ["Isolate from others", "Avoid scratching", "Take antiviral medication", "Get vaccinated (prevention)"],
        "emoji": "🔴",
        "color": "#f43f5e"
    },
    "Dengue": {
        "description": "A mosquito-borne viral infection causing high fever, severe joint pain, and rash.",
        "severity": 8,
        "specialist": "Infectious Disease Specialist",
        "avg_cost_inr": {"min": 5000, "max": 30000, "avg": 15000},
        "duration": "7–14 days",
        "precautions": ["Control mosquito breeding", "Use repellents", "Monitor platelet count", "Stay hydrated"],
        "emoji": "🦟",
        "color": "#f97316"
    },
    "Typhoid": {
        "description": "A bacterial infection caused by Salmonella typhi, spread through contaminated food and water.",
        "severity": 7,
        "specialist": "Infectious Disease Specialist",
        "avg_cost_inr": {"min": 3000, "max": 15000, "avg": 7000},
        "duration": "2–4 weeks with treatment",
        "precautions": ["Drink purified water only", "Eat thoroughly cooked food", "Maintain good hand hygiene", "Get typhoid vaccine"],
        "emoji": "🌡️",
        "color": "#ef4444"
    },
    "Hepatitis A": {
        "description": "A viral liver infection transmitted through contaminated food and water.",
        "severity": 6,
        "specialist": "Hepatologist",
        "avg_cost_inr": {"min": 3000, "max": 20000, "avg": 9000},
        "duration": "2–6 months",
        "precautions": ["Maintain hand hygiene", "Consume safe food and water", "Get vaccinated", "Avoid alcohol"],
        "emoji": "🫁",
        "color": "#f59e0b"
    },
    "Hepatitis B": {
        "description": "A serious liver infection caused by HBV virus, spread through blood and bodily fluids.",
        "severity": 8,
        "specialist": "Hepatologist",
        "avg_cost_inr": {"min": 5000, "max": 40000, "avg": 18000},
        "duration": "Chronic — lifelong monitoring",
        "precautions": ["Get vaccinated", "Use protection during sexual contact", "Don't share needles", "Regular liver function tests"],
        "emoji": "🔬",
        "color": "#dc2626"
    },
    "Hepatitis C": {
        "description": "A viral infection causing liver inflammation, potentially leading to serious liver damage.",
        "severity": 8,
        "specialist": "Hepatologist",
        "avg_cost_inr": {"min": 10000, "max": 80000, "avg": 35000},
        "duration": "12–24 weeks of antiviral treatment",
        "precautions": ["Don't share needles", "Avoid tattoo parlors with unsterilized equipment", "Practice safe sex", "Regular monitoring"],
        "emoji": "🧬",
        "color": "#f97316"
    },
    "Hepatitis D": {
        "description": "A liver infection that only occurs in people already infected with Hepatitis B.",
        "severity": 9,
        "specialist": "Hepatologist",
        "avg_cost_inr": {"min": 15000, "max": 100000, "avg": 45000},
        "duration": "Chronic — complex management",
        "precautions": ["Hepatitis B vaccination prevents D", "Avoid sharing blood-contaminated items", "Regular liver biopsies", "Antiviral therapy"],
        "emoji": "⚠️",
        "color": "#dc2626"
    },
    "Hepatitis E": {
        "description": "A waterborne viral liver infection, usually self-limiting but can be severe in pregnant women.",
        "severity": 6,
        "specialist": "Hepatologist / General Physician",
        "avg_cost_inr": {"min": 2000, "max": 15000, "avg": 7000},
        "duration": "4–6 weeks",
        "precautions": ["Drink safe clean water", "Avoid raw shellfish", "Maintain sanitation", "Rest adequately"],
        "emoji": "💧",
        "color": "#0ea5e9"
    },
    "Alcoholic hepatitis": {
        "description": "Liver inflammation caused by excessive alcohol consumption, ranging from mild to life-threatening.",
        "severity": 8,
        "specialist": "Hepatologist / Addiction Medicine Specialist",
        "avg_cost_inr": {"min": 10000, "max": 75000, "avg": 35000},
        "duration": "Weeks to months",
        "precautions": ["Stop alcohol consumption immediately", "Nutritional support", "Regular liver function tests", "Consider rehab program"],
        "emoji": "🍺",
        "color": "#d97706"
    },
    "Tuberculosis": {
        "description": "A serious bacterial infection primarily affecting the lungs, spread through air droplets.",
        "severity": 8,
        "specialist": "Pulmonologist / Infectious Disease Specialist",
        "avg_cost_inr": {"min": 3000, "max": 30000, "avg": 12000},
        "duration": "6–9 months of antibiotic treatment",
        "precautions": ["Complete full course of antibiotics", "Isolate during infectious period", "Wear masks", "Improve ventilation"],
        "emoji": "🫁",
        "color": "#6366f1"
    },
    "Common Cold": {
        "description": "A mild viral respiratory infection affecting the nose and throat, caused by rhinoviruses.",
        "severity": 2,
        "specialist": "General Physician",
        "avg_cost_inr": {"min": 200, "max": 1500, "avg": 800},
        "duration": "7–10 days",
        "precautions": ["Rest and stay hydrated", "Use saline nasal spray", "Avoid contact with infected people", "Maintain hand hygiene"],
        "emoji": "🤧",
        "color": "#6b7280"
    },
    "Pneumonia": {
        "description": "Lung infection causing air sacs to fill with fluid or pus, causing cough, fever, and breathing difficulty.",
        "severity": 8,
        "specialist": "Pulmonologist",
        "avg_cost_inr": {"min": 10000, "max": 80000, "avg": 30000},
        "duration": "2–4 weeks",
        "precautions": ["Complete antibiotic course", "Stay hydrated", "Rest", "Get pneumococcal vaccine"],
        "emoji": "🫁",
        "color": "#06b6d4"
    },
    "Dimorphic hemorrhoids (piles)": {
        "description": "Swollen veins in the rectum or anus causing pain, bleeding, and discomfort during bowel movements.",
        "severity": 5,
        "specialist": "Proctologist / Colorectal Surgeon",
        "avg_cost_inr": {"min": 5000, "max": 50000, "avg": 20000},
        "duration": "Weeks — may require surgery",
        "precautions": ["High fiber diet", "Stay hydrated", "Avoid straining", "Sitz baths"],
        "emoji": "🩺",
        "color": "#f43f5e"
    },
    "Heart attack": {
        "description": "Blockage of blood flow to a part of the heart muscle, requiring immediate emergency care.",
        "severity": 10,
        "specialist": "Cardiologist / Emergency Physician",
        "avg_cost_inr": {"min": 100000, "max": 500000, "avg": 250000},
        "duration": "Emergency — weeks of recovery",
        "precautions": ["Call emergency services immediately", "Chew aspirin if not allergic", "Cardiac rehabilitation", "Lifestyle changes"],
        "emoji": "💔",
        "color": "#dc2626"
    },
    "Varicose veins": {
        "description": "Enlarged, twisted veins usually in the legs due to weakened vein valves.",
        "severity": 4,
        "specialist": "Vascular Surgeon",
        "avg_cost_inr": {"min": 20000, "max": 100000, "avg": 50000},
        "duration": "Days to weeks post-treatment",
        "precautions": ["Elevate legs when resting", "Exercise regularly", "Avoid prolonged standing", "Wear compression stockings"],
        "emoji": "🦵",
        "color": "#8b5cf6"
    },
    "Hypothyroidism": {
        "description": "Underactive thyroid gland producing insufficient hormones, causing fatigue, weight gain, and depression.",
        "severity": 5,
        "specialist": "Endocrinologist",
        "avg_cost_inr": {"min": 2000, "max": 10000, "avg": 5000},
        "duration": "Lifelong hormone replacement",
        "precautions": ["Take thyroxine medication daily", "Regular TSH monitoring", "Eat iodine-rich foods", "Avoid excessive soy products"],
        "emoji": "🦋",
        "color": "#0ea5e9"
    },
    "Hyperthyroidism": {
        "description": "Overactive thyroid producing excess hormones, causing rapid heartbeat, weight loss, and anxiety.",
        "severity": 6,
        "specialist": "Endocrinologist",
        "avg_cost_inr": {"min": 5000, "max": 25000, "avg": 12000},
        "duration": "1–2 years of treatment",
        "precautions": ["Take antithyroid medications", "Avoid excess iodine", "Regular thyroid function tests", "Manage stress"],
        "emoji": "⚡",
        "color": "#f59e0b"
    },
    "Hypoglycemia": {
        "description": "Abnormally low blood sugar levels causing dizziness, confusion, and in severe cases, loss of consciousness.",
        "severity": 6,
        "specialist": "Endocrinologist / Diabetologist",
        "avg_cost_inr": {"min": 1000, "max": 8000, "avg": 4000},
        "duration": "Minutes to hours — acute episodes",
        "precautions": ["Carry fast-acting glucose (juice/candy)", "Eat regular meals", "Monitor blood sugar", "Wear medical alert bracelet"],
        "emoji": "🍬",
        "color": "#ec4899"
    },
    "Osteoarthritis": {
        "description": "Degenerative joint disease causing cartilage breakdown, leading to pain, stiffness, and limited mobility.",
        "severity": 6,
        "specialist": "Orthopedic Surgeon / Rheumatologist",
        "avg_cost_inr": {"min": 5000, "max": 80000, "avg": 25000},
        "duration": "Chronic — progressive",
        "precautions": ["Maintain healthy weight", "Low-impact exercise", "Physical therapy", "Joint supplements (glucosamine)"],
        "emoji": "🦴",
        "color": "#d97706"
    },
    "Arthritis": {
        "description": "Inflammation of one or more joints causing pain and stiffness that worsens with age.",
        "severity": 6,
        "specialist": "Rheumatologist",
        "avg_cost_inr": {"min": 3000, "max": 30000, "avg": 12000},
        "duration": "Chronic — managed with medication",
        "precautions": ["Regular low-impact exercise", "Hot/cold therapy", "Anti-inflammatory diet", "Physical therapy"],
        "emoji": "🤲",
        "color": "#f97316"
    },
    "Vertigo": {
        "description": "Sensation of spinning dizziness, often caused by inner ear problems (BPPV).",
        "severity": 4,
        "specialist": "ENT Specialist / Neurologist",
        "avg_cost_inr": {"min": 2000, "max": 15000, "avg": 7000},
        "duration": "Days to weeks — resolves with treatment",
        "precautions": ["Epley maneuver exercises", "Avoid sudden head movements", "Stay hydrated", "Reduce caffeine and sodium"],
        "emoji": "🌀",
        "color": "#6366f1"
    },
    "Acne": {
        "description": "A skin condition causing pimples, blackheads, and cysts due to clogged hair follicles.",
        "severity": 3,
        "specialist": "Dermatologist",
        "avg_cost_inr": {"min": 500, "max": 5000, "avg": 2000},
        "duration": "Months — variable",
        "precautions": ["Cleanse face twice daily", "Don't pop pimples", "Use non-comedogenic products", "Follow prescribed topical treatment"],
        "emoji": "😣",
        "color": "#f43f5e"
    },
    "Urinary tract infection": {
        "description": "Bacterial infection of any part of the urinary system causing burning, frequent urination, and pelvic pain.",
        "severity": 5,
        "specialist": "Urologist / General Physician",
        "avg_cost_inr": {"min": 1000, "max": 6000, "avg": 3000},
        "duration": "3–7 days with antibiotics",
        "precautions": ["Drink plenty of water", "Urinate after intercourse", "Wipe front to back", "Complete antibiotic course"],
        "emoji": "💧",
        "color": "#f59e0b"
    },
    "Psoriasis": {
        "description": "A chronic autoimmune skin condition causing rapid skin cell buildup, resulting in scaling, redness, and itching.",
        "severity": 5,
        "specialist": "Dermatologist",
        "avg_cost_inr": {"min": 3000, "max": 20000, "avg": 9000},
        "duration": "Chronic — flare and remission cycles",
        "precautions": ["Moisturize regularly", "Avoid triggers (stress, alcohol)", "Use medicated shampoos", "Phototherapy sessions"],
        "emoji": "🩹",
        "color": "#ec4899"
    },
    "Impetigo": {
        "description": "A highly contagious bacterial skin infection causing red sores and yellow-brown crust, common in children.",
        "severity": 4,
        "specialist": "Dermatologist / General Physician",
        "avg_cost_inr": {"min": 500, "max": 4000, "avg": 1500},
        "duration": "7–10 days with antibiotics",
        "precautions": ["Keep sores covered", "Avoid touching or scratching", "Handwashing frequently", "Don't share towels or clothing"],
        "emoji": "🔴",
        "color": "#f97316"
    }
}

# All 132 symptoms for autocomplete
ALL_SYMPTOMS = [
    "itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing", "shivering",
    "chills", "joint_pain", "stomach_pain", "acidity", "ulcers_on_tongue",
    "muscle_wasting", "vomiting", "burning_micturition", "spotting_urination", "fatigue",
    "weight_gain", "anxiety", "cold_hands_and_feets", "mood_swings", "weight_loss",
    "restlessness", "lethargy", "patches_in_throat", "irregular_sugar_level", "cough",
    "high_fever", "sunken_eyes", "breathlessness", "sweating", "dehydration",
    "indigestion", "headache", "yellowish_skin", "dark_urine", "nausea",
    "loss_of_appetite", "pain_behind_the_eyes", "back_pain", "constipation", "abdominal_pain",
    "diarrhoea", "mild_fever", "yellow_urine", "yellowing_of_eyes", "acute_liver_failure",
    "fluid_overload", "swelling_of_stomach", "swelled_lymph_nodes", "malaise", "blurred_and_distorted_vision",
    "phlegm", "throat_irritation", "redness_of_eyes", "sinus_pressure", "runny_nose",
    "congestion", "chest_pain", "weakness_in_limbs", "fast_heart_rate", "pain_during_bowel_movements",
    "pain_in_anal_region", "bloody_stool", "irritation_in_anus", "neck_pain", "dizziness",
    "cramps", "bruising", "obesity", "swollen_legs", "swollen_blood_vessels",
    "puffy_face_and_eyes", "enlarged_thyroid", "brittle_nails", "swollen_extremeties", "excessive_hunger",
    "extra_marital_contacts", "drying_and_tingling_lips", "slurred_speech", "knee_pain", "hip_joint_pain",
    "muscle_weakness", "stiff_neck", "swelling_joints", "movement_stiffness", "spinning_movements",
    "loss_of_balance", "unsteadiness", "weakness_of_one_body_side", "loss_of_smell", "bladder_discomfort",
    "foul_smell_of_urine", "continuous_feel_of_urine", "passage_of_gases", "internal_itching", "toxic_look(typhos)",
    "depression", "irritability", "muscle_pain", "altered_sensorium", "red_spots_over_body",
    "belly_pain", "abnormal_menstruation", "dischromic_patches", "watering_from_eyes", "increased_appetite",
    "polyuria", "family_history", "mucoid_sputum", "rusty_sputum", "lack_of_concentration",
    "visual_disturbances", "receiving_blood_transfusion", "receiving_unsterile_injections", "coma", "stomach_bleeding",
    "distention_of_abdomen", "history_of_alcohol_consumption", "fluid_overload", "blood_in_sputum", "prominent_veins_on_calf",
    "palpitations", "painful_walking", "pus_filled_pimples", "blackheads", "scurring",
    "skin_peeling", "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails", "blister",
    "red_sore_around_nose", "yellow_crust_ooze", "prognosis"
]

def get_symptom_display_name(symptom):
    """Convert symptom key to human-readable display name."""
    return symptom.replace("_", " ").title()

def get_all_symptom_names():
    """Get all symptoms as human-readable names."""
    return [get_symptom_display_name(s) for s in ALL_SYMPTOMS if s != "prognosis"]

def get_disease_info(disease_name):
    """Get complete info for a disease."""
    return DISEASE_INFO.get(disease_name, {
        "description": "A medical condition requiring professional evaluation.",
        "severity": 5,
        "specialist": "General Physician",
        "avg_cost_inr": {"min": 2000, "max": 15000, "avg": 7000},
        "duration": "Variable",
        "precautions": ["Consult a doctor immediately", "Rest well", "Stay hydrated", "Follow prescribed treatment"],
        "emoji": "🏥",
        "color": "#6b7280"
    })
