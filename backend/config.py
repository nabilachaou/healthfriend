# backend/config.py

# Seuil pour déclencher alerte urgence
EMERGENCY_KEYWORDS = [
    "chest pain", "difficulty breathing", "unconscious", "severe headache"
]

# Disclaimer
DISCLAIMER = (
    "⚠️ Ce chatbot fournit des informations générales basées sur PubMed. "
    "Il ne remplace pas un professionnel de santé. "
    "En cas d’urgence, contactez immédiatement un médecin."
)

# Nombre de chunks à récupérer depuis RAG
TOP_K = 3