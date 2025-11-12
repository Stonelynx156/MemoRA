import os
import ctypes
import msvcrt
import shutil
import panduan
import newdeck
import importdeck

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

#Get Available Deck
avail_decks = [
    "English to Indonesian",
    "Matematika Dasar",
    "Sejarah Dasar",
]

#Bottom Menu
menu_options = [
        "Panduan Penggunaan",
        "Buat Deck Baru",
        "Import Deck",
        "Kelola Deck"
    ]

"""Menu Utama"""
def main_menu(selected_deck, selected_option, deck_mode):
    clear()

    # ambil ukuran terminal saat ini
    cols, rows = shutil.get_terminal_size()

    #title
    header = "============================================= Care Card V.1 =============================================="
    set_color(BRIGHT | MAGENTA)
    print (center_text(header))
    print()
    lines_used = 2  # header + blank

    #deck menu (tampil di bagian atas)
    if avail_decks:
        for i, deck in enumerate (avail_decks):
            if deck_mode and i == selected_deck:
                set_color(BRIGHT | GREEN)
                deck_text = f"> {deck} <"
                print(center_text(deck_text))
                set_color(WHITE)
            else:
                set_color(WHITE)
                deck_text = f"  • {deck}"
                print(center_text(deck_text))
            lines_used += 1
    else:
        no_deck_text = "  (Belum ada deck)"
        set_color(BLUE)
        print(center_text(no_deck_text))
        set_color(WHITE)
        lines_used += 1

    # --- siapkan blok menu bawah yang akan di-"anchor" ke bawah ---
    # hitung tinggi blok menu bawah (header, blank, opsi bar, blank, instruksi)
    bottom_menu_height = 6

    # sisipkan blank lines agar menu bawah muncul di bagian bawah terminal
    blanks_needed = max(0, rows - lines_used - bottom_menu_height)
    for _ in range(blanks_needed):
        print()
    # sekarang cetak menu bawah (tetap berada di bawah)
    set_color(BRIGHT | CYAN)
    option_menu_header = "Menu:"
    print(center_text(option_menu_header))
    print()
    set_color(WHITE)

    #option (tetap sama, tapi dicetak setelah blank untuk anchoring)
    menu_items_reversed = list(reversed(menu_options))
    menu_texts = []
    
    # Buat menu texts dengan format yang benar
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
    selected_deck = 0
    selected_option = 0
    deck_mode = True  # True = navigasi di deck, False = navigasi di menu

    while True:
        main_menu(selected_deck, selected_option, deck_mode)
        
        #input keyboard
        key = msvcrt.getch()

        #arrow keys
        if key == b'\xe0':
            key = msvcrt.getch()
            if key == b'H': #arrow atas
                if deck_mode and avail_decks:
                    selected_deck = (selected_deck - 1) % len(avail_decks)
            elif key == b'P': #arrow bawah
                if deck_mode and avail_decks:
                    selected_deck = (selected_deck + 1) % len(avail_decks)
            elif key == b'K': #arrow kiri
                if not deck_mode:
                    selected_option = (selected_option + 1) % len(menu_options)
            elif key == b'M': #arrow kanan
                if not deck_mode:
                    selected_option = (selected_option - 1) % len(menu_options)
        elif key == b'\t': #tab pindah mode
            deck_mode = not deck_mode
        elif key == b'\r': #enter
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
                #memilih menu opsi
                set_color(BRIGHT | GREEN)
                print(center_text(f"Kamu memilih: {menu_options[selected_option]}"))
                set_color(WHITE)
                print()

                #act 
                if menu_options[selected_option] == "Buat Deck Baru":
                    clear()
                    newdeck.new_deck()
                elif menu_options[selected_option] == "Import Deck":
                    clear()
                    importdeck.import_deck()
                elif menu_options[selected_option] == "Kelola Deck":
                    print(center_text("Fitur Kelola Deck akan segera tersedia..."))
                    print()
                    wait_for_enter(center_text("Tekan Enter untuk kembali ke menu..."))
                elif menu_options[selected_option] == "Panduan Penggunaan":
                    clear()
                    panduan.panduan_penggunaan()
                    print()
                    wait_for_enter(center_text("Tekan Enter untuk kembali ke menu..."))
            
        elif key == b'\x1b': #ESC
            clear()
            set_color(BRIGHT | YELLOW)
            print(center_text("Terima Kasih telah menggunakan Care Card!"))
            set_color(WHITE)
            break

show_menu()



