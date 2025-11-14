import os
import ctypes
import msvcrt
import shutil
import guide
import newdeck
import importdeck
import managedeck
import time

from deck import load_index
from console import (
    clear, 
    set_color,
    center_text,
    wait_for_enter,
    read_key,
    get_terminal_size,
    monitor_terminal_size)

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

#Bottom Menu
menu_options = [
        "Panduan Penggunaan",
        "Buat Deck Baru",
        "Import Deck",
        "Kelola Deck"
    ]

"""Menu Utama"""
def main_menu(selected_deck, selected_option, deck_mode):
    clear()
    cols, rows = get_terminal_size()
    avail_decks = sorted(load_index().get("decks", []))

    # title 
    header = "================================== Care Card V.1 =================================="
    set_color(BRIGHT | MAGENTA)
    print(center_text(header))
    print()
    lines_used = 2  # header + blank

    #deck menu (tampil di bagian atas)
    if avail_decks:
        for i, deck in enumerate (avail_decks):
            if deck_mode and i == selected_deck:
                set_color(BRIGHT | GREEN)
                deck_text = f"> {deck} <"
                print("               " + (deck_text))
                set_color(WHITE)
            else:
                set_color(WHITE)
                deck_text = f"  • {deck}"
                print("               " + (deck_text))
            lines_used += 1
    else:
        no_deck_text = "  (Belum ada deck)"
        set_color(BLUE)
        print(center_text(no_deck_text))
        set_color(WHITE)
        lines_used += 1

    #spacer sebelum menu bawah
    bottom_menu_height = 6

    blanks_needed = max(0, rows - lines_used - bottom_menu_height)
    for _ in range(blanks_needed):
        print()

    set_color(BRIGHT | CYAN)
    option_menu_header = "Menu:"
    print(center_text(option_menu_header))
    print()
    set_color(WHITE)

    menu_items_reversed = list(reversed(menu_options))
    menu_texts = []
    
    #menu text highlight
    for i, option in enumerate(menu_items_reversed):
        original_index = len(menu_options) - 1 - i
        if not deck_mode and original_index == selected_option:
            menu_texts.append(f"[> {option} <]")
        else:
            menu_texts.append(f"[  {option}  ]")
    
    #center options
    total_length = sum(len(text) for text in menu_texts) + (len(menu_texts) - 1) * 2
    cols, _ = shutil.get_terminal_size()
    x = (cols - total_length) // 2

    print(" " * x, end="")
    for i, text in enumerate(menu_texts):
        print(text, end="")
        if i < len(menu_texts) - 1:
            print("  ", end="")
    print()
    print()

    #print instruksi
    set_color(BRIGHT | YELLOW)
    if deck_mode:
        instruction = "↑/↓: Pilih Deck | Tab: Pindah ke Menu | Enter: Buka Deck | ESC: Keluar"
    else:
        instruction = "←/→: Navigasi Menu | Tab: Pindah ke Deck | Enter: Pilih Menu | ESC: Keluar"
    print(center_text(instruction))
    set_color(WHITE)

"""Fungsi utama untuk menjalankan menu."""
def show_menu():
    selected_deck = 0
    selected_option = 0
    deck_mode = True
    prev_size = shutil.get_terminal_size()
    
    while True:
        #loop cek terminal
        # cek ukuran terminal
        if not monitor_terminal_size():
            return
        
        cols, rows = get_terminal_size()
        
        # redraw jika ukuran berubah
        if (cols, rows) != prev_size:
            prev_size = (cols, rows)
        
        main_menu(selected_deck, selected_option, deck_mode)

        # tunggu input
        key = None
        while True:
            if msvcrt.kbhit():
                key = read_key()
                break
            
            cols_now, rows_now = get_terminal_size()
            if (cols_now, rows_now) != prev_size:
                break
            
            time.sleep(0.1)

        # jika ukuran berubah, kembali ke loop utama
        if (cols_now, rows_now) != prev_size:
            continue

        # jika tidak ada input, lanjut polling
        if key is None:
            continue
        #loop selesai

        # proses input
        avail_decks = sorted(load_index().get("decks", []))

        if key == 'UP':
            if deck_mode and avail_decks:
                selected_deck = (selected_deck - 1) % len(avail_decks)
        elif key == 'DOWN':
            if deck_mode and avail_decks:
                selected_deck = (selected_deck + 1) % len(avail_decks)
        elif key == 'LEFT':
            if not deck_mode:
                selected_option = (selected_option + 1) % len(menu_options)
        elif key == 'RIGHT':
            if not deck_mode:
                selected_option = (selected_option - 1) % len(menu_options)
        elif key == 'TAB':
            deck_mode = not deck_mode
        elif key == 'ENTER':
            clear()
            if deck_mode and avail_decks:
                set_color(BRIGHT | BLUE)
                print(center_text(f"=== {avail_decks[selected_deck]} ==="))
                set_color(WHITE)
                print("     " + "Kartu Baru        : ")
                print("     " + "Kartu Tinjauan    : ")
                print("     " + "Kartu jatuh Tempo : ")

                print(center_text("Tekan Enter untuk Review Kartu atau ESC untuk kembali ke Menu Utama."))
                if key == 'ENTER':
                    print("Fitur Review akan segera hadir!")
                if key == 'ESC':
                    continue
                wait_for_enter()

            elif not deck_mode:
                opt = menu_options[selected_option]
                if opt == "Buat Deck Baru":
                    clear()
                    newdeck.new_deck()
                elif opt == "Import Deck":
                    clear()
                    importdeck.import_deck()
                elif opt == "Kelola Deck":
                    clear()
                    managedeck.manage_deck(avail_decks)
                elif opt == "Panduan Penggunaan":
                    clear()
                    guide.panduan_penggunaan()
                    print()
        elif key == 'ESC':
            clear()
            set_color(BRIGHT | YELLOW)
            print(center_text("Terima Kasih telah menggunakan Care Card!"))
            set_color(WHITE)
            break
