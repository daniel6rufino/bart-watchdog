# src/ai/model_loader.py
from transformers import pipeline

def load_bart_model():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
