# data/pubmed_chunk.py
import json
import re

with open("data/pubmed_clean.json", encoding="utf-8") as f:
    articles = json.load(f)

chunks = []

for a in articles:
    text = a["text"]
    pmid = a["pmid"]

    # Découper par sections PubMed connues
    section_pattern = r'(BACKGROUND|METHODS|RESULTS|CONCLUSION|OBJECTIVE|FINDINGS|SUMMARY)\s*:'
    parts = re.split(section_pattern, text, flags=re.IGNORECASE)

    if len(parts) > 1:
        # Recombiner section + contenu : ["BACKGROUND", "texte...", "RESULTS", "texte..."]
        i = 1
        while i < len(parts) - 1:
            section_name = parts[i].strip()
            section_content = parts[i + 1].strip()
            if len(section_content.split()) > 20:
                chunks.append({
                    "pmid": pmid,
                    "section": section_name,
                    "text": f"{section_name}: {section_content}"
                })
            i += 2
    else:
        # Pas de sections : découper par phrases groupées (chunks de ~100 mots)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        current_chunk = []
        word_count = 0

        for sentence in sentences:
            words = sentence.split()
            word_count += len(words)
            current_chunk.append(sentence)

            if word_count >= 100:
                chunk_text = " ".join(current_chunk)
                if len(chunk_text.split()) > 20:
                    chunks.append({
                        "pmid": pmid,
                        "section": "text",
                        "text": chunk_text
                    })
                current_chunk = []
                word_count = 0

        # Dernier chunk restant
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            if len(chunk_text.split()) > 20:
                chunks.append({
                    "pmid": pmid,
                    "section": "text",
                    "text": chunk_text
                })

with open("data/pubmed_chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)

print(f"✅ {len(chunks)} chunks créés dans data/pubmed_chunks.json")