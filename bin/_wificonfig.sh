#!/bin/bash

MOUNT_PATH="/mnt/usb_wifi"

DEVICE=$(echo "$1" | sed 's/[0-9]*$//')

for PARTITION in /dev/${DEVICE}*; do
    if mount | grep -q "$PARTITION"; then
        echo "$PARTITION já montado." | logger
        continue
    fi

    if grep -q "wifi_setup.txt" <(ls "$PARTITION"/*); then
        [ ! -d "$MOUNT_PATH" ] && mkdir -p "$MOUNT_PATH"
        mount "$PARTITION" "$MOUNT_PATH" || exit 1

        echo "Configurando Wi-Fi a partir de: $PARTITION" | logger

        umount "$MOUNT_PATH"
        break
    fi
done
