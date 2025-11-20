import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'user-interface'))
import ui

#batas bawah versi py
REQUIRED_MAJOR = 3
REQUIRED_MINOR = 14

#get version py
version = sys.version_info
print(f"Detected Python version: {version.major}.{version.minor}.{version.micro}")

#cek versi
if (version.major < REQUIRED_MAJOR) or (version.major == REQUIRED_MAJOR and version.minor < REQUIRED_MINOR):
    print(f"Python 3.14 atau lebih baru diperlukan!")
    confirm = input("Apakah anda yakin ingin menjalankan program ini dengan resiko program tidak berjalan / crash (y/n): ")
    if confirm == 'y':
        ui.show_menu()
    else:
        print("Program akan ditutup dalam 3 detik")
        time.sleep(3)
        os.system('cls')

else:
    ui.show_menu()

