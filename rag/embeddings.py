import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from tqdm import tqdm

# 1️⃣ Charger les chunks nettoyés en UTF-8
with open("data/pubmed_chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [c["text"] for c in chunks]

# 2️⃣ Choisir le modèle d'embedding
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 3️⃣ Créer les embeddings
print("Création des embeddings...")
embeddings = model.encode(texts, show_progress_bar=True)
embeddings = np.array(embeddings).astype('float32')

# 4️⃣ Créer l'index FAISS
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  # L2 distance
index.add(embeddings)

# 5️⃣ Sauvegarder l'index
faiss.write_index(index, "rag/pubmed_index.faiss")
print(f"Index FAISS créé avec {index.ntotal} vecteurs.")