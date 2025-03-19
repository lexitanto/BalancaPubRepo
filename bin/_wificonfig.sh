#!/bin/bash

MOUNT_POINT="/mnt/usb_wifi"
DEVICE="/dev/$1"
[ ! -d "$MOUNT_POINT" ] && mkdir -p "$MOUNT_POINT"


sudo mount -o ro /dev/"$DEVICE" "$MOUNT_POINT"
if [ $? -ne 0 ]; then
    echo "Erro ao montar $DEVICE"
    exit 1
fi

if [[ -f "$MOUNT_POINT/$CONFIG_FILE" ]]; then

    echo "Arquivo $CONFIG_FILE encontrado." 
    
fi

