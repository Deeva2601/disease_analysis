"""
MediSense AI — Flask Application Server
REST API for disease prediction + chatbot conversation handler.
"""

from flask import Flask, request, jsonify, render_template, session
import pickle
import os
import json
import re
from datetime import datetime
from disease_data import DISEASE_INFO, get_disease_info, ALL_SYMPTOMS, get_symptom_display_name

app = Flask(__name__)
app.secret_key = "medisense_ai_secret_2024"

# ── Load trained model ────────────────────────────────────────────────────────
MODEL_PATH = "models/disease_model.pkl"
model_data = None

def load_model():
    global model_data
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            model_data = pickle.load(f)
        print(f"[OK] Model loaded | Accuracy: {model_data['accuracy']*100:.1f}%")
    else:
        print("[WARN] Model not found! Run: python train_model.py")

load_model()

# ── Symptom matching helpers ──────────────────────────────────────────────────
SYMPTOM_ALIASES = {
    "fever": ["high_fever", "mild_fever"],
    "temperature": ["high_fever", "mild_fever"],
    "headache": ["headache"],
    "head pain": ["headache"],
    "cough": ["cough", "phlegm", "mucoid_sputum"],
    "cold": ["continuous_sneezing", "runny_nose", "congestion"],
    "running nose": ["runny_nose"],
    "runny nose": ["runny_nose"],
    "itch": ["itching"],
    "itching": ["itching"],
    "rash": ["skin_rash"],
    "vomit": ["vomiting"],
    "vomiting": ["vomiting"],
    "nausea": ["nausea"],
    "fatigue": ["fatigue", "lethargy", "malaise"],
    "tired": ["fatigue", "lethargy"],
    "weakness": ["muscle_weakness", "weakness_in_limbs"],
    "dizziness": ["dizziness", "spinning_movements"],
    "dizzy": ["dizziness"],
    "chest pain": ["chest_pain"],
    "breathless": ["breathlessness"],
    "breathing difficulty": ["breathlessness"],
    "difficulty breathing": ["breathlessness"],
    "stomach pain": ["stomach_pain", "abdominal_pain", "belly_pain"],
    "belly pain": ["belly_pain", "abdominal_pain"],
    "abdominal pain": ["abdominal_pain"],
    "diarrhea": ["diarrhoea"],
    "diarrhoea": ["diarrhoea"],
    "loose motion": ["diarrhoea"],
    "constipation": ["constipation"],
    "back pain": ["back_pain"],
    "neck pain": ["neck_pain"],
    "joint pain": ["joint_pain"],
    "knee pain": ["knee_pain"],
    "sweating": ["sweating"],
    "sweat": ["sweating"],
    "chills": ["chills", "shivering"],
    "shivering": ["shivering"],
    "yellow skin": ["yellowish_skin", "yellowing_of_eyes"],
    "jaundice": ["yellowish_skin", "yellowing_of_eyes", "dark_urine"],
    "dark urine": ["dark_urine"],
    "blood in urine": ["burning_micturition"],
    "burning urination": ["burning_micturition"],
    "frequent urination": ["continuous_feel_of_urine", "polyuria"],
    "acne": ["pus_filled_pimples", "blackheads", "skin_rash"],
    "pimple": ["pus_filled_pimples"],
    "anxiety": ["anxiety", "restlessness"],
    "depression": ["depression"],
    "weight loss": ["weight_loss"],
    "weight gain": ["weight_gain"],
    "swollen": ["swelled_lymph_nodes", "swelling_joints", "swollen_legs"],
    "loss of appetite": ["loss_of_appetite"],
    "no appetite": ["loss_of_appetite"],
    "not eating": ["loss_of_appetite"],
    "muscle pain": ["muscle_pain"],
    "body ache": ["muscle_pain", "joint_pain"],
    "sore throat": ["throat_irritation", "patches_in_throat"],
    "throat pain": ["throat_irritation"],
    "eye pain": ["redness_of_eyes", "pain_behind_the_eyes"],
    "red eyes": ["redness_of_eyes"],
    "blurred vision": ["blurred_and_distorted_vision"],
    "sneezing": ["continuous_sneezing"],
    "congestion": ["congestion", "sinus_pressure"],
    "heart racing": ["fast_heart_rate", "palpitations"],
    "palpitation": ["palpitations"],
    "skin peeling": ["skin_peeling"],
    "bloating": ["passage_of_gases", "distention_of_abdomen"],
    "gas": ["passage_of_gases"],
    "indigestion": ["indigestion", "acidity"],
    "acid reflux": ["acidity", "indigestion"],
    "heartburn": ["acidity", "chest_pain"],
    "ulcer": ["ulcers_on_tongue"],
}

