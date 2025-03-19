#!/bin/bash

MOUNT_PATH="/mnt/usb_wifi"
[ ! -d "$MOUNT_PATH" ] && mkdir -p "$MOUNT_PATH"

echo "Dispositivo detectado: $1" | logger
