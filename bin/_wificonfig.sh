#!/bin/bash

MOUNT_POINT="/mnt/usb_wifi"
CONFIG_FILE="wifi_setup.txt"
DEVICE="/dev/$1"
[ ! -d "$MOUNT_POINT" ] && mkdir -p "$MOUNT_POINT"

sudo systemctl daemon-reload
sudo mount -o ro "$DEVICE" "$MOUNT_POINT"
echo "Dispositivo montado."
if [ $? -ne 0 ]; then
    echo "Erro ao montar $DEVICE"
    exit 1
fi

if [[ -f "$MOUNT_POINT/$CONFIG_FILE" ]]; then

    echo "Arquivo $CONFIG_FILE encontrado." 
    sudo umount $MOUNT_POINT
    echo "Dispositivo desmontado."
    
fi

