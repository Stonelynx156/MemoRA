import os
import ctypes
import msvcrt
import shutil
import json
from tkinter import Tk, filedialog

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

"""Import Deck Baru"""
def import_deck():
    set_color(BRIGHT | CYAN)
    print(center_text("==================================== Import Deck Baru ===================================="))

    # buka file explorer untuk memilih file .json
    def select_json_file():
        root = Tk()
        root.withdraw()              # sembunyikan jendela utama
        root.attributes('-topmost', True)
        path = filedialog.askopenfilename(
            title="Pilih file JSON untuk import",
            filetypes=[("JSON files", "*.json")],
            initialdir=os.getcwd()
        )
        root.destroy()
        return path

    file_path = select_json_file()
    if not file_path:
        set_color(RED)
        print(center_text("Tidak ada file dipilih."))
        set_color(WHITE)
        wait_for_enter(center_text("Tekan Enter untuk kembali..."))
        return None

    # pastikan ekstensi .json
    if not file_path.lower().endswith('.json'):
        set_color(RED)
        print(center_text("File bukan format .json"))
        set_color(WHITE)
        wait_for_enter(center_text("Tekan Enter untuk kembali..."))
        return None

    # coba baca dan parse JSON
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        set_color(RED)
        print(center_text(f"Gagal membaca/parse JSON: {e}"))
        set_color(WHITE)
        wait_for_enter(center_text("Tekan Enter untuk kembali..."))
        return None

    # sukses - tampilkan ringkasan singkat
    set_color(BRIGHT | GREEN)
    print(center_text("Import berhasil!"))
    set_color(WHITE)
    print(center_text(f"File: {os.path.basename(file_path)}"))
    print()
    wait_for_enter(center_text("Tekan Enter untuk kembali ke menu..."))

    return data
