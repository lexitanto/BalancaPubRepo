#!/bin/bash

MOUNT_POINT="/mnt/usb_wifi"
LOCK_FILE="/tmp/usb_wifi.lock"
WPA_CONF="/etc/wpa_supplicant/wpa_supplicant.conf"


echo "Monitorando dispositivos USB..."

if [ -f "$LOCK_FILE" ]; then
    echo "Script já foi executado neste boot. Saindo..."
    exit 0
fi
touch "$LOCK_FILE"

echo "Criando diretório de montagem: $MOUNT_POINT"
mkdir -p "$MOUNT_POINT"

while true; do
    DEVICE=$(lsblk -rpo "NAME,TRAN" | grep "usb" | awk '{print $1}' | head -n 1)
    
    if [ -n "$DEVICE" ]; then
        PARTITION="${DEVICE}1"
        echo "Pendrive detectado: $DEVICE. Utilizando a partição: $PARTITION"

        if mount | grep -q "$PARTITION"; then
            echo "O dispositivo $PARTITION já está montado em outro local. Desmontando..."
            sudo umount "$PARTITION"
            sleep 1
        fi

        echo "Montando $PARTITION em $MOUNT_POINT..."
        sudo mount -o ro,nosuid,noexec "$PARTITION" "$MOUNT_POINT"
        if [ $? -ne 0 ]; then
            echo "Falha ao montar $PARTITION. Pulando..."
            sleep 5
            continue
        fi

        if [ -f "$MOUNT_POINT/wifi.txt" ]; then
            echo "Arquivo wifi.txt encontrado. Aplicando configurações..."
            SSID=$(grep 'SSID' "$MOUNT_POINT/wifi.txt" | cut -d '=' -f2 | tr -d ';|&$()<>`')
            PASSWORD=$(grep 'PASSWORD' "$MOUNT_POINT/wifi.txt" | cut -d '=' -f2 | tr -d ';|&$()<>`')
            
            cat <<EOF | sudo tee "$WPA_CONF" > /dev/null
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=BR

network={
    ssid="$SSID"
    psk="$PASSWORD"
    key_mgmt=WPA-PSK
}
EOF

            echo "Wi-Fi configurado para SSID: $SSID"
            
            sudo systemctl restart wpa_supplicant

        else
            echo "Arquivo wifi.txt não encontrado no pendrive."
        fi

        echo "Desmontando $PARTITION de $MOUNT_POINT..."
        sudo umount "$MOUNT_POINT"

    else
        echo "Nenhum pendrive detectado. Aguardando..."
    fi

    sleep 10
    
done
