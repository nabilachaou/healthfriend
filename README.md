## 🩺 HealthFriend — AI Medical Chatbot

An AI-powered medical chatbot built from scratch, leveraging real scientific articles from PubMed to provide reliable and informative health insights.

## ✨ Features
- 🌍 Multilingual support (French, English, Arabic, Spanish, etc.)
- 🚨 Emergency detection with instant alerts
- 👨‍⚕️ Medical specialist recommendations
- 🔬 Answers based on trusted PubMed articles
## 🛠️ Tech Stack
Frontend: Next.js 13
Backend: FastAPI
AI: FAISS + Hugging Face + Groq (LLaMA 3.3)
Data Source: PubMed (NCBI API)
## ⚙️ Installation
🔹 Backend
pip install fastapi uvicorn sentence-transformers faiss-cpu biopython deep-translator groq python-dotenv

uvicorn backend.main:app --reload
🔹 Frontend
cd frontend
npm install
npm run dev
🔑 Environment Variables

Create a .env file inside the backend/ folder and add:

GROQ_API_KEY=your_api_key
HF_TOKEN=your_huggingface_token
⚠️ Disclaimer

This chatbot provides general medical information only and does not replace professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.
Setup
Add your API keys in backend/.env:
GROQ_API_KEY=your_key
HF_TOKEN=your_token

⚠️ This chatbot provides general information only and does not replace a doctor.
