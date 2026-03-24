import faiss
import json
from sentence_transformers import SentenceTransformer

try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False
    print("⚠️ deep-translator non installé, pip install deep-translator")

# 1️⃣ Charger le modèle d'embedding
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 2️⃣ Charger l'index FAISS
index = faiss.read_index("rag/pubmed_index.faiss")

# 3️⃣ Charger les chunks
with open("data/pubmed_chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)


def translate_to_english(text: str) -> str:
    """
    Traduit automatiquement la question en anglais (FR, AR, ES... → EN)
    pour mieux matcher les chunks PubMed en anglais
    """
    if not TRANSLATOR_AVAILABLE:
        return text
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        print(f"🔤 Question traduite : '{text}' → '{translated}'")
        return translated
    except Exception as e:
        print(f"⚠️ Traduction échouée, question originale utilisée : {e}")
        return text


def retrieve(query: str, k: int = 3):
    """
    Traduit la question en anglais puis cherche dans FAISS
    """
    # ✅ Traduire la question en anglais avant la recherche
    query_en = translate_to_english(query)

    # Encoder la question
    query_embedding = model.encode([query_en]).astype('float32')

    # Chercher les k plus proches voisins
    distances, indices = index.search(query_embedding, k)

    # Récupérer les textes
    results = [chunks[i]["text"] for i in indices[0]]
    print(f"📚 {k} chunks récupérés pour : '{query_en}'")
    return results


if __name__ == "__main__":
    question = "Quels sont les symptômes du diabète ?"
    top_chunks = retrieve(question, k=3)
    for i, c in enumerate(top_chunks):
        print(f"Chunk {i+1}:\n{c}\n")