🩺 HealthFriend — AI Medical Chatbot
An AI-powered medical chatbot built from scratch, based on real PubMed scientific articles.
Features

🌍 Multilingual support (FR, EN, AR, ES...)
🚨 Emergency detection with instant alert
👨‍⚕️ Medical specialist recommendation
🔬 Answers sourced from PubMed articles

Tech Stack

Frontend : Next.js 13
Backend : FastAPI
AI : FAISS + HuggingFace + Groq (Llama 3.3)
Data : PubMed NCBI API

Installation
bash# Backend
pip install fastapi uvicorn sentence-transformers faiss-cpu biopython deep-translator groq python-dotenv
uvicorn backend.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
Setup
Add your API keys in backend/.env:
GROQ_API_KEY=your_key
HF_TOKEN=your_token

⚠️ This chatbot provides general information only and does not replace a doctor.
