#!/bin/bash

# Raspberry Pi Bootloader Update Script
# Prüft und aktualisiert den EEPROM-Bootloader bei Bedarf

echo "🔍 Prüfe aktuellen Bootloader-Status..."
rpi-eeprom-update

# Neueste Firmware-Infos abrufen
LATEST_VERSION=$(rpi-eeprom-update | grep "LATEST:" | awk '{print $2}')
CURRENT_VERSION=$(rpi-eeprom-update | grep "CURRENT:" | awk '{print $2}')

# Prüfen, ob ein Update notwendig ist
if [ "$LATEST_VERSION" == "$CURRENT_VERSION" ]; then
    echo "✅ Bootloader ist bereits aktuell: $CURRENT_VERSION"
    exit 0
else
    echo "🚀 Neuer Bootloader verfügbar: $LATEST_VERSION (aktuell: $CURRENT_VERSION)"
    echo "💾 Erstelle Backup des aktuellen Bootloaders..."
    sudo cp /lib/firmware/raspberrypi/bootloader/critical/pieeprom.bin "/boot/pieeprom_backup_$(date +%Y%m%d).bin"
    echo "🔄 Update wird durchgeführt..."
    sudo rpi-eeprom-update -a
    echo "🔁 Neustart erforderlich!"
    read -p "Möchtest du jetzt neustarten? (y/n) " choice
    if [ "$choice" == "y" ]; then
        sudo reboot
    else
        echo "⚠ Bitte manuell neustarten, um das Update zu aktivieren!"
    fi
fi
