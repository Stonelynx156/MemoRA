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

def load_index() -> Dict[str,List[str]]:
    _ensure_index()
    with INDEX_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)
def save_index(index: Dict[str, List[str]]) -> None:
    with INDEX_FILE.open("w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    
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
        save_index(index)
    _ensure_deck_file(name)

def load_deck(name: str) -> List[Dict]:
    _ensure_deck_file(name)
    with deck_file_path(name).open("r", encoding="utf-8")as f:
        data = json.load(f)
    return data.get("cards", [])

def load_limit(deck: str):
    path = deck_file_path(deck)
    with deck_file_path(deck).open("r", encoding="utf-8") as f:
        data = json.load(f)
    if "limit" not in data:
        data["limit"] = {"new_limit": 20, "due_limit":100}
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    return data.get("limit",{})

def save_limit(deck: str, limit_new: int, limit_due: int):
    path = deck_file_path(deck)
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    data["limit"] = {"new_limit": limit_new,"due_limit": limit_due}
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent = 2)

def save_deck(name: str, cards: List[Dict]) -> None:
    _ensure_deck_file(name)
    path = deck_file_path(name)
    with path.open("w", encoding="utf-8") as f:
        json.dump({"cards": cards}, f, indent=2)

def delete_deck(name: str) -> None:
    _ensure_deck_file(name)
    list_deck = load_index()
    os.remove(deck_file_path(name))
    if name in list_deck["decks"]:
        list_deck["decks"].remove(name)
    save_index(list_deck)

def rename_deck(old_name: str, new_name: str) -> None:
    _ensure_deck_file(old_name)
    list_decks = load_index()
    old = deck_file_path(old_name)
    new = deck_file_path(new_name)
    if old_name in list_decks["decks"]:
        index = list_decks["decks"].index(old_name)
        list_decks["decks"][index] = new_name
    os.rename(old, new)
    save_index(list_decks)