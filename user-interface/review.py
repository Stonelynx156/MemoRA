import ctypes
import utils.deck as deck
import utils.cards as cards
from datetime import datetime,timezone
import heapq
import itertools
from utils.deck import load_deck, save_deck, save_limit,load_limit
from utils.cards import card_queue, update_schedule, card_status

from console import (
    clear, 
    set_color,
    center_text,
    read_key,
    wait_for_enter,
    get_terminal_size,
    wait_for_key_with_resize,
    print_spacer_before_bottom_options,
    EXIT_TOKEN
    )

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

quality_options = [
    "[1] Again",
    "[2] Hard",
    "[3] Good",
    "[4] Easy"
]
def get_limit(limit):
    try:
        value = int(input(limit))
        return value
    except ValueError:
        return None

def display_question(deck_name, question, status):
    clear()
    set_color(BRIGHT | BLUE)
    print(center_text(f"=== {deck_name} ==="))
    set_color(WHITE)
    print()

    set_color(BRIGHT | GREEN)
    print(center_text("PERTANYAAN:"))
    set_color(WHITE)
    print(center_text(question))
    print("\n" * 5)    

    # Instruksi
    set_color(BRIGHT | YELLOW)
    instruction = "===== Tekan Spasi / Enter untuk melihat jawaban ====="
    print(center_text(instruction))
    set_color(WHITE)

    new_count = status[0]
    review_count = status[1]
    due_count = status[2]
    
    # Buat teks tanpa warna untuk menghitung panjang
    status_text = f"{new_count}   {review_count}   {due_count}"
    cols, _ = get_terminal_size()
    padding = (cols - len(status_text)) // 2

    print(" " * padding, end="")
    set_color(BRIGHT | GREEN)
    print(f"{new_count}", end="", flush=True)
    set_color(WHITE)
    print("   ", end="", flush=True)
    set_color(BRIGHT | RED)
    print(f"{review_count}", end="", flush=True)
    set_color(WHITE)
    print("   ", end="", flush=True)
    set_color(BRIGHT | CYAN)
    print(f"{due_count}", flush=True)
    set_color(WHITE)

def display_answer(deck_name, question, answer):
    clear()
    set_color(BRIGHT | BLUE)
    print(center_text(f"=== {deck_name} ==="))
    set_color(WHITE)
    print()

    set_color(BRIGHT | GREEN)
    print(center_text("PERTANYAAN:"))
    set_color(WHITE)
    print(center_text(question))
    print("\n" * 4)

    set_color(BRIGHT | BLUE)
    print(center_text("JAWABAN:"))
    set_color(WHITE)
    print(center_text(answer))
    
    lines_used = 13
    bottom_section_height = 2  
    
    print_spacer_before_bottom_options(lines_used, bottom_section_height)

    # Quality options di bawah
    set_color(BRIGHT | CYAN)
    quality_text = "  ".join(quality_options)
    print(center_text(quality_text))
    print()
    
    # Instruksi
    set_color(BRIGHT | YELLOW)
    instruction = "Pilih rating (1-4) untuk melanjutkan | ESC untuk kembali"
    print(center_text(instruction))
    set_color(WHITE)

def no_review(deck_name):
    clear()
    set_color(BRIGHT | BLUE)
    print(center_text(f"=== {deck_name} ==="))
    print()
    print()
    print()
    set_color(BRIGHT | CYAN)
    print(center_text("Selamat! Kamu sudah menyelesaikan dek ini untuk sekarang. "))
    print(center_text("Kamu bisa mengubah maksimal kartu baru per hari saat memilih deck!"))
    set_color(BRIGHT | YELLOW)
    print()
    wait_for_enter(center_text("Tekan Enter untuk kembali..."))
    set_color(WHITE)

