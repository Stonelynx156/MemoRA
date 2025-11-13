import os
import ctypes
import msvcrt
import shutil
import panduan
import sys
from deck import create_deck, load_index

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

"""Deck Baru"""
def new_deck():
    """
    Tampilkan form pembuatan deck.
    Mengembalikan nama deck (str) bila dibuat, None bila dibatalkan (ESC).
    """
    clear()
    set_color(BRIGHT | MAGENTA)
    print(center_text("======================================== Buat Deck Baru ========================================"))
    print()

    set_color(BRIGHT | WHITE)
    print(center_text("Tekan ESC untuk kembali ke menu..."))
    print()

    def input_with_esc(prompt=""):
        """
        Baca input dari pengguna, menangkap ESC untuk membatalkan.
        Mengembalikan (value_str, canceled_bool).
        """
        sys.stdout.write(prompt)
        sys.stdout.flush()
        buf = ""
        while True:
            ch = msvcrt.getwch()  # baca karakter sebagai str
            if ch == '\r':  # Enter
                sys.stdout.write("\n")
                return buf, False
            if ch == '\x1b':  # ESC
                sys.stdout.write("\n")
                return None, True
            if ch == '\x08':  # Backspace
                if buf:
                    buf = buf[:-1]
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
                continue
            # tampilkan karakter biasa
            buf += ch
            sys.stdout.write(ch)
            sys.stdout.flush()

    # gunakan prompt sederhana (tidak di-center supaya input terlihat normal)
    deck_name, canceled = input_with_esc(center_text("Masukkan nama deck baru: "))
    existing_decks = sorted(load_index().get("decks", []))
    if canceled:
        # kembali ke pemanggil (main menu) tanpa memanggil show_menu di sini
        return None
    
    if deck_name is None or deck_name.strip() == "":
        set_color(BRIGHT | RED)
        print(center_text("Nama deck tidak boleh kosong!"))
        set_color(WHITE)
        wait_for_enter(center_text("Tekan Enter untuk kembali ke menu..."))
        return None
    if deck_name in existing_decks:
        set_color(BRIGHT | RED)
        print()
        print(center_text(f"Deck dengan nama '{deck_name}' sudah ada!"))
        set_color(WHITE)
        wait_for_enter(center_text("Tekan Enter untuk kembali ke menu..."))
        return None

    # Di sini Anda dapat menambahkan logika menyimpan deck ke file / daftar
    create_deck(deck_name)
    set_color(BRIGHT | CYAN)
    print()
    print(center_text(f"Deck '{deck_name}' berhasil dibuat!"))
    set_color(WHITE)
    print()
    wait_for_enter(center_text("Tekan Enter untuk kembali ke menu..."))
    
