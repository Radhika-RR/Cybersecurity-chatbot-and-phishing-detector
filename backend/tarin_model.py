import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download NLTK data
nltk.download('stopwords')

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize
    words = text.split()
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    # Stemming
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    return ' '.join(words)

def train_model():
    # Load the dataset
    df = pd.read_csv('data/spam_ham_dataset.csv')
    
    # Preprocess the text
    df['processed_text'] = df['text'].apply(preprocess_text)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        df['processed_text'], df['label_num'], test_size=0.2, random_state=42
    )
    
    # Vectorize the text
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_vec, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test_vec)
    print(classification_report(y_test, y_pred))
    
    # Save the model and vectorizer
    model_data = {
        'model': model,
        'vectorizer': vectorizer
    }
    
    with open('models/phishing_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print("Model trained and saved successfully")

if __name__ == "__main__":
    train_model()