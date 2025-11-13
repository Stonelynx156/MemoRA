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
    cols, _ = shutil.get_terminal_size()
    x = (cols - len(text)) // 2
    return " " * x + text

# baca input keyboard menjadi token terpusat (UP/DOWN/LEFT/RIGHT/ENTER/ESC/TAB/'CHAR')
def read_key():
    k = msvcrt.getch()
    if k in (b'\x00', b'\xe0'):
        k2 = msvcrt.getch()
        if k2 == b'H':
            return 'UP'
        if k2 == b'P':
            return 'DOWN'
        if k2 == b'K':
            return 'LEFT'
        if k2 == b'M':
            return 'RIGHT'
        return 'OTHER'
    if k == b'\r':
        return 'ENTER'
    if k == b'\x1b':
        return 'ESC'
    if k == b'\t':
        return 'TAB'
    try:
        return ('CHAR', k.decode('utf-8', errors='ignore'))
    except Exception:
        return ('CHAR', '')

# Tunggu hanya tombol Enter (isolasi input)
def wait_for_enter(prompt=None):
    if prompt:
        print(prompt)
    # buang semua input yang tertinggal
    while msvcrt.kbhit():
        try:
            msvcrt.getch()
        except OSError:
            break
    # tunggu hingga Enter (CR) ditekan
    while True:
        key = msvcrt.getch()
        if key == b'\r':  # Enter
            break
        # jika key adalah prefix untuk key spesial, buang byte berikutnya
        if key in (b'\x00', b'\xe0'):
            try:
                msvcrt.getch()
            except OSError:
                pass
            continue
        # selain itu, abaikan dan terus tunggu

#Get Available Deck


#Bottom Menu
menu_options = [
        "Panduan Penggunaan",
        "Buat Deck Baru",
        "Import Deck",
        "Kelola Deck"
    ]

#fungsi cek ukuran terminal
def check_terminal_size(min_cols=84, min_rows=20, enforce=False):
    """Periksa ukuran terminal; tampilkan peringatan bila kurang."""
    cols, rows = shutil.get_terminal_size()
    if cols >= min_cols and rows >= min_rows:
        return True
    
    clear()
    set_color(RED)
    print(center_text(f"Ukuran terminal terlalu kecil: {cols}x{rows} (minimal {min_cols}x{min_rows})"))
    set_color(YELLOW)
    print(center_text("Beberapa tampilan mungkin terpotong. Perbesar untuk melanjutkan penggunaan."))
    set_color(WHITE)
    wait_for_enter(center_text("Tekan Enter untuk mencoba lagi..."))
    clear()
    return False

def ensure_terminal_ok(min_cols=84, min_rows=20, enforce=False):
    while True:
        if check_terminal_size(min_cols=min_cols, min_rows=min_rows, enforce=enforce):
            return True
        else:
            clear()
        time.sleep(0.05)

"""Menu Utama"""
def main_menu(selected_deck, selected_option, deck_mode):
    clear()
    cols, rows = shutil.get_terminal_size()
    avail_decks = sorted(load_index().get("decks", []))

    # title 
    header = "================================== Care Card V.1 =================================="
    set_color(BRIGHT | MAGENTA)
    print(center_text(header))
    print()
    lines_used = 2  # header + blank

    check_terminal_size(min_cols=84, min_rows=20, enforce=False)
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
    avail_decks = sorted(load_index().get("decks", []))
    selected_deck = 0
    selected_option = 0
    deck_mode = True  # True = navigasi di deck, False = navigasi di menu

    # loop utama — pastikan terminal ok setiap frame dan juga sebelum menjalankan aksi
    while True:
        # pastikan ukuran terminal terpenuhi sebelum merender frame
        ensure_terminal_ok(min_cols=84, min_rows=20, enforce=False)
        main_menu(selected_deck, selected_option, deck_mode)
        
        # gunakan read_key() yang terpusat
        key = read_key()

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
            # pastikan ukuran terminal masih terpenuhi sebelum masuk ke aksi/submenu
            ensure_terminal_ok(min_cols=84, min_rows=20, enforce=False)
            clear()
            if deck_mode and avail_decks:
                #memilih deck
                set_color(BRIGHT | GREEN)
                print(center_text(f"Kamu memilih deck: {avail_decks[selected_deck]}"))
                set_color(WHITE)
                print()
                print(center_text("Fitur membuka deck akan segera tersedia..."))
                print()
                wait_for_enter(center_text("Tekan Enter untuk kembali ke menu..."))
            else:
                #act 
                # sebelum tiap aksi/submenu pastikan terminal tetap OK
                if menu_options[selected_option] == "Buat Deck Baru":
                    ensure_terminal_ok(min_cols=84, min_rows=20, enforce=False)
                    clear()
                    newdeck.new_deck()
                elif menu_options[selected_option] == "Import Deck":
                    ensure_terminal_ok(min_cols=84, min_rows=20, enforce=False)
                    clear()
                    importdeck.import_deck()
                elif menu_options[selected_option] == "Kelola Deck":
                    ensure_terminal_ok(min_cols=84, min_rows=20, enforce=False)
                    clear()
                    managedeck.manage_deck(avail_decks)
                elif menu_options[selected_option] == "Panduan Penggunaan":
                    ensure_terminal_ok(min_cols=84, min_rows=20, enforce=False)
                    clear()
                    guide.panduan_penggunaan()
                    print()
        elif key == 'ESC':
            clear()
            set_color(BRIGHT | YELLOW)
            print(center_text("Terima Kasih telah menggunakan Care Card!"))
            set_color(WHITE)
            break
