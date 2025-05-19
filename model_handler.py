from transformers import pipeline
import streamlit as st
from db_handler import get_all_labels, get_guide_by_label

@st.cache_resource
def load_classifier():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

classifier = load_classifier()

# Default priority settings (can be moved to DB later)
DEFAULT_PRIORITY = "Medium"
PRIORITY_MAP = {
    "login problem": "High",
    "password reset": "High",
    "Phone request": "Low",
    "Laptop request": "Low",
    "VPN issue": "High",
    "Email issue": "Low",
    "Printer issue": "High",
    "Other": "Medium",
    "Software request": "Low",
    "Hardware drop off": "Low"
}

def classify_ticket(text):
    labels = get_all_labels()
    if not labels:
        return "unclassified", DEFAULT_PRIORITY, 0.0

    result = classifier(text, candidate_labels=labels)
    label = result["labels"][0]
    confidence = round(result["scores"][0], 2)

    # Try getting priority from guide metadata (optional enhancement)
    guide = get_guide_by_label(label)
    priority = guide.get("priority", PRIORITY_MAP.get(label, DEFAULT_PRIORITY)) if guide else DEFAULT_PRIORITY

    return label, priority, confidence