def extract_symptoms_from_text(text):
    """Extract symptoms from free-form user text."""
    text_lower = text.lower()
    found_symptoms = set()

    # Check aliases first (longer phrases first to avoid partial matches)
    aliases_sorted = sorted(SYMPTOM_ALIASES.items(), key=lambda x: len(x[0]), reverse=True)
    for alias, syms in aliases_sorted:
        if alias in text_lower:
            for sym in syms:
                if sym in ALL_SYMPTOMS:
                    found_symptoms.add(sym)

    # Direct symptom name matches
    for symptom in ALL_SYMPTOMS:
        symptom_readable = symptom.replace("_", " ")
        if symptom_readable in text_lower or symptom in text_lower:
            found_symptoms.add(symptom)

    return list(found_symptoms)


def predict_diseases(symptom_list):
    """Predict top-3 diseases from a list of symptom strings."""
    if model_data is None:
        return None

    model = model_data["model"]
    le = model_data["label_encoder"]
    feature_names = model_data["feature_names"]

    # Create feature vector
    feature_vector = [0] * len(feature_names)
    matched = []
    for sym in symptom_list:
        sym_clean = sym.strip().lower().replace(" ", "_")
        if sym_clean in feature_names:
            idx = feature_names.index(sym_clean)
            feature_vector[idx] = 1
            matched.append(sym_clean)

    if not any(feature_vector):
        return None

    # Get probabilities
    proba = model.predict_proba([feature_vector])[0]
    top3_idx = proba.argsort()[-3:][::-1]

    results = []
    for idx in top3_idx:
        disease_name = le.classes_[idx]
        confidence = round(proba[idx] * 100, 1)
        if confidence > 0.5:
            info = get_disease_info(disease_name)
            results.append({
                "disease": disease_name,
                "confidence": confidence,
                "info": info,
                "emoji": info.get("emoji", "🏥"),
                "severity": info.get("severity", 5),
                "specialist": info.get("specialist", "General Physician"),
                "description": info.get("description", ""),
                "avg_cost": info.get("avg_cost_inr", {"min": 0, "max": 0, "avg": 0}),
                "precautions": info.get("precautions", []),
                "duration": info.get("duration", "Variable"),
                "color": info.get("color", "#6b7280")
            })

    return results, matched


# ── Chatbot conversation logic ────────────────────────────────────────────────
CHAT_STAGES = {
    "greeting": 0,
    "collecting_symptoms": 1,
    "confirming_symptoms": 2,
    "showing_results": 3,
    "followup": 4
}

def get_greeting_message():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        time_greet = "Good Morning"
        emoji = "🌅"
    elif 12 <= hour < 17:
        time_greet = "Good Afternoon"
        emoji = "☀️"
    elif 17 <= hour < 21:
        time_greet = "Good Evening"
        emoji = "🌆"
    else:
        time_greet = "Good Night"
        emoji = "🌙"

    return f"""{emoji} {time_greet}! Welcome to **MediSense AI** — your intelligent health companion.

I'm Dr. MediBot 🤖, your AI health assistant powered by advanced machine learning.

I can help you:
- 🔍 Analyze your symptoms and identify probable diseases
- 💰 Estimate treatment costs
- 👨‍⚕️ Recommend the right specialist
- 💊 Give you precautionary advice

**Please tell me your symptoms.** For example:
*"I have fever, headache, and body aches"*

⚠️ **Important**: This is an AI health assistant for informational purposes. Always consult a qualified doctor for medical advice."""


