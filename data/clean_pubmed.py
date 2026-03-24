import json
import re

# ⚠️ Forcer UTF-8
with open("data/pubmed_raw.json", encoding="utf-8") as f:
    articles = json.load(f)

clean_articles = []

for a in articles:
    text = a["text"]
    text = re.sub(r"\n+", " ", text)       # enlever sauts de ligne
    text = re.sub(r"\[\d+\]", "", text)    # enlever références
    text = re.sub(r"\s+", " ", text).strip()
    if len(text.split()) > 20:             # conserver textes significatifs
        clean_articles.append({"pmid": a["pmid"], "text": text})

# ⚠️ Sauvegarde aussi en UTF-8
with open("data/pubmed_clean.json", "w", encoding="utf-8") as f:
    json.dump(clean_articles, f, indent=2, ensure_ascii=False)

print(f"Nettoyé {len(clean_articles)} articles.")