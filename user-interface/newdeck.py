import os
import ctypes
import msvcrt
import shutil
from deck import create_deck, load_index
from console import (
    clear, 
    set_color,
    center_text,
    input_with_esc,
    wait_for_enter,
)

"""Material & Needs"""
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

"""Deck Baru"""
def new_deck():
    """
    Tampilkan form pembuatan deck.
    Mengembalikan nama deck (str) bila dibuat, None bila dibatalkan (ESC).
    """
    clear()
    set_color(BRIGHT | MAGENTA)
    print(center_text("================================== Buat Deck Baru =================================="))
    print()

    set_color(BRIGHT | YELLOW)
    print(center_text("Tekan ESC untuk kembali ke menu..."))
    set_color(WHITE)
    print()

    deck_name, canceled = input_with_esc(center_text("Masukkan nama deck baru: "))
    existing_decks = sorted(load_index().get("decks", []))
    if canceled:
        return None
    
    if deck_name is None or deck_name.strip() == "":
        set_color(BRIGHT | RED)
        print(center_text("Nama deck tidak boleh kosong!"))
        print()
        set_color(BRIGHT | YELLOW)
        wait_for_enter(center_text("Tekan Enter untuk kembali ke menu..."))
        set_color(WHITE)
        return None
    if deck_name in existing_decks:
        set_color(BRIGHT | RED)
        print(center_text(f"Deck dengan nama '{deck_name}' sudah ada!"))
        print()
        set_color(BRIGHT | YELLOW)
        wait_for_enter(center_text("Tekan Enter untuk kembali ke menu..."))
        set_color(WHITE)
        return None

    create_deck(deck_name)
    set_color(BRIGHT | CYAN)
    print(center_text(f"Deck '{deck_name}' berhasil dibuat!"))
    set_color(WHITE)
    print()
    set_color(BRIGHT | YELLOW)
    wait_for_enter(center_text("Tekan Enter untuk kembali ke menu..."))
    set_color(WHITE)