def generate_bot_response(user_message, conversation_history, collected_symptoms):
    """Generate contextual chatbot response."""
    msg_lower = user_message.lower()
    
    # Greetings
    greet_words = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "namaste", "start"]
    if any(w in msg_lower for w in greet_words) and len(collected_symptoms) == 0:
        return {
            "type": "greeting",
            "message": get_greeting_message(),
            "suggestions": ["I have fever and headache", "Chest pain and breathlessness", "Skin rash and itching", "Stomach pain and nausea"]
        }
    
    # Thank you / Good feedback
    thank_words = ["thank", "thanks", "great", "awesome", "good", "nice", "helpful"]
    if any(w in msg_lower for w in thank_words) and len(collected_symptoms) == 0:
        return {
            "type": "thanks",
            "message": "😊 You're very welcome! Remember, your health is your greatest wealth. 💚\n\nFeel free to describe any symptoms whenever you need help. Stay healthy and take care! 🌟",
            "suggestions": ["Check new symptoms", "I have a different problem"]
        }

    # Extract symptoms from message
    new_symptoms = extract_symptoms_from_text(user_message)
    
    # Add to collected symptoms
    all_symptoms = list(set(collected_symptoms + new_symptoms))
    
    if not all_symptoms:
        return {
            "type": "no_symptoms",
            "message": "🤔 I couldn't quite identify specific symptoms from your message. Could you describe what you're feeling more clearly?\n\n**Try saying things like:**\n- \"I have fever, headache and body ache\"\n- \"I feel nauseous and have stomach pain\"\n- \"I have chest pain and difficulty breathing\"",
            "suggestions": ["Fever and chills", "Headache and dizziness", "Cough and breathlessness", "Skin rash and itching"],
            "collected_symptoms": all_symptoms
        }

    # Show collected symptoms and predict
    symptom_display = [get_symptom_display_name(s) for s in all_symptoms]
    
    # Get predictions
    result = predict_diseases(all_symptoms)
    
    if result is None:
        return {
            "type": "error",
            "message": "⚠️ Our prediction model is being loaded. Please ensure `python train_model.py` has been run first.",
            "collected_symptoms": all_symptoms
        }
    
    predictions, matched = result
    
    if not predictions:
        return {
            "type": "no_prediction",
            "message": f"🔍 I found these symptoms: **{', '.join(symptom_display)}**\n\nHmm, I couldn't confidently match these to a specific disease. This could mean the symptoms are early-stage or complex.\n\n🏥 **Please consult a General Physician** for a thorough examination.",
            "collected_symptoms": all_symptoms
        }

    # More symptoms prompt
    more_syms_msg = ""
    if len(all_symptoms) < 4:
        more_syms_msg = "\n\n💡 **Tip**: Add more symptoms for a more accurate prediction!"

    return {
        "type": "prediction",
        "message": f"✅ I've analyzed **{len(all_symptoms)} symptoms** you described:\n**{', '.join(symptom_display)}**{more_syms_msg}",
        "predictions": predictions,
        "collected_symptoms": all_symptoms,
        "suggestions": ["Add more symptoms", "Tell me about the top disease", "What specialist should I see?", "Analyze new symptoms"]
    }


# ── Flask Routes ──────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    conversation_history = data.get("history", [])
    collected_symptoms = data.get("collected_symptoms", [])
    
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    
    response = generate_bot_response(user_message, conversation_history, collected_symptoms)
    return jsonify(response)


@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()
    symptoms = data.get("symptoms", [])
    
    if not symptoms:
        return jsonify({"error": "No symptoms provided"}), 400
    
    if model_data is None:
        return jsonify({"error": "Model not loaded. Run train_model.py first."}), 503
    
    result = predict_diseases(symptoms)
    if result is None:
        return jsonify({"error": "Could not match symptoms to model features"}), 400
    
    predictions, matched = result
    return jsonify({
        "predictions": predictions,
        "matched_symptoms": matched,
        "total_symptoms_given": len(symptoms)
    })


@app.route("/api/symptoms", methods=["GET"])
def get_symptoms():
    """Return all known symptoms for autocomplete."""
    query = request.args.get("q", "").lower()
    symptoms = [
        {"key": s, "label": get_symptom_display_name(s)}
        for s in ALL_SYMPTOMS
        if s != "prognosis" and (not query or query in s.replace("_", " ").lower())
    ]
    return jsonify(symptoms[:20])  # limit for performance


@app.route("/api/diseases", methods=["GET"])
def get_diseases():
    """Return all diseases with basic info."""
    diseases = []
    for name, info in DISEASE_INFO.items():
        diseases.append({
            "name": name,
            "emoji": info.get("emoji", "🏥"),
            "severity": info.get("severity", 5),
            "specialist": info.get("specialist", "General Physician"),
            "avg_cost": info.get("avg_cost_inr", {}),
            "color": info.get("color", "#6b7280")
        })
    return jsonify(diseases)


@app.route("/api/disease/<name>", methods=["GET"])
def get_disease(name):
    """Get detailed info about a specific disease."""
    info = get_disease_info(name)
    if not info:
        return jsonify({"error": "Disease not found"}), 404
    return jsonify({"name": name, **info})


@app.route("/api/greeting", methods=["GET"])
def greeting():
    return jsonify({"message": get_greeting_message()})


@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "online",
        "model_loaded": model_data is not None,
        "diseases": len(DISEASE_INFO),
        "symptoms": len([s for s in ALL_SYMPTOMS if s != "prognosis"]),
        "accuracy": f"{model_data['accuracy']*100:.1f}%" if model_data else "N/A"
    })


if __name__ == "__main__":
    print("\n[HOSPITAL] MediSense AI -- Starting Server")
    print("=" * 40)
    print("URL: http://localhost:5000")
    print("[BOT] AI Health Chatbot Ready")
    print("=" * 40)
    app.run(debug=True, host="0.0.0.0", port=5000)
