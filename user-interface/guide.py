import ctypes

from console import (
    set_color,
    center_text,
    wait_for_enter,
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
    
"""Panduan Penggunaan"""
def panduan_penggunaan():
    set_color(BRIGHT | MAGENTA)
    print(center_text("=========================== Panduan Penggunaan MemoRA ==========================="))
    print()
    set_color(BRIGHT | WHITE)
    print(center_text("Panduan singkat penggunaan aplikasi (Bahasa Indonesia)"))
    print()
    set_color(WHITE)

    indent = " " * 5

    set_color(RED)
    print(center_text("User Interface"))
    set_color(WHITE)
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

    set_color(RED)
    print(center_text("Cara Belajar"))
    set_color(WHITE)

    print(indent + "1. Pastikan sudah mempunyai deck dan kartu yang tersedia")
    print(indent + "2. Pilih deck yang aktif (Memiliki kartu baru & kartu jatuh tempo) ")
    print(indent + "3. Mulai sesi belajar dengan menekan enter")
    print(indent + "4. Pertanyaan dari 1 kartu akan muncul, coba jawab pertanyaan yang ada")
    print(indent + "5. Apabila sudah menjawab, tekan enter dan lihat jawabannya")
    print(indent + "6. Pilih kemudahan (1-4), pilih sesuai dengan kemampuan dan perasaan dalam menjawab")
    print(indent + "7. Kartu akan berganti ke kartu selanjutnya")

    print("Catatan")

    print(indent + "Sesi bisa diberhentikan oleh pengguna dengan menggunakan tmobol ESC")
    print(indent + "Sesi Review akan selesai apabila semua kartu sudah dirasa mudah (Pilihan 4 ke semua kartu)")
    print(indent + "Jumlah kartu baru bisa diatur di menu kelola deck")
    print(indent + "Kartu lama yang sudah direview akan muncul kembali apabila sudah jatuh tempo")

    set_color(BRIGHT | YELLOW)
    print()
    wait_for_enter(center_text("Tekan Enter untuk kembali ke menu..."))

if __name__ == "__main__":
    panduan_penggunaan()
