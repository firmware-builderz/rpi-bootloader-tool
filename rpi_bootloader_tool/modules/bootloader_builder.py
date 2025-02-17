import os
import cmd
import requests
import subprocess


from tqdm import tqdm
from datetime import datetime
from rpi_bootloader_tool import *




# Verzeichnisse
BASE_DIR = "rpi_bootloader"
SOURCE_DIR = os.path.join(BASE_DIR, "source")
LOG_FILE = os.path.join(BASE_DIR, f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")

# VFAT-Image
IMAGE_NAME = os.path.join(BASE_DIR, "boot.vfat")
IMAGE_SIZE_MB = 256  # Raspberry Pi Boot-Partition Größe (256MB)

# GitHub API URL für das Repository
GITHUB_API_URL = "https://api.github.com/repos/firmware-builderz/rpi-firmware/contents/"

# Erlaubte Dateiendungen
ALLOWED_EXTENSIONS = (".dtb", ".img", ".dat", ".elf")









class Main(cmd.Cmd):
   
    
    
    

    def do_run(self):
        """Gesamtes Skript ausführen: Download + Image-Erstellung."""
        print("rpi-tools > Start building bootloader!!!:::...::..:.")
        self.download_files()
        self.create_vfat_image()




    def get_file_list(self):
        """Holt die Dateiliste aus dem GitHub-Repository."""
        response = requests.get(GITHUB_API_URL)

        if response.status_code != 200:
            print(f"Fehler beim Abrufen der Dateiliste: {response.status_code}")
            print(response.text)
            return []

        return response.json()

    def download_file(file_url, file_path):
        """Lädt eine Datei herunter und zeigt eine Fortschrittsanzeige."""
        response = requests.get(file_url, stream=True)

        if response.status_code == 200:
            file_size = int(response.headers.get("content-length", 0))
            with open(file_path, "wb") as f, tqdm(
                desc=os.path.basename(file_path),
                total=file_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    bar.update(len(chunk))
        else:
            print(f"❌ Fehler beim Herunterladen von {file_url}: {response.status_code}")

    def download_files(self):
        """Lädt die Dateien aus GitHub herunter und speichert sie in source/"""
        os.makedirs(SOURCE_DIR, exist_ok=True)
        files = self.get_file_list()
        log_entries = []

        if not files:
            print("Keine Dateien gefunden oder Fehler beim Abrufen der Dateiliste.")
            return

        for file in files:
            file_name = file["name"]
            file_url = file["download_url"]

            if file_url and file_name.endswith(ALLOWED_EXTENSIONS):
                file_path = os.path.join(SOURCE_DIR, file_name)
                self.download_file(file_url, file_path)
                file_size = os.path.getsize(file_path)
                log_entries.append(f"{file_name} - {file_size / 1024:.2f} KB")



        # Log-Datei für die heruntergeladenen Dateien erstellen
        with open(LOG_FILE, "w") as log:
            log.write(f"📄 Download Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log.write("=======================================\n")
            log.write("🔹 Dateien im 'source'-Verzeichnis:\n")
            log.write("\n".join(log_entries))
            log.write("\n=======================================\n")
            log.write(f"📦 Gesamtgröße: {sum(os.path.getsize(os.path.join(SOURCE_DIR, f)) for f in os.listdir(SOURCE_DIR)) / 1024:.2f} KB\n")
            log.write("🛠 Created by Firmware-Builder\n")

    def create_vfat_image(self):
        """Erstellt ein VFAT-Image und kopiert die Dateien hinein."""
        img_size_bytes = IMAGE_SIZE_MB * 1024 * 1024
        log_entries = []

        # 1️⃣ Leeres Image erstellen
        print(f"📦 Erstelle leeres Image '{IMAGE_NAME}' mit {IMAGE_SIZE_MB}MB...")
        subprocess.run(["dd", "if=/dev/zero", f"of={IMAGE_NAME}", f"bs=1M", f"count={IMAGE_SIZE_MB}"], check=True)

        # 2️⃣ Image als Loopback-Gerät mounten
        print("🔄 Erstelle Loopback-Gerät...")
        subprocess.run(["mkfs.vfat", IMAGE_NAME], check=True)

        mount_dir = "/mnt/rpi-boot"
        os.makedirs(mount_dir, exist_ok=True)

        loop_device = subprocess.run(["losetup", "--show", "-fP", IMAGE_NAME], capture_output=True, text=True).stdout.strip()
        print(f"📌 Loopback-Gerät: {loop_device}")

        # 3️⃣ Image mounten
        subprocess.run(["mount", loop_device, mount_dir], check=True)

        # 4️⃣ Dateien in das Image kopieren
        print("📂 Kopiere Boot-Dateien ins Image...")
        for file_name in os.listdir(SOURCE_DIR):
            file_path = os.path.join(SOURCE_DIR, file_name)
            subprocess.run(["cp", file_path, mount_dir], check=True)
            file_size = os.path.getsize(file_path)
            log_entries.append(f"{file_name} - {file_size / 1024:.2f} KB")

        # 5️⃣ Image aushängen und Loopback entfernen
        print("🚀 Unmounting und Loopback entfernen...")
        subprocess.run(["umount", mount_dir], check=True)
        subprocess.run(["losetup", "-d", loop_device], check=True)

        # Log-Datei für das Image erstellen
        image_log = os.path.join(BASE_DIR, f"image_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
        with open(image_log, "w") as log:
            log.write(f"📄 Image Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log.write("=======================================\n")
            log.write("🔹 Dateien im 'boot.vfat'-Image:\n")
            log.write("\n".join(log_entries))
            log.write("\n=======================================\n")
            log.write(f"📦 Gesamtgröße: {sum(os.path.getsize(os.path.join(SOURCE_DIR, f)) for f in os.listdir(SOURCE_DIR)) / 1024:.2f} KB\n")
            log.write("🛠 Created by Firmware-Builder\n")

        print(f"🎉 VFAT-Image '{IMAGE_NAME}' wurde erfolgreich erstellt!")


    


