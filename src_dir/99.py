from pathlib import Path

def create_folder(path):
    p = Path(path)
    if not p.exists():
        p.mkdir(parents=True)
        print(f"Папку '{p}' створено.")
    else:
        print(f"Папка '{p}' вже існує.")

create_folder('D:\\PytnonWebDev\\goit-pythonweb-hw-04\\folder_out')