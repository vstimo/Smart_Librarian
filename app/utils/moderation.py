import re
import unicodedata

# Normalizare simpla: lower, scoate diacritice, inlocuieste leet
_LEET = str.maketrans({
    "4": "a", "@": "a",
    "1": "i", "!": "i", "|": "i",
    "3": "e",
    "0": "o",
    "$": "s", "5": "s",
    "7": "t"
})

def _strip_accents(s: str) -> str:
    nfkd = unicodedata.normalize('NFKD', s)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


def _normalize(text: str) -> str:
    text = text.lower()
    text = _strip_accents(text) # elimina diacriticele romanesti
    text = text.translate(_LEET) # 1d!0t -> idiot
    return text

BLOCKLIST = {
    "idiot", "prost", "prostule", "tampit", "imbecil",
    "moron", "stupid", "hate", "ura", "urasc",
    "dispari", "du-te dracu", "dracu", "futu", "fmm",
    "kill", "omor", "omora", "nazist", "rasist"
}

# Construim o expresie regulată robustă pe baza blocklist-ului normalizat
# Face regex care cauta orice cuvant/expresie din BLOCKLIST ca termen intreg
_WORD_RE = re.compile(r"\b(" + "|".join(re.escape(w) for w in sorted(BLOCKLIST, key=len, reverse=True)) + r")\b")

def is_offensive(user_text: str) -> bool:
    norm = _normalize(user_text)
    return bool(_WORD_RE.search(norm))