import os
import ctypes
import msvcrt
import shutil
import json
import time
from tkinter import Tk, filedialog

from datetime import datetime, timezone
from deck import delete_deck, rename_deck, load_index, load_deck, save_deck
from cards import Card, card_status, add_card, reset_due, human_date
from console import (
    clear,
    read_key,
    set_color,
    center_text,
    wait_for_enter,
    input_with_esc,
    get_terminal_size,
    monitor_terminal_size,
    wait_for_key_with_resize,
    EXIT_TOKEN,
)

"""Material & Needs"""
#Import Warna
BLACK = 0x00
BLUE = 0x01
GREEN = 0x02
RED = 0x04
WHITE = 0x07
YELLOW = RED | GREEN
CYAN = GREEN | BLUE
MAGENTA = RED | BLUE
BRIGHT = 0x08

STD_OUTPUT_HANDLE = -11
h = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

options = [
                "Ringkasan",
                "Edit Kartu",
                "Tambah Kartu",
                "Informasi Kartu",
                "Daftar Semua Kartu",
                "Reset Waktu Semua Kartu",
                "Ganti Nama Deck",
                "Ekspor (JSON)",
                "Hapus Deck"
            ]

"""Fungsi kelola deck"""
#deck summary
def deck_summary(deck_name):
    set_color(BRIGHT | CYAN)
    print(center_text(f"=== Ringkasan Deck: {deck_name} ==="))
    set_color(WHITE)
    deck = load_deck(deck_name)
    print()
    print("     " + f"Total Kartu        : {len(deck)}")
    print("     " + f"Kartu baru         : {len([Card.from_dict(c) for c in deck if c.get("first_time") == True ])}")
    print("     " + f"kartu jatuh tempo  : {len([Card.from_dict(c) for c in deck if c.get("first_time") == False 
                                                 and datetime.isoformat(c.get("due") <= datetime.now(timezone.utc))])}")
    print("     " + f"Jadwal Terdekat    : {(datetime.fromisoformat(min([Card.from_dict(c).due for c in deck]))).strftime("%d/%B/%Y - %H:%M UTC")}")
    print("     " + f"Interval Rata Rata : {sum([Card.from_dict(c).interval for c in deck]) / len([Card.from_dict(c) for c in deck])}")
    print("     " + f"Interval Terbesar  : {max([Card.from_dict(c).interval for c in deck])}")
    print()
    set_color(BRIGHT | YELLOW)
    wait_for_enter(center_text("Tekan Enter untuk kembali..."))
    set_color(WHITE)

#tambah kartu baru
def new_cards(deck_name):
    set_color(BRIGHT | CYAN)
    print(center_text(f"=== Membuat kartu di: {deck_name} ==="))
    set_color(WHITE)
    print()
    set_color(BRIGHT | YELLOW)
    print(center_text("Tekan ESC untuk kembali..."))
    set_color(WHITE)
    print()
    front_cards, canceled = input_with_esc("Masukkan pertanyaan (front): ")
    if canceled:
        return
    if not front_cards.strip():
        set_color(RED)
        print()
        print(center_text("Pertanyaan tidak boleh kosong!"))
        set_color(BRIGHT | YELLOW)
        wait_for_enter(center_text("Tekan Enter untuk kembali..."))
        set_color(WHITE)
        return
    back_cards, canceled = input_with_esc("Masukkan jawaban (back)    : ")
    if canceled:
        return
    if not back_cards.strip():
        set_color(RED)
        print()
        print(center_text("Jawaban tidak boleh kosong!"))
        set_color(BRIGHT | YELLOW)
        wait_for_enter(center_text("Tekan Enter untuk kembali..."))
        set_color(WHITE)
        return
    add_card(front_cards, back_cards, deck_name)
    print()
    set_color(BRIGHT | YELLOW)
    wait_for_enter(center_text("Tekan Enter untuk kembali..."))
    set_color(WHITE)

