# backend/safety_filter.py
from backend.config import DISCLAIMER

def apply_safety_filter(response_text: str) -> str:
    """
    Ajoute un disclaimer et filtre les réponses inappropriées
    """
    # Exemple simple : vérifier longueur minimum
    if len(response_text.strip()) < 10:
        response_text = "Aucune information fiable trouvée."
    
    # Ajouter disclaimer à la fin
    return response_text + "\n\n" + DISCLAIMER