<!-- Banner / Header -->
<p align="center">
  <img src="https://via.placeholder.com/1200x300.png?text=Festika+-+CLI+Flashcard+System" width="100%">
</p>

<h1 align="center">📚 Festika — CLI Flashcard System</h1>
<p align="center"><b>Alternatif Anki yang lebih cepat, ringan, dan efisien langsung dari terminal.</b></p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-CLI-blue">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen">
  <img src="https://img.shields.io/badge/License-MIT-green">
</p>

---

## 📌 Tentang Care Cards
**Care Cards** adalah aplikasi flashcard berbasis **Command Line Interface (CLI)** yang dirancang sebagai alternatif **Anki** untuk pengguna yang menginginkan:

- kecepatan  
- kesederhanaan  
- terminal-based workflow  
- kontrol penuh tanpa GUI  

Aplikasi ini sangat cocok untuk programmer, pengguna terminal, dan siapa pun yang ingin belajar tanpa distraksi.

---

# ⭐ Keunggulan Festika Dibanding Anki Normal

## ⚡ 1. Super Ringan — Tidak Butuh GUI Sama Sekali
Anki memakai QT5 yang agak berat untuk device low-end.  
**Festika berjalan full di terminal**, cocok untuk:

- PC low-spec  
- WSL  
- Server headless  
- Raspberry Pi  

➡ *Tidak ada loading GUI, langsung jalan.*

---

## 🔥 2. Akses Sangat Cepat — Keyboard-Only Navigation
Tidak ada klik mouse seperti Anki.  
Festika mendukung navigasi super cepat:

- Arrow keys  
- Enter  
- Shortcuts huruf/angka  

➡ *Belajar jadi cepat & fokus.*

---

## 🧪 3. Fleksibel dan Mudah Dikustomisasi
Anki memerlukan add-on untuk mengubah UI/UX.  
Festika:

- UI seluruhnya berbasis teks  
- Bisa dimodifikasi lewat kode Python  
- Bisa dipakai dalam pipeline terminal  
- Bisa di-automate & di-scripting  

➡ *Benar-benar developer-friendly.*

---

## 🧱 4. Struktur Data Sederhana
Anki menggunakan SQLite `.apkg` yang kompleks.  
Festika memakai:

- JSON / TXT format sederhana  
- Mudah dibaca  
- Bisa langsung di-edit dan commit ke Git  

➡ *Tidak ada metadata rumit.*

---

## 📈 5. Belajar Tanpa Distraksi Visual
Anki memiliki banyak UI element: card, deck list, popup, menu.  
Festika hanya fokus pada:

- pertanyaan  
- jawaban  
- review  
- progress  

➡ *Minimalis = retensi belajar lebih tinggi.*

---

## 💻 6. Terminal-Aware + Responsive TUI
Festika mendukung fitur yang bahkan Anki tidak miliki:

- auto detect ukuran terminal  
- spacer vertikal dinamis  
- highlight warna (ANSI / WinAPI)  
- TUI yang responsif  

➡ *Tetap tertata rapi meskipun terminal berubah ukuran.*

---

## 🔒 7. Tidak Ada Telemetry
Festika **100% tanpa tracking**, tanpa internet, tanpa data usage.

➡ *Privasi penuh.*

---

---

# 🚀 Demo Singkat
*(Tambahkan GIF nanti jika ada)*

```
python main.py
```

---

# ✨ Fitur Utama
- Membuat deck
- Menambah kartu baru
- Review kartu (SM-2 sederhana)
- TUI dengan warna
- Auto terminal-size check
- Navigation full keyboard (msvcrt)
- JSON storage sederhana

---

# 📦 Instalasi
```
git clone https://github.com/username/festika
cd festika
python main.py
```

---

# ▶️ Cara Menjalankan
```
python main.py
```

---

# 🧩 Struktur Folder
```
festika/
│── core/
│   ├── deck.py
│   ├── card.py
│   └── scheduler.py
│── ui/
│   ├── tui.py
│   ├── color.py
│   └── spacer.py
│── data/
│   └── decks.json
│── main.py
│── README.md
```

---

# 🤝 Kontribusi
Pull request dipersilakan!  
Jika ingin menambah fitur — misalnya:

- TUI lebih canggih  
- Mode review baru  
- Integrasi cloud  
- Export/import deck  

Buat issue dan mari diskusikan!

---

# 📄 Lisensi
MIT License

---

# 👤 Author
**anglerfish**  
🔗 https://github.com/anglerfish
