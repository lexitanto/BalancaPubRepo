#!/bin/bash

USER=$(logname)
SERVICE_FILE="/etc/systemd/system/monitor@.service"
SCRIPT_PATH="/home/$USER/monitorPython/ProjetoBalanca/scripts/_monitor.sh"

sudo chmod +x $SCRIPT_PATH

sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Iniciar o aplicativo no boot do sistema (%i)
After=network.target

[Service]
Type=simple
ExecStart=/home/%i/monitorPython/ProjetoBalanca/scripts/_monitor.sh
WorkingDirectory=/home/%i/monitorPython/ProjetoBalanca/scripts
Restart=always
User=%i
Environment="HOME=/home/%i" "USER=%i"

[Install]
WantedBy=multi-user.target
EOF

# Recarregar os serviços do systemd
echo "Recarregando systemd..."
sudo systemctl daemon-reload

# Ativar o serviço para o usuário atual
echo "Ativando o serviço para $USER..."
sudo systemctl enable monitor@$USER
sudo systemctl start monitor@$USER

echo "✅Serviço monitor@$USER criado e iniciado com sucesso!"
