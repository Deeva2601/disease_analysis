# 🏥 MediSense AI — Human Disease Prediction Chatbot

MediSense AI is a medical diagnosis assistant powered by Machine Learning (Random Forest) and Flask. It helps patients understand their symptoms, estimate treatment costs in India, and find the right specialists.

## 🚀 Getting Started

### 1. Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install flask scikit-learn pandas numpy
```

### 2. Train the Model
The model needs to be trained on the disease-symptom dataset first:
```bash
python train_model.py
```
This will create a `models/disease_model.pkl` file and a `data/` directory.

### 3. Start the Server
Launch the Flask application:
```bash
python app.py
```
Visit **http://localhost:5000** in your browser to start chatting.

## 📁 Project Structure
- `app.py`: Flask backend and REST API.
- `train_model.py`: ML training script.
- `disease_data.py`: Medical knowledge base and pricing.
- `templates/`: HTML user interface.
- `static/`: CSS styles, JavaScript logic, and images.
- `models/`: Trained ML model (generated after training).
- `data/`: CSV datasets (generated after training).

## ✨ Features
- **Intelligent Chatbot**: Natural language symptom extraction.
- **Top-3 Predictions**: Probable diseases with confidence scores.
- **Cost Estimation**: Average treatment costs in INR (Indian Rupees).
- **Specialist Referrals**: Advice on which doctor to visit.
- **Premium UI**: Hospital-grade dark theme with smooth animations.

---
**Disclaimer**: This project is for educational purposes only. Always consult a qualified medical professional for diagnosis and treatment.