def review_deck(deck_name, new, due, init):
    prev_size = get_terminal_size()
    show_answer = False
    cards_raw = load_deck(deck_name)
    counter = itertools.count()
    queue = card_queue(deck_name, new, due)
    # Tampilkan pertanyaan pertama kali
    if not queue:
        no_review(deck_name)
        return
    
    while queue:
        status = card_status(queue)
        _, _, card = heapq.heappop(queue)
        q = card.front
        a = card.back
        display_question(deck_name, q, status)
        limit = load_limit(deck_name)
        show_answer = False
        while True:
            key, prev_size = wait_for_key_with_resize(prev_size)

            if key == EXIT_TOKEN:
                return
            
            if key is None:
                # Terminal di-resize, refresh tampilan
                if show_answer:
                    display_answer(deck_name, card.front, card.back)
                else:
                    display_question(deck_name, card.front, status)
                continue

            if not show_answer:
                # State: menampilkan pertanyaan
                if key == 'SPASI' or key == 'ENTER':
                    show_answer = True
                    display_answer(deck_name, q, a)
                elif key == 'ESC':
                    return
                else:
                    continue
            
            else:
                # State: menampilkan jawaban
                if key == 'ESC':
                    return
                elif isinstance(key, tuple) and key[0] == 'CHAR':
                    char = key[1]
                    if char in ['1', '2', '3', '4']:
                        # Handle rating (bisa ditambahkan logika update card di sini)
                        quality = int(char) - 1
                        if card.first_time == True:
                            if limit["due_limit"] is not None and limit["due_limit"]> 0: 
                                due = limit["due_limit"] - 1
                        if datetime.fromisoformat(card.due) <= datetime.now(timezone.utc):
                            if limit["new_limit"] is not None and limit["new_limit"]> 0 : 
                                new = limit["new_limit"] - 1 
                        update_schedule(card, quality)
                        if card.step <= 3:
                            due_dt = card.due if isinstance(card.due, datetime) else datetime.fromisoformat(card.due)
                            heapq.heappush(queue, (due_dt,next(counter), card))
                            
                        for idx, stored in enumerate(cards_raw):
                            if stored["id"] == card.id:
                                cards_raw[idx] = card.to_dict()                        
                        save_deck(deck_name, cards_raw)
                        save_limit(deck_name, new, due, init)
                        break
                        # Untuk sekarang, kembali ke pertanyaan atau lanjut ke kartu berikutnya   
    queue = card_queue(deck_name)
    no_review(deck_name)
    return

def review_menu(deck_name, new, due):
    """Menu review deck - menampilkan statistik dan opsi untuk mulai review"""
    prev_size = get_terminal_size()
    while True:
        limit = load_limit(deck_name)
        new = limit["new_limit"]
        due = limit["due_limit"]
        init = limit["init"]
        init_new = init[0]
        init_due = init[1]
        queue = card_queue(deck_name, new, due)
        clear()
        
        # Header
        set_color(BRIGHT | BLUE)
        print(center_text(f"=== {deck_name} ==="))
        print()
        set_color(WHITE)
        
        # Statistik
        set_color(BRIGHT | CYAN)
        print(center_text("Statistik Deck:"))
        print()
        set_color(WHITE)
        
        set_color(BRIGHT | GREEN)
        print(center_text(f"Kartu Baru        : {card_status(queue)[0]}"))
        set_color(BRIGHT | RED)
        print(center_text(f"Kartu Tinjau      : {card_status(queue)[1]}"))
        set_color(BRIGHT | CYAN)
        print(center_text(f"Kartu Jatuh Tempo : {card_status(queue)[2]}"))
        set_color(WHITE)
        print()

        lines_used = 7
        bottom_section_height = 3
        print_spacer_before_bottom_options(lines_used, bottom_section_height)

        set_color(BRIGHT | BLUE)
        print(center_text("Tekan ESC untuk kembali"))
        set_color(BRIGHT | YELLOW)
        print(center_text("Tekan Enter untuk mulai review"))
        set_color(BRIGHT | MAGENTA)
        print(center_text("Tekan TAB untuk pengaturan limit"))
        set_color(WHITE)
        
        key, prev_size = wait_for_key_with_resize(prev_size)
        if key == EXIT_TOKEN:
            return
        if key is None:
            continue

        # Mulai sesi review
        if key == 'ENTER':
            print
            review_deck(deck_name, new, due, init)
        elif key == 'TAB':
            clear()
            set_color(BRIGHT | BLUE)
            print(center_text(f"=== {deck_name} ==="))
            set_color(WHITE)
            print()
            print(center_text("Kosongkan untuk default"))
            print()
            new_limit = get_limit(center_text("Masukkan Limit Kartu Baru: ")) 
            due_limit = get_limit(center_text("Masukkan Limit Kartu Jatuh Tempo: "))
            
            if datetime.fromisoformat(limit["date"]) <= datetime.now(timezone.utc):
                new = new_limit
                due = due_limit
                save_limit(deck_name, new, due,[new, due])
            else:    
                if new_limit and new_limit >= 0 and init_new and new:
                    d_new = new_limit - init_new
                    if d_new > 0:
                        new += new_limit - init_new
                    elif init_new - new_limit > 0 and new > 0:
                        new = new_limit
                    else: new = new
                elif new_limit is None: new = new_limit
                else: 
                    new = new_limit - init_new 
                    if new < 0: new = 0 
                if due_limit and due_limit >= 0 and init_due and due:
                    d_due = due_limit - init_due
                    if d_due > 0:
                        due += due_limit - init_due
                    elif init_due - due_limit > 0 and due > 0:
                        due = due_limit
                    else: due = due
                elif due_limit is None: due = due_limit
                else: 
                    due = due_limit - init_due
                    if due < 0: due =0
                if new or due:
                    save_limit(deck_name, new, due,[new, due])
                else:
                    save_limit(deck_name, new, due,[init_new, init_due])
            return review_menu(deck_name, new, due)        
        elif key == 'ESC':
            return

def show_review_deck(deck_name):
    limit = load_limit(deck_name)
    new = limit["new_limit"]
    due = limit["due_limit"]
    
    review_menu(deck_name, new, due)


    
