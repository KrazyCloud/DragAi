from utils.log import logger
from sklearn.metrics.pairwise import cosine_similarity
from plugin.modelLoader import vectorizer, question_vectors
from plugin.modelLoader import answers
import numpy as np

# ML models
# Function to get the best answer
def get_answer(user_question):
    logger.info(f"Received question: {user_question}")
    user_question_vector = vectorizer.transform([user_question])
    similarities = cosine_similarity(user_question_vector, question_vectors)
    best_match_index = np.argmax(similarities)
    best_answer = answers[best_match_index]
    logger.info(f"Best match answer: {best_answer}")
    return best_answer