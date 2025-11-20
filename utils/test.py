from deck import deck_file_path
name = "Tes"
safe = "".join(c if c.isalnum() else "_" for c in name)
print(name)
print(deck_file_path(name))