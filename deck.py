import json
from pathlib import Path
from typing import Dict, List
import os

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
    
def deck_file_path(name: str) -> Path:
    #removes whitespaces and turn to lowercase for filename
    safe = "".join(c if c.isalnum()else "_" for c in name)
    return DATA_DIR / f"{safe}.json"

#check deck file exists, if not create it
def _ensure_deck_file(name: str) -> None:
    path = deck_file_path(name)
    if not path.exists():
        path.write_text(json.dumps({"cards": []}, indent=2))
    

def create_deck(name: str) -> None:
    _ensure_index()
    #load index file
    index = load_index()
    decks = index.setdefault("decks", [])
    #if deck names not in index, add it
    if name not in decks:
        decks.append(name)
        with INDEX_FILE.open("w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)
    _ensure_deck_file(name)

def load_decks(name: str) -> List[Dict]:
    _ensure_deck_file(name)
    with deck_file_path(name).open("r", encoding="utf-8")as f:
        data = json.load(f)
    return data.get("cards", [])

def save_decks(name: str, cards: List[Dict]) -> None:
    _ensure_deck_file(name)
    path = deck_file_path(name)
    with path.open("w", encoding="utf-8") as f:
        json.dump({"cards": cards}, f, indent=2)
