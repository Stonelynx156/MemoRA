import os
import ctypes
import msvcrt
import shutil
import json
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
    while msvcrt.kbhit():
        try:
            msvcrt.getch()
        except OSError:
            break
    while True:
        key = msvcrt.getch()
        if key == b'\r':
            break
        if key in (b'\x00', b'\xe0'):
            try:
                msvcrt.getch()
            except OSError:
                pass
            continue

# simple key reader for arrows/esc/enter
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
    try:
        return ('CHAR', k.decode('utf-8', errors='ignore'))
    except Exception:
        return ('CHAR', '')

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

options = [
                "Ringkasan",
                "Edit Kartu",
                "Tambah Kartu",
                "Informasi Kartu",
                "Daftar Semua Kartu",
                "Reset Waktu Semua Kartu",
                "Ganti Nama Deck",
                "Ekspor (JSON)",
                "Hapus Deck"
            ]

"""Fungsi kelola deck"""
#deck summary
def deck_summary(deck_name):
    set_color(BRIGHT | CYAN)
    print(center_text(f"=== Ringkasan Deck: {deck_name} ==="))
    set_color(WHITE)
    print()
    print("     " + "Total Kartu        : ")
    print("     " + "Kartu baru         : ")
    print("     " + "kartu jatuh tempo  : ")
    print("     " + "Kartu tertunda     : ")
    print("     " + "Jadwal Terdekat    : ")
    print("     " + "Interval Rata Rata : ")
    print("     " + "Internal Terbesar  : ")
    print()
    wait_for_enter(center_text("Tekan Enter untuk kembali..."))

#tambah kartu baru
def newcards(deck_name):
    set_color(BRIGHT | CYAN)
    print(center_text(f"=== Membuat kartu di: {deck_name} ==="))
    set_color(WHITE)
    print()
    front_cards = input("Masukkan pertanyaan (front): ")
    if not front_cards.strip():
        set_color(RED)
        print()
        print(center_text("Pertanyaan tidak boleh kosong!"))
        set_color(WHITE)
        wait_for_enter(center_text("Tekan Enter untuk kembali..."))
        return
    back_cards = input("Masukkan jawaban (back)    : ")
    if not back_cards.strip():
        set_color(RED)
        print()
        print(center_text("Jawaban tidak boleh kosong!"))
        set_color(WHITE)
        wait_for_enter(center_text("Tekan Enter untuk kembali..."))
        return
    print()
    wait_for_enter(center_text("Tekan Enter untuk kembali..."))

#cek daftar kartu
def card_list(deck_name):
    set_color(BRIGHT | CYAN)
    print(center_text(f"=== Daftar Kartu di: {deck_name} ==="))
    set_color(WHITE)
    print()
    print("     " + "ID Kartu   | Pertanyaan (front) | Jawaban (back) ")
    print("     " + "-----------------------------------------------")
    print("     " + "1          | Apa itu Python?   | Bahasa pemrograman tingkat tinggi.")
    print("     " + "2          | Apa itu JSON?     | Format data ringan untuk pertukaran data.")
    print()
    wait_for_enter(center_text("Tekan Enter untuk kembali..."))

#cek informasi kartu
def card_info(deck_name):
    set_color(BRIGHT | CYAN)
    print(center_text(f"=== Informasi Kartu di: {deck_name} ==="))
    set_color(WHITE)
    print()
    card_id = input("Masukkan ID Kartu: ")
    if not card_id.isdigit():
        set_color(RED)
        print()
        print(center_text("ID Kartu tidak valid!"))
        set_color(WHITE)
        wait_for_enter(center_text("Tekan Enter untuk kembali..."))
        return
    print()
    print("     " + "Pertanyaan (front) : ")
    print("     " + "Jawaban (back)     : ")
    print("     " + "Level              : ")
    print("     " + "Interval           : ")
    print("     " + "EFactor            : ")
    print("     " + "Due Date           : ")
    print()
    wait_for_enter(center_text("Tekan Enter untuk kembali..."))

