#!/usr/bin/env python3
"""
anki_cli.py
A simple CLI flashcard app with SM-2 spaced repetition.
Python 3.7+
Save decks in a 'decks' folder as JSON files.
"""

import os
import json
import uuid
from datetime import datetime, timedelta

DECKS_DIR = "decks"

def ensure_decks_dir():
    if not os.path.exists(DECKS_DIR):
        os.makedirs(DECKS_DIR)

def deck_path(name):
    safe = name.replace("/", "_")
    return os.path.join(DECKS_DIR, f"{safe}.json")

def load_deck(name):
    p = deck_path(name)
    if not os.path.exists(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def save_deck(deck):
    p = deck_path(deck["name"])
    with open(p, "w", encoding="utf-8") as f:
        json.dump(deck, f, ensure_ascii=False, indent=2)

def list_decks():
    ensure_decks_dir()
    files = [f for f in os.listdir(DECKS_DIR) if f.endswith(".json")]
    decks = [os.path.splitext(f)[0] for f in files]
    return decks

def new_deck(name):
    deck = {
        "name": name,
        "created_at": datetime.utcnow().isoformat(),
        "cards": []
    }
    save_deck(deck)
    return deck

def new_card(front, back):
    # SM-2 fields: easiness (EF), interval (days), repetitions (consecutive correct), due_date
    card = {
        "id": str(uuid.uuid4()),
        "front": front,
        "back": back,
        "easiness": 2.5,         # EF
        "interval": 0,          # days
        "repetitions": 0,
        "created_at": datetime.utcnow().isoformat(),
        "due_date": datetime.utcnow().isoformat(),  # available immediately
        "history": []           # list of (date, quality)
    }
    return card

def add_card_to_deck(deck_name, front, back):
    deck = load_deck(deck_name)
    if deck is None:
        print("Deck tidak ditemukan.")
        return
    card = new_card(front, back)
    deck["cards"].append(card)
    save_deck(deck)
    print("Kartu ditambahkan.")

def sm2_update(card, quality):
    """
    Update card using SM-2 algorithm.
    quality: int 0..5
    """
    # ensure ints/floats
    q = int(quality)
    ef = float(card.get("easiness", 2.5))
    rep = int(card.get("repetitions", 0))
    interval = int(card.get("interval", 0))

    # record history
    card.setdefault("history", []).append({
        "date": datetime.utcnow().isoformat(),
        "quality": q
    })

    if q < 3:
        rep = 0
        interval = 1
    else:
        if rep == 0:
            interval = 1
        elif rep == 1:
            interval = 6
        else:
            # round to nearest int
            interval = max(1, int(round(interval * ef)))
        rep += 1

    # update easiness
    ef = ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    if ef < 1.3:
        ef = 1.3

    card["easiness"] = round(ef, 4)
    card["repetitions"] = rep
    card["interval"] = interval
    next_due = datetime.utcnow() + timedelta(days=interval)
    card["due_date"] = next_due.isoformat()

    return card

def cards_due(deck):
    today = datetime.utcnow()
    due = []
    for c in deck["cards"]:
        try:
            d = datetime.fromisoformat(c["due_date"])
        except Exception:
            d = datetime.utcnow()
        if d <= today:
            due.append(c)
    return due

def pretty_card_summary(card):
    return f"[{card['id'][:8]}] {card['front'][:60]}..."

def edit_card(deck_name, card_id, new_front=None, new_back=None):
    deck = load_deck(deck_name)
    if deck is None:
        print("Deck tidak ditemukan.")
        return
    changed = False
    for c in deck["cards"]:
        if c["id"].startswith(card_id) or c["id"] == card_id:
            if new_front is not None:
                c["front"] = new_front
                changed = True
            if new_back is not None:
                c["back"] = new_back
                changed = True
            break
    if changed:
        save_deck(deck)
        print("Kartu diupdate.")
    else:
        print("Kartu tidak ditemukan.")

def delete_card(deck_name, card_id):
    deck = load_deck(deck_name)
    if deck is None:
        print("Deck tidak ditemukan.")
        return
    before = len(deck["cards"])
    deck["cards"] = [c for c in deck["cards"] if not (c["id"].startswith(card_id) or c["id"] == card_id)]
    after = len(deck["cards"])
    if after < before:
        save_deck(deck)
        print("Kartu dihapus.")
    else:
        print("Kartu tidak ditemukan.")

def show_stats(deck):
    total = len(deck["cards"])
    due = len(cards_due(deck))
    learned = sum(1 for c in deck["cards"] if c.get("repetitions", 0) >= 3)
    print(f"Deck: {deck['name']}")
    print(f"Total kartu: {total}")
    print(f"Kartu due sekarang: {due}")
    print(f"Kartu dengan >=3 repetisi: {learned}")

def import_deck_from_json(path):
    if not os.path.exists(path):
        print("File tidak ada.")
        return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # check for expected structure; if simple list, convert
    if isinstance(data, list):
        name = os.path.splitext(os.path.basename(path))[0]
        deck = {"name": name, "created_at": datetime.utcnow().isoformat(), "cards": []}
        for item in data:
            front = item.get("front") or item.get("question") or ""
            back = item.get("back") or item.get("answer") or ""
            deck["cards"].append(new_card(front, back))
    elif isinstance(data, dict) and "cards" in data:
        deck = data
        if "name" not in deck:
            deck["name"] = os.path.splitext(os.path.basename(path))[0]
    else:
        print("Format JSON tidak dikenali.")
        return
    save_deck(deck)
    print(f"Deck '{deck['name']}' diimpor.")

def export_deck(deck_name, path):
    deck = load_deck(deck_name)
    if deck is None:
        print("Deck tidak ditemukan.")
        return
    with open(path, "w", encoding="utf-8") as f:
        json.dump(deck, f, ensure_ascii=False, indent=2)
    print(f"Deck diekspor ke {path}")

def review_session(deck_name):
    deck = load_deck(deck_name)
    if deck is None:
        print("Deck tidak ditemukan.")
        return
    due = cards_due(deck)
    if not due:
        print("Tidak ada kartu yang perlu direview sekarang.")
        return
    print(f"\nMulai sesi review: {len(due)} kartu due.\n")
    for i, c in enumerate(due, 1):
        print(f"--- Kartu {i}/{len(due)} ---")
        print("FRONT:")
        print(c["front"])
        input("\nTekan Enter untuk melihat BACK...")
        print("\nBACK:")
        print(c["back"])
        # ask quality 0..5
        while True:
            q = input("\nPenilaian (0=tidak ingat sama sekali ... 5=sempurna): ")
            if q.strip().isdigit() and 0 <= int(q) <= 5:
                q = int(q)
                break
            else:
                print("Masukkan angka antara 0 dan 5.")
        sm2_update(c, q)
        save_deck(deck)
        print(f"Disimpan. Next due: {c['due_date']}, EF: {c['easiness']}, interval: {c['interval']} hari\n")
    print("Sesi review selesai.")

def show_deck_cards(deck_name, show_all=True, limit=20):
    deck = load_deck(deck_name)
    if deck is None:
        print("Deck tidak ditemukan.")
        return
    cards = deck["cards"]
    if not show_all:
        cards = cards[:limit]
    for c in cards:
        d = c.get("due_date", "n/a")
        print(f"{c['id'][:8]} | EF={c.get('easiness', '')} | rep={c.get('repetitions',0)} | due={d} | {c['front'][:80]}")

def main_menu():
    ensure_decks_dir()
    while True:
        print("\n=== Anki-CLI (SM-2) ===")
        print("1) List deck")
        print("2) Buat deck baru")
        print("3) Pilih deck")
        print("4) Import deck (JSON)")
        print("5) Export deck (JSON)")
        print("0) Keluar")
        choice = input("Pilih: ").strip()
        if choice == "1":
            decks = list_decks()
            if not decks:
                print("Belum ada deck.")
            else:
                print("Deck yang tersedia:")
                for d in decks:
                    print(" -", d)
        elif choice == "2":
            name = input("Nama deck baru: ").strip()
            if not name:
                print("Nama kosong.")
            else:
                if load_deck(name):
                    print("Deck sudah ada.")
                else:
                    new_deck(name)
                    print("Deck dibuat.")
        elif choice == "3":
            name = input("Nama deck: ").strip()
            deck = load_deck(name)
            if deck is None:
                print("Deck tidak ditemukan.")
                continue
            deck_menu(deck)
        elif choice == "4":
            path = input("Path file JSON untuk diimport: ").strip()
            import_deck_from_json(path)
        elif choice == "5":
            name = input("Nama deck yang diekspor: ").strip()
            path = input("Path output JSON: ").strip()
            export_deck(name, path)
        elif choice == "0":
            print("Sampai jumpa!")
            break
        else:
            print("Pilihan tidak dikenal.")

def deck_menu(deck):
    while True:
        print(f"\n--- Deck: {deck['name']} ---")
        print("1) Tambah kartu")
        print("2) Tampilkan kartu (ringkasan)")
        print("3) Review session (due cards)")
        print("4) Edit kartu")
        print("5) Hapus kartu")
        print("6) Statistik deck")
        print("7) Export deck (JSON)")
        print("0) Kembali")
        choice = input("Pilih: ").strip()
        if choice == "1":
            front = input("Front (pertanyaan): ").strip()
            back = input("Back (jawaban): ").strip()
            add_card_to_deck(deck["name"], front, back)
            deck = load_deck(deck["name"])  # refresh
        elif choice == "2":
            show_deck_cards(deck["name"])
        elif choice == "3":
            review_session(deck["name"])
            deck = load_deck(deck["name"])  # refresh
        elif choice == "4":
            cid = input("Masukkan awal ID kartu (atau ID lengkap): ").strip()
            newf = input("Front baru (kosong = tidak diubah): ")
            newb = input("Back baru (kosong = tidak diubah): ")
            edit_card(deck["name"], cid, new_front=newf if newf else None, new_back=newb if newb else None)
            deck = load_deck(deck["name"])
        elif choice == "5":
            cid = input("Masukkan awal ID kartu (atau ID lengkap): ").strip()
            confirm = input("Yakin hapus? (y/N): ").strip().lower()
            if confirm == "y":
                delete_card(deck["name"], cid)
            deck = load_deck(deck["name"])
        elif choice == "6":
            show_stats(deck)
        elif choice == "7":
            path = input("Path file export (mis: /tmp/deck.json): ").strip()
            export_deck(deck["name"], path)
        elif choice == "0":
            break
        else:
            print("Pilihan tidak dikenal.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nKeluar. Sampai jumpa!")
