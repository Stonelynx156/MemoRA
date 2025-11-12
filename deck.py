import json
from pathlib import Path
from typing import Dict, List

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

INDEX_FILE = DATA_DIR / "decks_index.json"

def _ensure_index():
    if not INDEX_FILE.exists():
        INDEX_FILE.write_text(json.dumps({"decks": []}, indent=2))

def load_index() -> List[str]:
    _ensure_index()
    with INDEX_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)
    
def save_index(index: Dict) -> None:
    with INDEX_FILE.open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

#check deck file exists, if not create it
def _ensure_deck_file(deck_name: str):
    #removes whitespaces and turn to lowercase for filename
    safe = "".join(c if c.isalnum()else "_" for c in deck_name)
    deck_file = DATA_DIR / f"{safe}.json"
    if not deck_file.exists():
        deck_file.write_text(json.dumps({"cards": []}, indent=2))
    return deck_file

def create_deck(name: str) -> None:
    _ensure_index()
    #load index file
    index = load_index()
    decks = index.setdefault("decks", [])
    #if deck names not in index, add it
    if name not in decks:
        decks.append(name)
        save_index(index)
    _ensure_deck_file(name)
