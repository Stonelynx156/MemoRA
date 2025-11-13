import os
import ctypes
import msvcrt
import shutil
import time

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

#check terminal size   
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
    
"""Panduan Penggunaan"""
def panduan_penggunaan():
    ensure_terminal_ok(min_cols=84, min_rows=20, enforce=False)
    set_color(BRIGHT | MAGENTA)
    print(center_text("=========================== Panduan Penggunaan Care Card ==========================="))
    print()
    set_color(BRIGHT | WHITE)
    print(center_text("Panduan singkat penggunaan aplikasi (Bahasa Indonesia)"))
    print()
    set_color(WHITE)

    indent = " " * 5

    # Section 1
    print(center_text("1) Navigasi utama"))
    print(indent + "- ↑ / ↓ : Pilih deck")
    print(indent + "- Tab   : Berpindah fokus antara daftar deck dan menu bawah")
    print(indent + "- ← / → : Navigasi opsi menu bawah")
    print(indent + "- Enter : Pilih / konfirmasi")
    print(indent + "- ESC   : Kembali / keluar")
    print()

    # Section 2
    print(center_text("2) Menu bawah"))
    print(indent + "- Panduan Penggunaan : Menampilkan panduan ini")
    print(indent + "- Buat Deck Baru     : Membuat deck baru (tekan ESC untuk batal)")
    print(indent + "- Import Deck        : Import file .json berisi deck")
    print(indent + "- Kelola Deck        : Masuk ke manajemen deck (lihat opsi di bawah)")
    print()

    # Section 3
    print(center_text("3) Kelola Deck (opsi saat memilih sebuah deck)"))
    print(indent + "- Ringkasan              : Melihat info singkat deck")
    print(indent + "- Tambah Kartu           : Menambah kartu (pertanyaan & jawaban)")
    print(indent + "- Informasi Kartu        : Lihat metadata kartu")
    print(indent + "- Reset Waktu Kartu      : Reset status/last_seen semua kartu")
    print(indent + "- Ganti Nama Deck        : Ubah nama deck (disimpan sebagai file .json)")
    print(indent + "- Ekspor (JSON)         : Simpan deck ke file .json lewat dialog")
    print(indent + "- Hapus Deck            : Hapus file deck (konfirmasi diperlukan)")
    print()

    # Section 4
    print(center_text("4) Format file import/export (.json)"))
    print(indent + "- File berupa objek JSON berisi minimal field:")
    print(indent + "  { \"name\": \"Nama Deck\", \"cards\": [ {\"q\":\"pertanyaan\",\"a\":\"jawaban\"}, ... ] }")
    print()

    # Section 5
    print(center_text("5) Tips & catatan"))
    print(indent + "- Pastikan ukuran terminal cukup besar agar tampilan rapi.")
    print(indent + "- Aplikasi mencoba mendeteksi Enter/ESC; gunakan keyboard fisik.")
    print(indent + "- Jika dialog file explorer muncul otomatis, itu karena modul import dipanggil.")
    print()
    set_color(YELLOW)
    wait_for_enter(center_text("Tekan Enter untuk kembali ke menu..."))

if __name__ == "__main__":
    panduan_penggunaan()