#cek daftar kartu
def card_list(deck_name):
    set_color(BRIGHT | CYAN)
    print(center_text(f"=== Daftar Kartu di: {deck_name} ==="))
    set_color(WHITE)
    cards_raw = load_deck(deck_name)
    print()
    print("     " + "ID Kartu   | Pertanyaan (front) | Jawaban (back) ")
    print("     " + "-----------------------------------------------")
    for c in cards_raw:
        print("     " + f"{c.get("id")} | {c.get("front")} | {c.get("back")}")
    print()
    set_color(BRIGHT | YELLOW)
    wait_for_enter(center_text("Tekan Enter untuk kembali..."))
    set_color(WHITE)

#cek informasi kartu
def card_info(deck_name):
    cards_raw = load_deck(deck_name)
    set_color(BRIGHT | CYAN)
    print(center_text(f"=== Informasi Kartu di: {deck_name} ==="))
    set_color(WHITE)
    print()
    set_color(BRIGHT | YELLOW)
    print(center_text("Tekan ESC untuk kembali..."))
    set_color(WHITE)
    print()
    card_id, canceled = input_with_esc("Masukkan ID Kartu: ")
    if canceled:
        return
    for c in cards_raw:
        if c.get("id") == card_id:
            card = c
    if card_id not in (c.get("id") for c in cards_raw):
        set_color(RED)
        print()
        print(center_text("ID Kartu tidak valid!"))
        set_color(BRIGHT | YELLOW)
        wait_for_enter(center_text("Tekan Enter untuk kembali..."))
        set_color(WHITE)
        return
    print()
    print("     " + f"Pertanyaan (front) : {card.get("front")}")
    print("     " + f"Jawaban (back)     : {card.get("back")}")
    print("     " + f"Interval           : {card.get("interval")}")
    print("     " + f"EFactor            : {card.get("ease_factor")}")
    print("     " + f"Due Date           : {human_date(card.get("due"))}")
    print("     " + f"Kartu Baru         : {card.get("first_time")}")
    print()
    set_color(BRIGHT | YELLOW)
    wait_for_enter(center_text("Tekan Enter untuk kembali..."))
    set_color(WHITE)

