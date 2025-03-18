#!/bin/bash

MOUNT_POINT="/mnt/usb_wifi"
CONFIG_FILE="wifi_setup.txt"
WPA_SUPPLICANT="/etc/wpa_supplicant/wpa_supplicant.conf"

# Criar diretório de montagem
sudo mkdir -p "$MOUNT_POINT"

# Monitorar dispositivos USB
while true; do
    # Esperar por um pendrive
    DEVICE=$(lsblk -o NAME,MOUNTPOINT | grep -E 'sd[b-z]' | awk '{print $1}' | head -n 1)
    
    if [[ -n "$DEVICE" ]]; then
        echo "Pendrive detectado: /dev/$DEVICE"

        # Montar como somente leitura
        sudo mount -o ro /dev/"$DEVICE"1 "$MOUNT_POINT"

        if [[ -f "$MOUNT_POINT/$CONFIG_FILE" ]]; then
            echo "Arquivo $CONFIG_FILE encontrado. Processando..."

            # Ler SSID e senha do arquivo
            SSID=$(grep "SSID=" "$MOUNT_POINT/$CONFIG_FILE" | cut -d '=' -f2 | tr -d '\r')
            PASS=$(grep "PASS=" "$MOUNT_POINT/$CONFIG_FILE" | cut -d '=' -f2 | tr -d '\r')

            # Validar entrada
            if [[ -z "$SSID" || -z "$PASS" ]]; then
                echo "Erro: SSID ou senha vazios."
            else
                echo "Configurando Wi-Fi para SSID: $SSID"

                # Criar novo wpa_supplicant.conf seguro
                sudo bash -c "cat > $WPA_SUPPLICANT" <<EOF
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=BR

network={
    ssid="$SSID"
    psk="$PASS"
    key_mgmt=WPA-PSK
    scan_ssid=1
}
EOF
                sudo systemctl restart wpa_supplicant
                echo "Wi-Fi configurado com sucesso!"
            fi
        else
            echo "Arquivo $CONFIG_FILE não encontrado. Ignorando pendrive."
        fi

        sudo umount "$MOUNT_POINT"
        echo "Pendrive removido."

        sleep 10
    fi

    sleep 2
done