def card_edit(deck_name):
    set_color(BRIGHT | CYAN)
    print(center_text(f"=== Edit Kartu di: {deck_name} ==="))
    set_color(WHITE)
    print()
    card_id = input("Masukkan ID Kartu yang akan diedit: ")
    #validasi input ID kartu
    if not card_id.isdigit():
        set_color(RED)
        print()
        print(center_text("ID Kartu tidak valid!"))
        set_color(WHITE)
        wait_for_enter(center_text("Tekan Enter untuk kembali..."))
        return
    print()
    print("     " + "1) Edit Pertanyaan (front)")
    print("     " + "2) Edit Jawaban (back)")
    print("     " + "3) Hapus Kartu")
    print("     " + "4) Kembali")
    print()
    choice = input("Pilih opsi (1-4): ")
    if choice == '1':
        new_front   = input("Masukkan pertanyaan baru: ")
    elif choice == '2':
        new_back    = input("Masukkan jawaban baru   : ")
    elif choice == '3':
        confirm = input("Yakin hapus kartu ini? (y/n): ")
        if confirm.lower() == 'y':
            print()
            print(center_text("Kartu telah dihapus."))
        else:
            print()
            print(center_text("Operasi dibatalkan."))
    elif choice == '4':
        return
    elif choice not in ['1','2','3','4']:
        set_color(RED)
        print()
        print(center_text("Opsi tidak valid!"))
        set_color(WHITE)
        wait_for_enter(center_text("Tekan Enter untuk kembali..."))
        

def reset_times(deck_name):
    set_color(BRIGHT | CYAN)
    print(center_text(f"=== Reset Waktu Kartu di: {deck_name} ==="))
    set_color(WHITE)
    print()
    confirm = input("Apakah Anda yakin ingin mereset waktu semua kartu? (y/n): ")
    if confirm.lower() == 'y':
        print()
        print(center_text("Waktu semua kartu telah direset."))
    else:
        print()
        print(center_text("Operasi dibatalkan."))
    print()
    wait_for_enter(center_text("Tekan Enter untuk kembali..."))

def change_name_deck(deck_name):
    set_color(BRIGHT | CYAN)
    print(center_text(f"=== Ganti Nama Deck: {deck_name} ==="))
    set_color(WHITE)
    print()
    new_name = input("Masukkan nama deck baru: ")\
        
    print()
    print(center_text(f"Nama deck telah diubah menjadi: {new_name}"))
    print()
    wait_for_enter(center_text("Tekan Enter untuk kembali..."))

