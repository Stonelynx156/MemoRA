import os
import ctypes
import msvcrt
import shutil
import time
import sys
from utils.deck import load_index

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
    if k == b' ':
        return 'SPASI'
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

#fungsi cek ukuran terminal
def get_terminal_size():
    cols, rows = shutil.get_terminal_size()
    return cols, rows

min_cols = 85
min_rows = 20

def monitor_terminal_size():
    """Loop cek ukuran terminal. Return saat ukuran OK atau ESC ditekan."""
    while True:
        cols, rows = shutil.get_terminal_size()
        if cols >= min_cols and rows >= min_rows:
            return True
        
        clear()
        set_color(BRIGHT | RED)
        print(center_text(f"Ukuran terminal terlalu kecil: {cols}x{rows} (minimal {min_cols}x{min_rows})"))
        set_color(BRIGHT | YELLOW)
        print(center_text("Beberapa tampilan mungkin terpotong."))
        print(center_text("Perbesar terminal atau tekan ESC untuk keluar."))
        set_color(WHITE)
        
        if msvcrt.kbhit():
            k = read_key()
            if k == 'ESC':
                clear()
                set_color(BRIGHT | YELLOW)
                print(center_text("Terima Kasih telah menggunakan MemoRA!"))
                set_color(WHITE)
                return False
        
        time.sleep(0.5)

EXIT_TOKEN = "__EXIT__"

def wait_for_key_with_resize(prev_size):
    while True:
        if msvcrt.kbhit():
            return read_key(), prev_size

        cols_now, rows_now = get_terminal_size()
        if cols_now < min_cols or rows_now < min_rows:
            if not monitor_terminal_size():
                return EXIT_TOKEN, prev_size
            cols_now, rows_now = get_terminal_size()
            prev_size = (cols_now, rows_now)
            return None, prev_size

        if (cols_now, rows_now) != prev_size:
            return None, (cols_now, rows_now)

        time.sleep(0.1)

def print_spacer_before_bottom_options(lines_used, bottom_section_height):
    _, rows = get_terminal_size()
    blanks_needed = max(0, rows - lines_used - bottom_section_height)
    
    for _ in range(blanks_needed):
        print()

def input_with_esc(prompt=""):
        
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