from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.triage import detect_emergency, suggest_specialist
from backend.safety_filter import apply_safety_filter
from backend.hf_rewriter import rewrite_text

from rag.retriever import retrieve

app = FastAPI(title="Medical RAG Chatbot Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question.strip()
    print("📝 Question reçue :", question)

    # 1️⃣ Urgence — traiter en priorité
    emergency = detect_emergency(question)
    print("⚠️ Urgence :", emergency)

    # ✅ Si urgence détectée → réponse immédiate sans passer par le RAG
    if emergency:
        return {
            "response": (
                "🚨 **URGENCE MÉDICALE DÉTECTÉE**\n\n"
                "Vos symptômes peuvent indiquer une situation grave.\n"
                "**Appelez immédiatement le 15 (SAMU) ou le 112.**\n\n"
                "Ne restez pas seul(e). Signalez vos symptômes exactement à l'opérateur.\n\n"
                "⚠️ *Ce chatbot ne remplace pas les secours d'urgence.*"
            )
        }

    # 2️⃣ Spécialiste
    specialist = suggest_specialist(question)
    print("👨‍⚕️ Spécialiste :", specialist)

    # 3️⃣ RAG
    context_chunks = retrieve(question, k=3)
    context_text = "\n\n".join(context_chunks)

    # 4️⃣ Construire contexte brut
    response = context_text + f"\n\nOrientation : {specialist}"

    # 5️⃣ Filtre sécurité
    response_safe = apply_safety_filter(response)

    # 6️⃣ Reformuler avec Groq
    final_response = rewrite_text(question, response_safe)
    print("✅ Réponse finale :", final_response[:100])

    return {"response": final_response}