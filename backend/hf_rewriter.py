import re
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def clean_raw_text(text: str) -> str:
    # Supprimer listes d'auteurs
    author_pattern = re.compile(
        r'(?:[A-Z][a-z\-]+\s+[A-Z]{1,3}(?:\(\d+\))+,?\s*){3,}',
        re.UNICODE
    )
    text = author_pattern.sub(' ', text)

    # Supprimer affiliations type "(7)Department..."
    text = re.sub(
        r'\(\d+\)[^.]*(?:Department|Division|University|Hospital|Institute|Center|School|Faculty|College)[^.]*\.',
        '', text, flags=re.IGNORECASE
    )

    text = re.sub(r'Author information:.*?(?=BACKGROUND|METHODS|RESULTS|CONCLUSION|$)', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'doi:\s*\S+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'PMID:\s*\d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'©.*$', '', text, flags=re.DOTALL)
    text = re.sub(
        r'(Conflict of interest|Competing interests|Ethics approval|Declaration of Helsinki|Informed consent).*$',
        '', text, flags=re.IGNORECASE | re.DOTALL
    )

    section_match = re.search(
        r'(BACKGROUND|RESULTS|CONCLUSION|FINDINGS|OBJECTIVE)\s*:',
        text, re.IGNORECASE
    )
    if section_match:
        text = text[section_match.start():]

    text = re.sub(
        r'METHODS?\s*:.*?(?=(BACKGROUND|RESULTS|CONCLUSION|FINDINGS|$))',
        '', text, flags=re.IGNORECASE | re.DOTALL
    )

    # ✅ Supprimer caractères spéciaux qui cassent l'API
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\x20-\x7E\n]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:1500]  # Réduire pour éviter les erreurs


def rewrite_with_groq(question: str, context: str) -> str:
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        print("❌ GROQ_API_KEY manquante dans .env")
        return None

    print(f"🔑 Clé Groq chargée : {groq_api_key[:8]}...")

    # ✅ Nettoyer la question aussi
    question_clean = question.encode('ascii', 'ignore').decode('ascii')

    prompt = (
        "You are a helpful medical assistant. Answer the patient's question based ONLY on the medical extracts provided.\n"
        "Guidelines:\n"
        "- Give a complete and detailed answer (5-7 sentences)\n"
        "- Use simple, clear language accessible to everyone\n"
        "- Structure your answer: explain the condition, then symptoms/treatments/causes depending on the question\n"
        "- Do NOT mention authors, studies, or journal names\n"
        "- Do NOT say 'based on the extracts' or 'according to the text'\n"
        "- If the extracts don't fully answer the question, say so honestly\n\n"
        f"Patient question: {question_clean}\n\n"
        f"Medical extracts:\n{context}"
    )

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 600,
                "temperature": 0.3
            },
            timeout=15
        )

        if not response.ok:
            print(f"❌ Erreur Groq {response.status_code}: {response.text[:200]}")
            return None

        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        print("✅ Réponse Groq :", answer[:100])
        return answer

    except Exception as e:
        print(f"❌ Erreur Groq API: {e}")
        return None


def rewrite_text(question: str, text: str) -> str:
    # 1️⃣ Extraire orientation
    orientation = ""
    for line in text.split("\n"):
        if "Orientation" in line:
            orientation = line.replace("Orientation :", "").strip()

    # 2️⃣ Nettoyer le contexte
    chunks = text.split("\n\n")
    clean_chunks = []
    for chunk in chunks:
        if any(kw in chunk for kw in ["Orientation", "URGENCE"]):
            continue
        cleaned = clean_raw_text(chunk)
        if len(cleaned) > 50:
            clean_chunks.append(cleaned)

    context = "\n\n".join(clean_chunks[:3])

    if not context.strip():
        return (
            "No precise medical information found for this question.\n\n"
            "⚠️ *This chatbot provides general information only. Consult a doctor.*"
        )

    # 3️⃣ Reformuler avec Groq
    reformulated = rewrite_with_groq(question, context)

    # 4️⃣ Fallback
    if not reformulated:
        sentences = re.split(r'(?<=[.!?])\s+', context)
        reformulated = " ".join(s for s in sentences[:3] if len(s) > 40)

    # 5️⃣ Réponse finale
    response = f"📋 **Medical Information**\n\n{reformulated}\n"
    if orientation:
        response += f"\n👨‍⚕️ **Consult**: {orientation}"
    response += "\n\n⚠️ *This information is general and does not replace a doctor.*"

    return response