#edit kartu
def card_edit(deck_name):
    prev_size = get_terminal_size()
    cards = [Card.from_dict(c) for c in load_deck(deck_name)]
    set_color(BRIGHT | CYAN)
    print(center_text(f"=== Edit Kartu di: {deck_name} ==="))
    set_color(WHITE)
    print()
    set_color(BRIGHT | YELLOW)
    print(center_text("Tekan ESC untuk kembali..."))
    set_color(WHITE)
    print()
    card_id, canceled = input_with_esc("Masukkan ID Kartu yang akan diedit: ")
    if canceled:
        return
    for c in cards:
        if c.id == card_id:
            card = c
    if card_id not in (c.id for c in cards):
        set_color(RED)
        print()
        print(center_text("ID Kartu tidak valid!"))
        set_color(BRIGHT | YELLOW)
        wait_for_enter(center_text("Tekan Enter untuk kembali..."))
        set_color(WHITE)
        return

    opt_selected = 0
    card_edit_options = [
        "1) Edit Pertanyaan (front)",
        "2) Edit Jawaban (back)",
        "3) Reset Waktu Kartu",
        "4) Hapus Kartu",    
    ]

    while True:
        cards = [Card.from_dict(c) for c in load_deck(deck_name)]
        for c in cards:
            if c.id == card_id:
                card = c
        clear()
        set_color(BRIGHT | CYAN)
        print(center_text(f"=== Edit Kartu di: {deck_name} ==="))
        set_color(WHITE)
        print()
        for idx, opt in enumerate(card_edit_options):
            if idx == opt_selected:
                set_color(BRIGHT | GREEN)
                print(center_text(f"> {opt} <"))
                set_color(WHITE)
            else:
                print(center_text(f"  {opt}"))
        
        key, prev_size = wait_for_key_with_resize(prev_size)
        if key == EXIT_TOKEN:
            return
        if key is None:
            continue
        if key == 'UP':
            if opt_selected > 0:
                opt_selected -= 1
        elif key == 'DOWN':
            if opt_selected < len(card_edit_options) - 1:
                opt_selected += 1
        elif key == 'ESC':
            break
        elif key == 'ENTER':
            choice = opt_selected + 1
            clear()
            if choice == 1:
                set_color(BRIGHT | CYAN)
                print(center_text(f"=== Edit Kartu di: {deck_name} ==="))
                set_color(WHITE)
                print()
                set_color(BRIGHT | YELLOW)
                print(center_text("Tekan ESC untuk kembali..."))
                set_color(WHITE)
                print()
                print(f"     Pertanyaan Lama: {card.front}")
                print()
                new_front, canceled = input_with_esc("     Masukkan Pertanyaan Baru: ")
                if canceled:
                    continue
                if not new_front.strip():
                    set_color(RED)
                    print()
                    print(center_text("Pertanyaan tidak boleh kosong!"))
                if new_front.strip():    
                    card.front = new_front
                    cards = [Card.to_dict(c)for c in cards]
                    save_deck(deck_name, cards)
                    print(f"     Pertanyaan telah diubah menjadi : {new_front}")
                set_color(BRIGHT | YELLOW)
                wait_for_enter(center_text("Tekan Enter untuk kembali..."))
                set_color(WHITE)
            elif choice == 2:
                set_color(BRIGHT | CYAN)
                print(center_text(f"=== Edit Kartu di: {deck_name} ==="))
                set_color(WHITE)
                print()
                set_color(BRIGHT | YELLOW)
                print(center_text("Tekan ESC untuk kembali..."))
                set_color(WHITE)
                print()
                print(f"     Jawaban Lama: {card.back}")
                print()
                new_back, canceled = input_with_esc("     Masukkan jawaban baru   : ")
                if canceled:
                    continue
                if not new_back.strip():
                    set_color(RED)
                    print()
                    print(center_text("Jawaban tidak boleh kosong!"))
                if new_back.strip():
                    card.back = new_back
                    cards = [Card.to_dict(c)for c in cards]
                    save_deck(deck_name, cards)
                    print(f"     Pertanyaan telah diubah menjadi : {new_back}")
                set_color(BRIGHT | YELLOW)
                wait_for_enter(center_text("Tekan Enter untuk kembali..."))
                set_color(WHITE)
            elif choice == 3:
                set_color(BRIGHT | CYAN)
                print(center_text(f"=== Edit Kartu di: {deck_name} ==="))
                set_color(WHITE)
                print()
                confirm = input("     Yakin reset waktu kartu ini? (y/n): ")
                if confirm.lower() == 'y':
                    card.due = datetime.now(timezone.utc).isoformat()
                    card.first_time = True
                    card.interval = 1
                    card.step = 1
                    card.ease_factor = 2.5
                    cards = [Card.to_dict(c)for c in cards]
                    save_deck(deck_name, cards)
                    print(center_text("Waktu telah direset")) 
                else:
                    print()
                    set_color(RED)
                    print(center_text("Operasi dibatalkan."))
                    set_color(WHITE)
                set_color(BRIGHT | YELLOW)
                wait_for_enter(center_text("Tekan Enter untuk kembali..."))
                set_color(WHITE)
                    
            
            elif choice == 4:
                set_color(BRIGHT | CYAN)
                print(center_text(f"=== Edit Kartu di: {deck_name} ==="))
                set_color(WHITE)
                print()
                confirm = input("     Yakin hapus kartu ini? (y/n): ")
                if confirm.lower() == 'y':
                    cards.remove(card)
                    cards = [Card.to_dict(c)for c in cards]
                    save_deck(deck_name, cards)
                    print()
                    set_color(RED)
                    print(center_text("Kartu telah dihapus."))
                    set_color(WHITE)
                    set_color(BRIGHT | YELLOW)
                    wait_for_enter(center_text("Tekan Enter untuk kembali..."))
                    set_color(WHITE)
                    return
                else:
                    print()
                    set_color(RED)
                    print(center_text("Operasi dibatalkan."))
                    set_color(WHITE)
                    set_color(BRIGHT | YELLOW)
                    wait_for_enter(center_text("Tekan Enter untuk kembali..."))
                    set_color(WHITE)

