#!/bin/bash

CMD_INICIAR="python3 /opt/BalancaPubRepo/bin/index.py"
CAMINHO_APP="/opt/BalancaPubRepo"  

echo "$(date '+%Y-%m-%d %H:%M:%S') - Verificando se há alterações no repositório..." | tee -a /tmp/monitor.log

git -C "$CAMINHO_APP" fetch origin

if git -C "$CAMINHO_APP" diff --quiet origin/main; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Nenhuma alteração no código." | tee -a /tmp/monitor.log
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Atualizando código..." | tee -a /tmp/monitor.log
    git -C "$CAMINHO_APP" pull origin main
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') - Iniciando aplicação..." | tee -a /tmp/monitor.log
sudo nohup $CMD_INICIAR 2>&1 >> /tmp/monitor.log 2>&1 &
