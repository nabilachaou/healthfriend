# data/pubmed_fetch.py
from Bio import Entrez
import json
from tqdm import tqdm
import ssl
import csv

# ⚠️ Bypass SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

Entrez.email = "nabilachaou31@gmail.com"

# ✅ Suffixes cliniques pour cibler les articles utiles
CLINICAL_SUFFIXES = [
    "symptoms diagnosis",
    "treatment management",
    "early signs",
]

# Lire les maladies depuis le CSV
csv_file = "data/diseases.csv"
diseases = []
with open(csv_file, "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        diseases.append(row["disease"])

print(f"✅ {len(diseases)} maladies chargées")

# Construire les requêtes enrichies
queries = []
for disease in diseases:
    for suffix in CLINICAL_SUFFIXES:
        queries.append(f"{disease} {suffix}")

print(f"✅ {len(queries)} requêtes générées")

max_results = 3  # 3 articles par requête = base bien couverte sans surcharger
all_articles = []
seen_pmids = set()  # Éviter les doublons

for q in queries:
    try:
        handle = Entrez.esearch(db="pubmed", term=q, retmax=max_results, sort="relevance")
        record = Entrez.read(handle)
        ids = record["IdList"]

        for pmid in tqdm(ids, desc=f"📥 {q[:50]}"):
            if pmid in seen_pmids:
                continue
            seen_pmids.add(pmid)

            fetch_handle = Entrez.efetch(
                db="pubmed", id=pmid, rettype="abstract", retmode="text"
            )
            abstract = fetch_handle.read()
            all_articles.append({
                "pmid": pmid,
                "query": q,
                "text": abstract
            })

    except Exception as e:
        print(f"❌ Erreur pour '{q}': {e}")

# Sauvegarde
with open("data/pubmed_raw.json", "w", encoding="utf-8") as f:
    json.dump(all_articles, f, indent=2, ensure_ascii=False)

print(f"\n✅ {len(all_articles)} articles sauvegardés dans data/pubmed_raw.json")