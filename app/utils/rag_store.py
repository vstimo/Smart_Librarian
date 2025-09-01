# rag_store.py

import os, re
from pathlib import Path
#from dotenv import load_dotenv, find_dotenv
from typing import Any, Dict, List
import chromadb # type: ignore
from chromadb.utils import embedding_functions # type: ignore

DATA_MD = Path("app/data/book_summaries.md") # calea catre fisierul cu rezumatele
DB_DIR = Path(".chroma_db") # calea catre baza de date
COLLECTION = "book_summaries" # numele colectiei

# load_dotenv(find_dotenv(filename="../.env", usecwd=True), override=True)
EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL")

def _parse_markdown(content: str) -> List[Dict[str, Any]]:
    """
    Transforma fisierului de markdown in elemente structurate de formata
        [   { "title": "Titlu", "summary": "Rezumat" },
            ...
        ]
    """
    blocks = re.split(r"^##\s*Title:\s*", content, flags=re.MULTILINE)
    items = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Extrage titlul si continutul
        title, *rest = block.splitlines()
        summary = "\n".join(rest).strip()
        items.append({"title": title.strip(), "summary": summary})

    return items

def get_client_and_collection():
    """
    Pregateste conexiunea la ChromaDB si colectia cu embedding-uri OpenAI
    """
    DB_DIR.mkdir(exist_ok=True)
    client = chromadb.PersistentClient(path=str(DB_DIR))

    # transforma textul in embedding-uri
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key = os.getenv("OPENAI_API_KEY"),
        model_name = EMBED_MODEL)

    # Creeaza sau deschide colectia book_summaries (stocheaza textele si embeddingurile)
    col = client.get_or_create_collection(
        name = COLLECTION, embedding_function = openai_ef)
    return client, col # returneaza baza de date, colectia (indexul de carti)

def ingest_if_needed(force: bool = False):
    _, col = get_client_and_collection()

    if force: # sterge tot ce era anterior in colectie
        try:
            col.delete(where={})
        except Exception as e:
            print(f"Error deleting old data: {e}")
            pass
    else:
        print("Data already ingested. Use force=True to re-ingest.")

    # daca colectia are deja date (si force=False) returnam numarul de elemente
    # scopul este sa nu incarcam din nou aceleasi carti de fiecare data cand ruleaza programul
    count = col.count()
    if count and not force:
        return count
    
    # citeste fisierul book_summaries.md
    md_text = DATA_MD.read_text(encoding="utf-8")
    items = _parse_markdown(md_text)

    # adauga elementele in colectie
    ids = [] # ID unic
    docs = [] # rezumatul proprius zis
    metas = [] # titlu
    for i, it in enumerate(items):
        ids.append(f"book-{i}")
        docs.append(it["summary"]) # searchable content
        metas.append({"title": it["title"]})

    if ids:
        col.add(ids=ids, documents=docs, metadatas=metas)
    return col.count()



def retrieve_candidates(query: str, n: int = 5) -> List[Dict[str, Any]]:
    """
    Cauta in colectia ChromaDB si intoarce cele mai apropiate rezumate de query-ul meu, 
    ordonate dupa relevanta semantica"""
    _, col = get_client_and_collection()
    # Raspunsul contine: (cat de apropiat e rezumatul - valoare num., rezumatul, titlu)
    result = col.query(
        query_texts=[query],
        n_results=n,
        include=["distances", "documents", "metadatas"])
    out = []
    for id in range(len(result.get("ids", [[]])[0])):
        out.append({
            "title": result["metadatas"][0][id]["title"],
            "summary": result["documents"][0][id],
            "distance": result["distances"][0][id],
        })
    return out


if __name__ == "__main__":
    added = ingest_if_needed(force=False)
    print(f"ChromaDB ready. Items in collection: {added}")