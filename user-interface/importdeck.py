from nt import get_terminal_size
import os
import ctypes
import json
import shutil
from deck import DATA_DIR, _ensure_index, load_index, save_index
from pathlib import Path
from tkinter import Tk, filedialog

from console import (
    set_color,
    center_text,
    wait_for_enter,
    )

EXIT_TOKEN = "__EXIT__"

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

"""Import Deck Baru"""
def import_deck():
    while True:
        set_color(BRIGHT | CYAN)
        print(center_text("================================= Import Deck Baru ================================="))

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
            print()
            print(center_text("Tidak ada file dipilih."))
            set_color(BRIGHT | YELLOW)
            print()
            wait_for_enter(center_text("Tekan Enter untuk kembali..."))
            set_color(WHITE)
            return None

        # pastikan ekstensi .json
        if not file_path.lower().endswith('.json'):
            set_color(RED)
            print()
            print(center_text("File bukan format .json"))
            set_color(BRIGHT | YELLOW)
            print()
            wait_for_enter(center_text("Tekan Enter untuk kembali..."))
            set_color(WHITE)
            return None

        # coba baca dan parse JSON
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # ambil nama deck dari nama file
            name = os.path.splitext(os.path.basename(file_path))[0]
            
            # cek apakah nama deck sudah ada
            index = load_index()
            decks = index.setdefault("decks", [])
            
            if name in decks:
                # tampilkan peringatan jika deck sudah ada
                set_color(BRIGHT | YELLOW)
                print()
                print(center_text(f"Peringatan: Deck dengan nama '{name}' sudah ada!"))
                set_color(WHITE)
                print()
                print(center_text("Apakah Anda ingin mengganti deck yang sudah ada?"))
                print()
                overwrite = input(center_text("Lanjutkan? (y/n): ")).strip().lower()
                
                if overwrite != 'y':
                    set_color(RED)
                    print()
                    print(center_text("Import dibatalkan."))
                    set_color(BRIGHT | YELLOW)
                    print()
                    wait_for_enter(center_text("Tekan Enter untuk kembali..."))
                    set_color(WHITE)
                    return None
            
            # copy file dan update index
            shutil.copy(file_path, DATA_DIR)
            if name not in decks:
                decks.append(name)
                save_index(index)
        except Exception as e:
            set_color(RED)
            print()
            print(center_text(f"Gagal membaca/parse JSON: {e}"))
            set_color(BRIGHT | YELLOW)
            wait_for_enter(center_text("Tekan Enter untuk kembali..."))
            set_color(WHITE)
            return None

        # sukses - tampilkan ringkasan singkat
        set_color(BRIGHT | GREEN)
        print()
        print(center_text("Import berhasil!"))
        set_color(WHITE)
        print(center_text(f"File: {os.path.basename(file_path)}"))
        set_color(BRIGHT | YELLOW)
        print()
        wait_for_enter(center_text("Tekan Enter untuk kembali ke menu..."))
        set_color(WHITE)

        return data
