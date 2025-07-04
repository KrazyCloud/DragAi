from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Initialize the model and pipeline
model = pipeline("question-answering", model=r"distilbert-base-uncased-distilled-squad")

# Load dataset
data = pd.read_csv('chatbot.csv')
data = data.dropna(subset=['Question', 'Answer'])

# Extract questions and answers
questions = data['Question'].tolist()
answers = data['Answer'].tolist()

# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)