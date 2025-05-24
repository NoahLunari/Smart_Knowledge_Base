from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from db_handler import get_all_labels
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def classify_ticket(text):
    labels = get_all_labels()
    if not labels:
        return "unclassified", "Medium", 0.0

    # Embed the ticket description
    ticket_vec = model.encode([text])[0]

    # Embed all labels
    label_vecs = model.encode(labels)

    # Compute cosine similarities
    sims = cosine_similarity([ticket_vec], label_vecs)[0]
    top_index = np.argmax(sims)

    best_label = labels[top_index]
    confidence = float(sims[top_index])  # Convert numpy float to Python float

    return best_label, "Medium", round(confidence, 2)
