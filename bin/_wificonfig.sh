#!/bin/bash

MOUNT_PATH="/mnt/usb_wifi"
[ ! -d "$MOUNT_POINT" ] && mkdir -p "$MOUNT_POINT"

echo "Dispositivo detectado: $1" | logger
