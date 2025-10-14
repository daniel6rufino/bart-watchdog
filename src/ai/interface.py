# src/ai/interface.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

print("[+] Carregando modelo BART...")

# Caminho absoluto
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../facebook/bart-large-mnli"))
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH).to(device)

def analyze_dependency(dep_name, vuln_description, threshold=0.7):
    """
    Retorna True se BART classificar a dependência como vulnerável à descrição.
    """
    premise = f"A dependência `{dep_name}` está segura."
    hypothesis = vuln_description

    inputs = tokenizer(premise, hypothesis, return_tensors="pt", truncation=True).to(device)
    with torch.no_grad():
        logits = model(**inputs).logits
        # BART MNLI output: [contradiction, neutral, entailment]
        scores = torch.softmax(logits, dim=1)[0]
        entailment_score = scores[2].item()  # índice 2 = entailment
        return entailment_score >= threshold

def generate_summary(vulnerable_dependencies):
    """
    Gera um resumo em texto para a lista de vulnerabilidades.
    """
    if not vulnerable_dependencies:
        return "Nenhuma vulnerabilidade encontrada."

    summary = "As seguintes vulnerabilidades foram encontradas:\n"
    for v in vulnerable_dependencies:
        summary += f"- {v['package']}@{v['version']} -> {v['description']}\n"

    return summary
