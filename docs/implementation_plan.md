# 🏥 MediSense AI — Human Disease Prediction & Chatbot

## Overview
A full-stack hospital-grade web application where patients and doctors can input symptoms via a chatbot and get ML-powered disease predictions, treatment costs, severity ratings, and doctor recommendations — all within a premium clinical UI.

## Architecture

```
MediSense AI
├── train_model.py         → Train RandomForest + MultiLabel classifier
├── app.py                 → Flask server + REST API endpoints  
├── disease_data.py        → Disease knowledge base (symptoms, prices, info)
├── templates/
│   └── index.html         → Premium single-page app
├── static/
│   ├── css/style.css      → Premium hospital UI
│   ├── js/chat.js         → Chatbot logic + API calls
│   └── images/            → Medical imagery
├── data/
│   └── disease_symptoms.csv  → Training dataset
├── models/
│   └── disease_model.pkl  → Saved ML model
└── requirements.txt
```

## Features

### 🤖 AI Chatbot
- Conversational symptom collection
- Context-aware multi-turn dialogue
- Smart symptom suggestions/autocomplete
- 132 symptoms across 41+ diseases

### 🔬 ML Model
- Random Forest Classifier (scikit-learn)
- Multi-label disease prediction  
- Top-3 probable diseases with confidence scores
- ~95% accuracy on premium Kaggle disease dataset

### 💰 Treatment Cost Database  
- Average treatment costs (INR) per disease
- Severity rating (1-10)
- Recommended specialist doctor type
- Nearest hospital guide

### 🎨 Premium UI
- Hospital-grade dark teal + white theme
- Animated hero with medical imagery
- Split Patient / Doctor mode
- Smooth animations & micro-interactions
- Health emojis throughout