#reset semua kartu
def reset_times(deck_name):
    set_color(BRIGHT | CYAN)
    print(center_text(f"=== Reset Waktu Kartu di: {deck_name} ==="))
    set_color(WHITE)
    print()
    confirm = input("Apakah Anda yakin ingin mereset waktu semua kartu? (y/n): ")
    if confirm.lower() == 'y':
        reset_due(deck_name)
        print()
        set_color(RED)
        print(center_text("Waktu semua kartu telah direset."))
        set_color(WHITE)
    else:
        print()
        set_color(RED)
        print(center_text("Operasi dibatalkan."))
        set_color(WHITE)
    set_color(BRIGHT | YELLOW)
    wait_for_enter(center_text("Tekan Enter untuk kembali..."))
    set_color(WHITE)

#ganti nama deck
def change_name_deck(deck_name):
    set_color(BRIGHT | CYAN)
    print(center_text(f"=== Ganti Nama Deck: {deck_name} ==="))
    set_color(WHITE)
    print()
    set_color(BRIGHT | YELLOW)
    print(center_text("Tekan ESC untuk kembali..."))
    set_color(WHITE)
    print()
    new_name, canceled = input_with_esc("Masukkan nama deck baru: ")
    if canceled:
        return
    if not new_name.strip():
        set_color(RED)
        print()
        print(center_text("Nama deck tidak boleh kosong!"))
        set_color(BRIGHT | YELLOW)
        wait_for_enter(center_text("Tekan Enter untuk kembali..."))
        set_color(WHITE)
        return
    rename_deck(deck_name, new_name)
    print()
    print(center_text(f"Nama deck telah diubah menjadi: {new_name}"))
    print()
    set_color(BRIGHT | YELLOW)
    wait_for_enter(center_text("Tekan Enter untuk kembali..."))
    set_color(WHITE)

#ekspor deck
def export_deck(deck_name):
    set_color(BRIGHT | CYAN)
    print(center_text(f"=== Ekspor Deck: {deck_name} ==="))
    set_color(WHITE)
    print()
    
    # buka file explorer untuk memilih lokasi penyimpanan
    def select_save_path(default_name):
        root = Tk()
        root.withdraw()  # sembunyikan jendela utama
        root.attributes('-topmost', True)
        path = filedialog.asksaveasfilename(
            title="Simpan deck sebagai JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=default_name,
            initialdir=os.getcwd()
        )
        root.destroy()
        return path
    
    try:
        # load data deck
        cards = load_deck(deck_name)
        deck_data = {"cards": cards}
        
        # buka file explorer untuk memilih path
        default_filename = f"{deck_name}.json"
        save_path = select_save_path(default_filename)
        if not save_path:
            set_color(RED)
            print()
            print(center_text("Ekspor dibatalkan."))
            set_color(BRIGHT | YELLOW)
            print()
            wait_for_enter(center_text("Tekan Enter untuk kembali..."))
            set_color(WHITE)
            return
        
        # pastikan ekstensi .json
        if not save_path.lower().endswith('.json'):
            save_path += '.json'
        
        # simpan file
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(deck_data, f, indent=2, ensure_ascii=False)
        
        # sukses
        set_color(BRIGHT | GREEN)
        print()
        print(center_text("Ekspor berhasil!"))
        set_color(WHITE)
        print(center_text(f"File disimpan di: {save_path}"))
        print(center_text(f"Total kartu: {len(cards)}"))
        set_color(BRIGHT | YELLOW)
        print()
        set_color(BRIGHT | YELLOW)
        wait_for_enter(center_text("Tekan Enter untuk kembali..."))
        set_color(WHITE)
        
    except Exception as e:
        set_color(RED)
        print()
        print(center_text(f"Gagal mengekspor deck: {e}"))
        set_color(BRIGHT | YELLOW)
        print()
        wait_for_enter(center_text("Tekan Enter untuk kembali..."))
        set_color(WHITE)

#hapus deck
def remove_deck(deck_name):
    while True:
        set_color(BRIGHT | RED)
        print(center_text(f"=== Hapus Deck: {deck_name} ==="))
        set_color(WHITE)
        print()
        confirm = input("Apakah Anda yakin ingin menghapus deck ini? (y/n): ")
        if confirm.lower() == 'y':
            print()
            delete_deck(deck_name)
            print(center_text("Deck telah dihapus."))
            set_color(BRIGHT | YELLOW)
            wait_for_enter(center_text("Tekan Enter untuk kembali..."))
            set_color(WHITE)
            return True  
        else:
            print()
            print(center_text("Operasi dibatalkan."))
            set_color(BRIGHT | YELLOW)
            wait_for_enter(center_text("Tekan Enter untuk kembali..."))
            set_color(WHITE)
            return False 
                        