"""Manajemen Deck"""
def manage_deck(avail_decks):
    MAX_VISIBLE = 10
    if avail_decks is None:
        avail_decks = []

    selected = 0
    top = 0

    while True:
        check_terminal_size(min_cols=84, min_rows=20, enforce=False)
        ensure_terminal_ok(min_cols=84, min_rows=20, enforce=False)
        clear()
        set_color(BRIGHT | MAGENTA)
        print(center_text("================================== Manajemen Deck =================================="))
        print()
        set_color(BRIGHT | WHITE)
        print(center_text("ESC: Kembali | ↑/↓: Pilih | Enter: Kelola deck"))
        print()

        count = len(avail_decks)
        window = min(MAX_VISIBLE, count) if count > 0 else 1

        # keep selected visible
        if selected < top:
            top = selected
        if selected >= top + window:
            top = selected - window + 1

        # show visible decks
        if count == 0:
            set_color(BLUE)
            print(center_text("  (Belum ada deck)"))
            set_color(WHITE)
        else:
            for i in range(top, min(top + window, count)):
                name = avail_decks[i]
                if i == selected:
                    set_color(BRIGHT | GREEN)
                    print(center_text(f"> {name} <"))
                    set_color(WHITE)
                else:
                    print(center_text(f"  • {name}"))

        # hint if hidden
        hidden = max(0, count - window)
        if hidden > 0:
            print()
            set_color(BLUE)
            print(center_text(f"...dan {hidden} deck lainnya tidak ditampilkan (maks {MAX_VISIBLE})"))
            set_color(WHITE)

        # read key
        k = read_key()
        if k == 'UP':
            if selected > 0:
                selected -= 1
        elif k == 'DOWN':
            if selected < max(0, count - 1):
                selected += 1
        elif k == 'ESC':
            return  # back to main menu
        elif k == 'ENTER':
            if count == 0:
                set_color(RED)
                print()
                print(center_text("Tidak ada deck untuk dikelola. Tekan Enter untuk kembali..."))
                set_color(WHITE)
                wait_for_enter()
                continue
            # simple submenu placeholder (tidak langsung kembali)
            deck_name = avail_decks[selected]
            # submenu: pilih opsi dengan arrow ↑/↓ dan Enter untuk konfirmasi
            opt_selected = 0
            while True:
                clear()
                set_color(BRIGHT | CYAN)
                print(center_text(f"=== Kelola Deck: {deck_name} ==="))
                print()
                set_color(WHITE)
                print(center_text("Gunakan ↑/↓ untuk pilih, Enter untuk konfirmasi, ESC untuk kembali"))
                print()

                # tampilkan opsi dengan highlight pada opt_selected
                for idx, opt in enumerate(options):
                    if idx == opt_selected:
                        set_color(BRIGHT | GREEN)
                        print(center_text(f"> {idx+1}) {opt} <"))
                        set_color(WHITE)
                    else:
                        print(center_text(f"  {idx+1}) {opt}"))

                # baca input
                k = read_key()
                check_terminal_size(min_cols=84, min_rows=20, enforce=False)
                ensure_terminal_ok(min_cols=84, min_rows=20, enforce=False)
                if k == 'UP':
                    if opt_selected > 0:
                        opt_selected -= 1
                elif k == 'DOWN':
                    if opt_selected < len(options) - 1:
                        opt_selected += 1
                elif k == 'ESC':
                    break  # kembali ke daftar deck
                elif k == 'ENTER':
                    choice = opt_selected + 1
                    clear()
                    ensure_terminal_ok(min_cols=84, min_rows=20, enforce=False)
                    if choice == 1:
                        deck_summary(deck_name)
                    if choice == 2:
                        card_edit(deck_name)
                    if choice == 3:
                        newcards(deck_name)
                    if choice == 4:
                        card_info(deck_name)
                    if choice == 5:
                        card_list(deck_name)
                    if choice == 6:
                        reset_times(deck_name)
                    if choice == 7:
                        change_name_deck(deck_name)
                    if choice == 8:
                        set_color(BRIGHT | CYAN)
                        print(center_text(f"=== Ekspor Deck: {deck_name} ==="))
                        set_color(WHITE)
                        print()
                        print(center_text("Fitur ekspor akan segera tersedia..."))
                        print()
                        wait_for_enter(center_text("Tekan Enter untuk kembali..."))
                    if choice == 9:
                        set_color(BRIGHT | RED)
                        print(center_text(f"=== Hapus Deck: {deck_name} ==="))
                        set_color(WHITE)
                        print()
                        confirm = input("Apakah Anda yakin ingin menghapus deck ini? (y/n): ")
                        if confirm.lower() == 'y':
                            print()
                            print(center_text("Deck telah dihapus."))
                            #hapus deck disini
                            wait_for_enter(center_text("Tekan Enter untuk kembali..."))
                            break  # kembali ke daftar deck setelah hapus
                        else:
                            print()
                            print(center_text("Operasi dibatalkan."))
                            wait_for_enter(center_text("Tekan Enter untuk kembali..."))

                else:
                    # ignore other keys
                    continue