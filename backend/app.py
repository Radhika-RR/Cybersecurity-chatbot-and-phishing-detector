from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import re
from typing import List, Dict
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="Cybersecurity API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
frontend_dir = os.path.join(project_root, 'frontend')

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Serve the main page
@app.get("/")
async def read_index():
    return FileResponse(os.path.join(frontend_dir, 'index.html'))

# Load phishing detection model
model = None
vectorizer = None
try:
    model_path = os.path.join(current_dir, 'models/phishing_model.pkl')
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
        model = model_data['model']
        vectorizer = model_data['vectorizer']
    print("Model loaded successfully")
except FileNotFoundError:
    print("Model file not found. Please train the model first.")
except Exception as e:
    print(f"Error loading model: {str(e)}")

# Load chatbot QnAs
try:
    qna_path = os.path.join(current_dir, 'chatbot/qna.json')
    with open(qna_path, 'r') as f:
        qna_data = json.load(f)
except FileNotFoundError:
    qna_data = {"questions": []}
    print("QnA data not found.")

# Request models
class EmailRequest(BaseModel):
    text: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Phishing prediction endpoint
@app.post("/predict")
async def predict_phishing(email: EmailRequest):
    if not model or not vectorizer:
        raise HTTPException(status_code=503, detail="Model not trained yet")
    
    # Preprocess and vectorize the email text
    email_vector = vectorizer.transform([email.text])
    prediction = model.predict(email_vector)
    probability = model.predict_proba(email_vector)
    
    return {
        "is_phishing": bool(prediction[0]),
        "probability": float(probability[0][1]),
        "message": "Phishing email detected" if prediction[0] else "Legitimate email"
    }

# Chatbot endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    user_message = request.message.lower()
    
    # Simple pattern matching
    for qna in qna_data["questions"]:
        for pattern in qna["patterns"]:
            if re.search(pattern, user_message):
                return ChatResponse(response=qna["response"])
    
    # Default response if no match found
    return ChatResponse(
        response="I'm not sure how to answer that. Could you please rephrase your question?"
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# API info endpoint
@app.get("/api")
async def api_info():
    return {"message": "Cybersecurity API is running"}