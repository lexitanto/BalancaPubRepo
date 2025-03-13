#!/bin/bash

echo "Monitorando dispositivos USB..."

MOUNT_POINT="/mnt/usb_wifi"
LOCK_FILE="/tmp/usb_wifi.lock"

# Impedir que o script rode mais de uma vez por boot
if [ -f "$LOCK_FILE" ]; then
    echo "Script já foi executado neste boot. Saindo..."
    exit 0
fi
touch "$LOCK_FILE"

# Criar ponto de montagem, se não existir
echo "Criando diretório de montagem: $MOUNT_POINT"
mkdir -p "$MOUNT_POINT"

while true; do
    # Identifica o primeiro pendrive USB conectado; normalmente ele aparece como /dev/sda
    DEVICE=$(lsblk -rpo "NAME,TRAN" | grep "usb" | awk '{print $1}' | head -n 1)
    
    if [ -n "$DEVICE" ]; then
        # Define a partição de armazenamento (ex: /dev/sda1)
        PARTITION="${DEVICE}1"
        echo "Pendrive detectado: $DEVICE. Utilizando a partição: $PARTITION"

        # Se a partição já estiver montada em outro local, desmontá-la
        if mount | grep -q "$PARTITION"; then
            echo "O dispositivo $PARTITION já está montado em outro local. Desmontando..."
            sudo umount "$PARTITION"
            sleep 1
        fi

        # Montar a partição no diretório de montagem com somente leitura, sem execução e sem setuid
        echo "Montando $PARTITION em $MOUNT_POINT..."
        sudo mount -o ro,nosuid,noexec "$PARTITION" "$MOUNT_POINT"
        if [ $? -ne 0 ]; then
            echo "Falha ao montar $PARTITION. Pulando..."
            sleep 5
            continue
        fi

        # Verifica se o arquivo wifi.txt existe
        if [ -f "$MOUNT_POINT/wifi.txt" ]; then
            echo "Arquivo wifi.txt encontrado. Aplicando configurações..."
            SSID=$(grep 'SSID' "$MOUNT_POINT/wifi.txt" | cut -d '=' -f2 | tr -d ';|&$()<>`')
            PASSWORD=$(grep 'PASSWORD' "$MOUNT_POINT/wifi.txt" | cut -d '=' -f2 | tr -d ';|&$()<>`')
            
            # Atualiza a configuração do Wi-Fi
            cat <<EOF | sudo tee /etc/wpa_supplicant/wpa_supplicant.conf > /dev/null
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

            # Reiniciar os serviços de rede para aplicar as configurações
            sudo systemctl restart networking
            sudo systemctl restart wpa_supplicant
        else
            echo "Arquivo wifi.txt não encontrado no pendrive."
        fi

        # Desmonta a partição após a operação
        echo "Desmontando $PARTITION de $MOUNT_POINT..."
        sudo umount "$MOUNT_POINT"
    else
        echo "Nenhum pendrive detectado. Aguardando..."
    fi

    # Aguarda 5 segundos antes de verificar novamente
    sleep 5
done
