from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pickle
import pandas as pd
import json
import re
import os
from typing import Dict

# Initialize FastAPI
app = FastAPI(title="Cybersecurity API")

# Enable CORS (allow frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
frontend_dir = os.path.join(project_root, "frontend")
model_dir = os.path.join(current_dir, "models")
chatbot_dir = os.path.join(current_dir, "chatbot")

# Serve static frontend files (CSS, JS)
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Serve index.html at root
@app.get("/")
async def root():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="Frontend not found")

# Load phishing detection model
model = None
vectorizer = None
try:
    model_path = os.path.join(model_dir, "phishing_model.pkl")
    with open(model_path, "rb") as f:
        model_data = pickle.load(f)
        model = model_data["model"]
        vectorizer = model_data["vectorizer"]
    print("Model loaded successfully")
except FileNotFoundError:
    print("Model file not found. Please train the model first.")
except Exception as e:
    print(f"Error loading model: {str(e)}")

# Load chatbot QnAs
qna_data = {"questions": []}
try:
    qna_path = os.path.join(chatbot_dir, "qna.json")
    with open(qna_path, "r") as f:
        qna_data = json.load(f)
except FileNotFoundError:
    print("QnA file not found. Defaulting to empty QnA data.")

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
    for qna in qna_data.get("questions", []):
        for pattern in qna.get("patterns", []):
            if re.search(pattern, user_message):
                return ChatResponse(response=qna["response"])
    return ChatResponse(
        response="I'm not sure how to answer that. Could you please rephrase your question?"
    )

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# API info
@app.get("/api")
async def api_info():
    return {"message": "Cybersecurity API is running"}
