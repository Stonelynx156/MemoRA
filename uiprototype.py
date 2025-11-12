from curses import keyname
from dis import Instruction
from operator import truediv
import os
import ctypes
import msvcrt
from pydoc import text
import shutil
from webbrowser import get

from ui import menu_options

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

"""Fungsi Penting"""
#Import Size Terminal
cols, rows = shutil.get_terminal_size()

#Clear Tampilan
def clear():
    os.system('cls')

#Ganti Warna
def set_color(color):
    ctypes.windll.kernel32.SetConsoleTextAttribute(h, color)

#Align Center
def center_text(text):
    x = (cols - len(text)) // 2
    return " " * x + text

#Get Available Deck
avail_decks = [
    ["ID", "Nama", "Skor"],
    [1, "Alice", 90],
    [2, "Bob", 85],
    [3, "Charlie", 95],
]

#Bottom Menu
menu_options = [
        "Buat Deck Baru",
        "Import Deck",
        "Kelola Deck"
    ]

"""Menu Utama"""
def main_menu(selected_deck, selected_option, deck_mode):
    clear()

    #title
    header = "============================================= Care Card V.1 =============================================="
    set_color(BRIGHT | MAGENTA)
    print (center_text(header))
    print()

    #deck menu
    if avail_decks:
        for i, deck in enumerate (avail_decks):
            if deck_mode and i == selected_deck:
                set_color(BRIGHT | GREEN)
                deck_text = f"> {deck} <"
                print(center_text(deck_text))
                set_color(WHITE)
    else:
        no_deck_text = "  (Belum ada deck)"
        set_color(BLUE)
        print(center_text(no_deck_text))
        set_color(WHITE)

    #menu bawah
    set_color(BRIGHT | CYAN)
    option_menu_header = "Menu:"
    print(center_text(option_menu_header))
    print()
    set_color(WHITE)

    #menu horizontal
    menu_items_reversed = list(reversed(menu_options))

    #total lenght center
    menu_text = []
    for i, option in enumerate(menu_items_reversed):
        original_index = len(menu_options) - 1 - i
        if not deck_mode and original_index == selected_option:
            menu_text.append(f"[> {option} <]")
        else:
            menu_text.append(f"[  {option}  ]")

    total_lenght = sum(len(text) for text in menu_text) + (len(menu_text) - 1 ) * 2
    x = (cols - total_lenght) // 2
    
    #print 
    print (" " * x, end="")
    for i, (text, option) in enumerate (zip(menu_text, menu_items_reversed)):
        original_index = len(menu_options) - 1 - i
        if not deck_mode and original_index == selected_option:
            set_color (BRIGHT | GREEN)
            print(text, end="")
            set_color (WHITE)
        if i < len(menu_text) - 1:
            print("  ", end="")
    print()
    print()

    #instruksi key
    set_color(BRIGHT | YELLOW)
    if deck_mode:
        Instruction = "↑/↓: Pilih Deck | Tab: Pindah ke Menu | Enter: Buka Deck | ESC: Keluar"
    else:
        instruction = "←/→: Navigasi Menu | Tab: Pindah ke Deck | Enter: Pilih Menu | ESC: Keluar"
    print(center_text(instruction))
    set_color(WHITE)

def show_menu():
    """Menampilkan dan menjalankan menu"""
    selected_deck = 0
    selected_option = 0
    deck_mode = True # True = deck, False = menu

    while True:
        show_menu(selected_deck,selected_option,deck_mode)

        #input keyboard 
        key = msvcrt.getch()

        #arrow keys
        if key == b'\xe0'

        

