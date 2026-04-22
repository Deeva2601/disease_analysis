"""
MediSense AI — ML Model Training Script
Trains a Random Forest Classifier on the disease-symptom dataset.
Saves the trained model and label encoder as pickle files.
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.multiclass import OneVsRestClassifier

# ── All 132 symptoms (features) ──────────────────────────────────────────────
SYMPTOMS = [
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
    "foul_smell_of_urine", "continuous_feel_of_urine", "passage_of_gases", "internal_itching", "toxic_look_typhos",
    "depression", "irritability", "muscle_pain", "altered_sensorium", "red_spots_over_body",
    "belly_pain", "abnormal_menstruation", "dischromic_patches", "watering_from_eyes", "increased_appetite",
    "polyuria", "family_history", "mucoid_sputum", "rusty_sputum", "lack_of_concentration",
    "visual_disturbances", "receiving_blood_transfusion", "receiving_unsterile_injections", "coma", "stomach_bleeding",
    "distention_of_abdomen", "history_of_alcohol_consumption", "blood_in_sputum", "prominent_veins_on_calf",
    "palpitations", "painful_walking", "pus_filled_pimples", "blackheads", "scurring",
    "skin_peeling", "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails", "blister",
    "red_sore_around_nose", "yellow_crust_ooze"
]

# ── Disease → Symptom Mapping ─────────────────────────────────────────────────
DISEASE_SYMPTOMS = {
    "Fungal infection": ["itching", "skin_rash", "nodal_skin_eruptions", "dischromic_patches"],
    "Allergy": ["continuous_sneezing", "shivering", "chills", "watering_from_eyes", "runny_nose", "throat_irritation"],
    "GERD": ["stomach_pain", "acidity", "ulcers_on_tongue", "vomiting", "cough", "chest_pain", "indigestion"],
    "Chronic cholestasis": ["itching", "vomiting", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite", "abdominal_pain"],
    "Drug Reaction": ["itching", "skin_rash", "stomach_pain", "burning_micturition", "spotting_urination"],
    "Peptic ulcer disease": ["vomiting", "indigestion", "loss_of_appetite", "abdominal_pain", "passage_of_gases", "internal_itching"],
    "AIDS": ["muscle_wasting", "patches_in_throat", "high_fever", "extra_marital_contacts", "fatigue", "weight_loss"],
    "Diabetes": ["fatigue", "weight_loss", "restlessness", "lethargy", "irregular_sugar_level", "blurred_and_distorted_vision",
                 "obesity", "excessive_hunger", "increased_appetite", "polyuria", "lack_of_concentration"],
    "Gastroenteritis": ["vomiting", "sunken_eyes", "dehydration", "diarrhoea"],
    "Bronchial Asthma": ["fatigue", "cough", "high_fever", "breathlessness", "family_history", "mucoid_sputum"],
    "Hypertension": ["headache", "chest_pain", "dizziness", "loss_of_balance", "lack_of_concentration"],
    "Migraine": ["acidity", "indigestion", "headache", "blurred_and_distorted_vision", "excessive_hunger",
                 "stiff_neck", "depression", "irritability", "visual_disturbances"],
    "Cervical spondylosis": ["back_pain", "weakness_in_limbs", "neck_pain", "dizziness", "loss_of_balance"],
    "Paralysis (brain hemorrhage)": ["vomiting", "headache", "weakness_of_one_body_side", "altered_sensorium", "slurred_speech"],
    "Jaundice": ["itching", "vomiting", "fatigue", "weight_loss", "high_fever", "yellowish_skin", "dark_urine",
                 "abdominal_pain", "constipation", "loss_of_appetite", "yellow_urine", "yellowing_of_eyes",
                 "acute_liver_failure", "swelling_of_stomach", "malaise"],
    "Malaria": ["chills", "vomiting", "high_fever", "sweating", "headache", "nausea", "diarrhoea", "muscle_pain"],
    "Chicken pox": ["itching", "skin_rash", "fatigue", "lethargy", "high_fever", "headache", "loss_of_appetite",
                    "mild_fever", "swelled_lymph_nodes", "malaise", "red_spots_over_body", "blister"],
    "Dengue": ["skin_rash", "chills", "joint_pain", "vomiting", "fatigue", "high_fever", "headache", "nausea",
               "loss_of_appetite", "pain_behind_the_eyes", "back_pain", "malaise", "muscle_pain", "red_spots_over_body"],
    "Typhoid": ["chills", "vomiting", "fatigue", "high_fever", "headache", "nausea", "constipation",
                "abdominal_pain", "diarrhoea", "toxic_look_typhos", "belly_pain", "altered_sensorium"],
    "Hepatitis A": ["joint_pain", "vomiting", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite",
                    "abdominal_pain", "diarrhoea", "mild_fever", "yellowing_of_eyes", "muscle_pain"],
    "Hepatitis B": ["itching", "fatigue", "lethargy", "yellowish_skin", "dark_urine", "loss_of_appetite",
                    "abdominal_pain", "yellow_urine", "yellowing_of_eyes", "malaise", "receiving_blood_transfusion",
                    "receiving_unsterile_injections"],
    "Hepatitis C": ["fatigue", "yellowish_skin", "nausea", "loss_of_appetite", "yellowing_of_eyes",
                    "receiving_blood_transfusion", "receiving_unsterile_injections", "family_history"],
    "Hepatitis D": ["joint_pain", "vomiting", "fatigue", "yellowish_skin", "dark_urine", "nausea",
                    "loss_of_appetite", "abdominal_pain", "yellowing_of_eyes"],
    "Hepatitis E": ["joint_pain", "vomiting", "fatigue", "high_fever", "yellowish_skin", "dark_urine",
                    "nausea", "loss_of_appetite", "abdominal_pain", "acute_liver_failure", "coma"],
    "Alcoholic hepatitis": ["vomiting", "yellowish_skin", "abdominal_pain", "swelling_of_stomach",
                            "distention_of_abdomen", "history_of_alcohol_consumption", "fluid_overload"],
    "Tuberculosis": ["chills", "vomiting", "fatigue", "weight_loss", "cough", "high_fever", "breathlessness",
                     "sweating", "loss_of_appetite", "mild_fever", "swelled_lymph_nodes", "malaise",
                     "phlegm", "blood_in_sputum", "mucoid_sputum"],
    "Common Cold": ["continuous_sneezing", "chills", "fatigue", "cough", "headache", "swelled_lymph_nodes",
                    "malaise", "phlegm", "throat_irritation", "redness_of_eyes", "sinus_pressure",
                    "runny_nose", "congestion", "muscle_pain"],
    "Pneumonia": ["chills", "fatigue", "cough", "high_fever", "breathlessness", "sweating", "malaise",
                  "phlegm", "chest_pain", "fast_heart_rate", "rusty_sputum"],
    "Dimorphic hemorrhoids (piles)": ["constipation", "pain_during_bowel_movements", "pain_in_anal_region",
                                       "bloody_stool", "irritation_in_anus"],
    "Heart attack": ["vomiting", "breathlessness", "sweating", "chest_pain", "fast_heart_rate"],
    "Varicose veins": ["fatigue", "cramps", "bruising", "obesity", "swollen_legs", "swollen_blood_vessels",
                       "prominent_veins_on_calf", "painful_walking"],
    "Hypothyroidism": ["fatigue", "weight_gain", "cold_hands_and_feets", "mood_swings", "lethargy",
                       "dizziness", "puffy_face_and_eyes", "enlarged_thyroid", "brittle_nails",
                       "swollen_extremeties", "depression", "irritability", "abnormal_menstruation"],
    "Hyperthyroidism": ["fatigue", "mood_swings", "weight_loss", "restlessness", "sweating", "diarrhoea",
                        "fast_heart_rate", "enlarged_thyroid", "excessive_hunger", "irritability",
                        "abnormal_menstruation", "muscle_weakness"],
    "Hypoglycemia": ["fatigue", "anxiety", "sweating", "headache", "nausea", "blurred_and_distorted_vision",
                     "slurred_speech", "irritability", "excessive_hunger", "drying_and_tingling_lips", "palpitations"],
    "Osteoarthritis": ["joint_pain", "neck_pain", "knee_pain", "hip_joint_pain", "swelling_joints", "painful_walking"],
    "Arthritis": ["muscle_weakness", "stiff_neck", "swelling_joints", "movement_stiffness", "loss_of_balance"],
    "Vertigo": ["vomiting", "headache", "nausea", "spinning_movements", "loss_of_balance", "unsteadiness"],
    "Acne": ["skin_rash", "pus_filled_pimples", "blackheads", "scurring"],
    "Urinary tract infection": ["burning_micturition", "bladder_discomfort", "foul_smell_of_urine",
                                 "continuous_feel_of_urine"],
    "Psoriasis": ["skin_rash", "joint_pain", "itching", "skin_peeling", "silver_like_dusting",
                  "small_dents_in_nails", "inflammatory_nails"],
    "Impetigo": ["skin_rash", "high_fever", "blister", "red_sore_around_nose", "yellow_crust_ooze"]
}


def create_dataset():
    """Generate training dataset from disease-symptom mappings."""
    print("[STATS] Creating training dataset...")
    data = []
    np.random.seed(42)

    samples_per_disease = 120  # enough for robust training

    for disease, symptoms in DISEASE_SYMPTOMS.items():
        for _ in range(samples_per_disease):
            row = {s: 0 for s in SYMPTOMS}
            row["prognosis"] = disease

            # Always include core symptoms
            for sym in symptoms:
                if sym in row:
                    row[sym] = 1

            # Add some random noise — remove 0–2 symptoms occasionally
            num_to_remove = np.random.randint(0, min(3, len(symptoms)))
            remove_syms = np.random.choice(symptoms, num_to_remove, replace=False)
            for sym in remove_syms:
                if sym in row:
                    row[sym] = 0

            data.append(row)

    df = pd.DataFrame(data)
    print(f"[OK] Dataset created: {df.shape[0]} rows x {df.shape[1]} columns")
    return df


def train_model():
    """Train the Random Forest disease prediction model."""
    print("\n[HOSPITAL] MediSense AI -- Model Training")
    print("=" * 50)

    # Create dataset
    df = create_dataset()

    # Save dataset
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/disease_symptoms.csv", index=False)
    print("[OK] Dataset saved to data/disease_symptoms.csv")

    # Prepare features and labels
    X = df.drop("prognosis", axis=1)
    y = df["prognosis"]

    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    print(f"\n[INFO] Diseases to predict: {len(le.classes_)}")
    print(f"[INFO] Features (symptoms): {X.shape[1]}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    # Train Random Forest (PRIMARY MODEL)
    print("\n[MODEL] Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)

    # Evaluate
    y_pred = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"[OK] Random Forest Accuracy: {accuracy * 100:.2f}%")

    # Cross-validation
    cv_scores = cross_val_score(rf_model, X, y_encoded, cv=5)
    print(f"[STATS] Cross-Val Score (5-fold): {cv_scores.mean() * 100:.2f}% ± {cv_scores.std() * 100:.2f}%")

    # Save model and encoder
    os.makedirs("models", exist_ok=True)
    model_data = {
        "model": rf_model,
        "label_encoder": le,
        "feature_names": list(X.columns),
        "disease_names": list(le.classes_),
        "accuracy": accuracy
    }

    with open("models/disease_model.pkl", "wb") as f:
        pickle.dump(model_data, f)

    print("\n[OK] Model saved to models/disease_model.pkl")
    print("\n[DONE] Training complete! MediSense AI is ready.")
    print("=" * 50)
    print("\n[RUN] python app.py  ->  http://localhost:5000")


if __name__ == "__main__":
    train_model()
