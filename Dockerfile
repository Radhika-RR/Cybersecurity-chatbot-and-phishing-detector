FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('stopwords')"

# Copy application code
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Create directories for model and data
RUN mkdir -p backend/models backend/data backend/chatbot

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]