"""Manajemen Deck"""
def manage_deck(avail_decks):
    MAX_VISIBLE = 10
    if avail_decks is None:
        avail_decks = []

    if not monitor_terminal_size():
        return

    selected = 0
    top = 0
    prev_size = get_terminal_size()

    while True:
        avail_decks = sorted(load_index().get("decks", []))
        clear()
        set_color(BRIGHT | MAGENTA)
        print(center_text("================================== Manajemen Deck =================================="))
        print()
        set_color(BRIGHT | WHITE)
        print(center_text("ESC: Kembali | ↑/↓: Pilih | Enter: Kelola deck"))
        print()

        count = len(avail_decks)
        window = min(MAX_VISIBLE, count) if count > 0 else 1

        #keep selected visible
        if selected < top:
            top = selected
        if selected >= top + window:
            top = selected - window + 1

        #show deck
        if count == 0:
            set_color(BLUE)
            print(center_text("  (Belum ada deck)"))
            set_color(WHITE)
        else:
            for i in range(top, min(top + window, count)):
                name = avail_decks[i]
                if i == selected:
                    set_color(BRIGHT | GREEN)
                    print(center_text(f"> {name} <"))
                    set_color(WHITE)
                else:
                    print(center_text(f"  • {name}"))

        #hint if hidden
        hidden = max(0, count - window)
        if hidden > 0:
            print()
            set_color(BLUE)
            print(center_text(f"...dan {hidden} deck lainnya tidak ditampilkan (maks {MAX_VISIBLE})"))
            set_color(WHITE)

        #input key
        k, prev_size = wait_for_key_with_resize(prev_size)
        if k == EXIT_TOKEN:
            return
        if k is None:
            continue
        if k == 'UP':
            if selected > 0:
                selected -= 1
        elif k == 'DOWN':
            if selected < max(0, count - 1):
                selected += 1
        elif k == 'ESC':
            return  # back to main menu
        elif k == 'ENTER':
            if count == 0:
                set_color(RED)
                print()
                print(center_text("Tidak ada deck untuk dikelola. Tekan Enter untuk kembali..."))
                set_color(WHITE)
                wait_for_enter()
                return

            deck_name = avail_decks[selected]
            #submenu ketika sudah pilih deck
            opt_selected = 0
            while True:
                clear()
                set_color(BRIGHT | CYAN)
                print(center_text(f"=== Kelola Deck: {deck_name} ==="))
                print()
                set_color(WHITE)
                print(center_text("Gunakan ↑/↓ untuk pilih, Enter untuk konfirmasi, ESC untuk kembali"))
                print()

                #highlight ketika dipilih
                for idx, opt in enumerate(options):
                    if idx == opt_selected:
                        set_color(BRIGHT | GREEN)
                        print(center_text(f"> {idx+1}) {opt} <"))
                        set_color(WHITE)
                    else:
                        print(center_text(f"  {idx+1}) {opt}"))

                #input
                k, prev_size = wait_for_key_with_resize(prev_size)
                if k == EXIT_TOKEN:
                    return
                if k is None:
                    continue
                if k == 'UP':
                    if opt_selected > 0:
                        opt_selected -= 1
                elif k == 'DOWN':
                    if opt_selected < len(options) - 1:
                        opt_selected += 1
                elif k == 'ESC':
                    break  # kembali ke daftar deck
                elif k == 'ENTER':
                    choice = opt_selected + 1
                    clear()
                    if choice == 1:
                        deck_summary(deck_name)
                    if choice == 2:
                        card_edit(deck_name)
                    if choice == 3:
                        new_cards(deck_name)
                    if choice == 4:
                        card_info(deck_name)
                    if choice == 5:
                        card_list(deck_name)
                    if choice == 6:
                        reset_times(deck_name)
                    if choice == 7:
                        change_name_deck(deck_name)
                    if choice == 8:
                        export_deck(deck_name)
                    if choice == 9:
                        if remove_deck(deck_name):
                            break

                else:
                    continue