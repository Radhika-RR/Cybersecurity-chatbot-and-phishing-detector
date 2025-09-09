# Cybersecurity-chatbot-and-phishing-detector
CyberGuard Assistant is a full-stack cybersecurity project with a phishing detector and AI-powered QnA chatbot. It uses ML to classify phishing emails and a JSON-based chatbot for cybersecurity awareness. Built with FastAPI backend, and HTML/CSS/JS frontend

# Cybersecurity Assistant

A web application that provides:
1. Phishing email detection using machine learning
2. Cybersecurity Q&A chatbot

## Setup Instructions

### Using Docker (Recommended)

1. Make sure you have Docker and Docker Compose installed
2. Clone this repository
3. Place your `spam_ham_dataset.csv` in the `backend/data/` directory
4. Run: `docker-compose up --build`
5. Open your browser and go to `http://localhost:8000`

### Manual Setup

1. Install Python 3.9+ and required packages:

2. Download NLTK data:
```python
import nltk
nltk.download('stopwords')