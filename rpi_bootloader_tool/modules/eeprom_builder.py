import os
import cmd
import requests
import zipfile
import io


from tqdm import tqdm
from datetime import datetime
from rpi_bootloader_tool import *





class Main(cmd.Cmd):
    """ EEPROM Builder Main Class"""
    
    
    def do_run(self, arg):
        print("rpi-tools > Downloading EEPROM!!!:::...::..:.")
        self.get_eeprom()
    
    
    
    def download_file(self, url, dest_folder):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        filename = url.split("/")[-1]
        filepath = os.path.join(dest_folder, filename)
    
        with open(filepath, 'wb') as file, tqdm(
            desc=filename, total=total_size, unit='B', unit_scale=True, unit_divisor=1024
        ) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    bar.update(len(chunk))
        return filename, total_size



    def log_download(self, log_path, filename, size):
        with open(log_path, "a") as log_file:
            log_file.write(f"{datetime.now()} - {filename} - {size / 1024:.2f} KB\n")



    def get_eeprom(self):
        repo_url = "https://github.com/firmware-builderz/rpi-eeprom/archive/refs/heads/master.zip"
        dest_folder = "rpi-eeprom"
        log_file = os.path.join(dest_folder, "download_log.txt")
    
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
    
        # Auswahl des Raspberry Pi Modells
        while True:
            model = input("Wähle dein Raspberry Pi Modell (4 oder 5): ")
            if model in ["4", "5"]:
                break
            print("Ungültige Eingabe. Bitte 4 oder 5 eingeben.")

        firmware_folder = "firmware-2711" if model == "4" else "firmware-2712"
    
        # Download ZIP-Archiv
        print("Lade Repository herunter...")
        response = requests.get(repo_url)
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    
        repo_name = zip_file.namelist()[0].rstrip("/")  # Ordnername aus ZIP
    
        # Dateien entpacken
        for file in tqdm(zip_file.namelist(), desc="Entpacke Dateien", unit="file"):
            if file.startswith(f"{repo_name}/firmware-2711") or file.startswith(f"{repo_name}/firmware-2712"):
                if file.startswith(f"{repo_name}/{firmware_folder}"):
                    zip_file.extract(file, dest_folder)
                    self.log_download(log_file, file, os.path.getsize(os.path.join(dest_folder, file)))
            else:
                zip_file.extract(file, dest_folder)
                self.log_download(log_file, file, os.path.getsize(os.path.join(dest_folder, file)))
    
        print(f"Download abgeschlossen! Dateien befinden sich in: {dest_folder}")
        print(f"Log-Datei gespeichert unter: {log_file}")
    

    
