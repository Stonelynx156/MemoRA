import os
import ctypes
import msvcrt
import shutil

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

# Enable ANSI escape sequences di Windows (untuk clear() yang lebih efisien)
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
kernel32 = ctypes.windll.kernel32
mode = ctypes.c_ulong()
kernel32.GetConsoleMode(h, ctypes.byref(mode))
mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
kernel32.SetConsoleMode(h, mode)

#Import Size Terminal
cols, rows = shutil.get_terminal_size()

def clear():
    """Bersihkan layar menggunakan ANSI escape codes (lebih efisien)."""
    print('\033[2J\033[H', end='', flush=True)

def set_color(color):
    """Ubah warna teks di console."""
    ctypes.windll.kernel32.SetConsoleTextAttribute(h, color)

def center_text(text):
    """Mengembalikan teks yang sudah di-center."""
    x = (cols - len(text)) // 2
    return " " * x + text

# Daftar deck yang tersedia (dapat diubah nanti)
available_decks = [
    "English to Indonesian",
    "Matematika Dasar",
    "Sejarah Indonesia"
]

# Menu opsi di bawah
menu_options = [
    "Buat Deck Baru",
    "Import Deck",
    "Kelola Deck"
]

def show_menu(selected_deck, selected_option, in_deck_mode):
    """Menampilkan menu utama dengan deck dan opsi."""
    clear()
    
    # Title
    title = "============================================= Care Card V.1 =============================================="
    set_color(BRIGHT | WHITE)
    print(center_text(title))
    print()
    
    # Header untuk deck
    set_color(BRIGHT | CYAN)
    deck_header = "Deck yang Tersedia:"
    print(center_text(deck_header))
    print()
    set_color(WHITE)
    
    # Menampilkan daftar deck (di tengah) dengan highlight
    if available_decks:
        for i, deck in enumerate(available_decks):
            if in_deck_mode and i == selected_deck:
                set_color(BRIGHT | GREEN)
                deck_text = f"> {deck} <"
                print(center_text(deck_text))
                set_color(WHITE)
            else:
                deck_text = f"  • {deck}"
                print(center_text(deck_text))
    else:
        no_deck_text = "  (Belum ada deck)"
        set_color(YELLOW)
        print(center_text(no_deck_text))
        set_color(WHITE)
    
    print()
    print()
    
    # Menu opsi di bawah (horizontal dari kanan ke kiri)
    set_color(BRIGHT | CYAN)
    options_header = "Menu:"
    print(center_text(options_header))
    print()
    set_color(WHITE)
    
    # Menampilkan opsi menu horizontal (dari kanan ke kiri - reverse order)
    # Membuat menu items dalam urutan terbalik
    menu_items_reversed = list(reversed(menu_options))
    
    # Menghitung total panjang untuk center
    menu_texts = []
    for i, option in enumerate(menu_items_reversed):
        original_index = len(menu_options) - 1 - i
        if not in_deck_mode and original_index == selected_option:
            menu_texts.append(f"[> {option} <]")
        else:
            menu_texts.append(f"[  {option}  ]")
    
    total_length = sum(len(text) for text in menu_texts) + (len(menu_texts) - 1) * 2
    x = (cols - total_length) // 2
    
    # Print dengan spacing dan warna hijau untuk menu yang dipilih
    print(" " * x, end="")
    for i, (text, option) in enumerate(zip(menu_texts, menu_items_reversed)):
        original_index = len(menu_options) - 1 - i
        if not in_deck_mode and original_index == selected_option:
            # Warna hijau terang untuk menu yang dipilih
            set_color(BRIGHT | GREEN)
            print(text, end="")
            set_color(WHITE)  # Reset ke warna default setelah print
        else:
            # Warna putih normal untuk menu yang tidak dipilih
            set_color(WHITE)
            print(text, end="")
        if i < len(menu_texts) - 1:
            print("  ", end="")
    print()
    
    print()
    set_color(BRIGHT | YELLOW)
    if in_deck_mode:
        instruction = "↑/↓: Pilih Deck | Tab: Pindah ke Menu | Enter: Buka Deck | ESC: Keluar"
    else:
        instruction = "←/→: Navigasi Menu | Tab: Pindah ke Deck | Enter: Pilih Menu | ESC: Keluar"
    print(center_text(instruction))
    set_color(WHITE)

def mainmenu():
    """Fungsi utama untuk menjalankan menu."""
    selected_deck = 0
    selected_option = 0
    in_deck_mode = True  # True = navigasi di deck, False = navigasi di menu
    
    while True:
        show_menu(selected_deck, selected_option, in_deck_mode)
        
        # Mendapatkan input keyboard
        key = msvcrt.getch()
        
        # Handle arrow keys (Windows)
        if key == b'\xe0':  # Arrow key prefix
            key = msvcrt.getch()
            if key == b'H':  # Panah atas
                if in_deck_mode and available_decks:
                    selected_deck = (selected_deck - 1) % len(available_decks)
            elif key == b'P':  # Panah bawah
                if in_deck_mode and available_decks:
                    selected_deck = (selected_deck + 1) % len(available_decks)
            elif key == b'K':  # Panah kiri (karena menu terbalik, kiri = index lebih besar)
                if not in_deck_mode:
                    selected_option = (selected_option + 1) % len(menu_options)
            elif key == b'M':  # Panah kanan (karena menu terbalik, kanan = index lebih kecil)
                if not in_deck_mode:
                    selected_option = (selected_option - 1) % len(menu_options)
        elif key == b'\t':  # Tab untuk pindah mode
            in_deck_mode = not in_deck_mode
        elif key == b'\r':  # Enter
            clear()
            if in_deck_mode and available_decks:
                # Memilih deck
                set_color(BRIGHT | GREEN)
                print(center_text(f"Kamu memilih deck: {available_decks[selected_deck]}"))
                set_color(WHITE)
                print()
                print(center_text("Fitur membuka deck akan segera tersedia..."))
            else:
                # Memilih menu opsi
                set_color(BRIGHT | GREEN)
                print(center_text(f"Kamu memilih: {menu_options[selected_option]}"))
                set_color(WHITE)
                print()
                
                # Handle aksi untuk setiap menu
                if menu_options[selected_option] == "Buat Deck Baru":
                    print(center_text("Fitur Buat Deck Baru akan segera tersedia..."))
                    print()
                    input(center_text("Tekan Enter untuk kembali ke menu..."))
                elif menu_options[selected_option] == "Import Deck":
                    print(center_text("Fitur Import Deck akan segera tersedia..."))
                    print()
                    input(center_text("Tekan Enter untuk kembali ke menu..."))
                elif menu_options[selected_option] == "Kelola Deck":
                    print(center_text("Fitur Kelola Deck akan segera tersedia..."))
                    print()
                    input(center_text("Tekan Enter untuk kembali ke menu..."))
        elif key == b'\x1b':  # ESC untuk keluar
            clear()
            set_color(BRIGHT | YELLOW)
            print(center_text("Terima kasih telah menggunakan Care Card!"))
            set_color(WHITE)
            break

if __name__ == "__main__":
    mainmenu()


