#!/bin/bash

REPO_PATH="/opt/BalancaPubRepo"
CMD_INICIAR="python3 $REPO_PATH/bin/index.py"

until ping -c 1 github.com &>/dev/null; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Esperando por conexão com a internet..." | tee -a /tmp/monitor.log
    sleep 5
done

echo "$(date '+%Y-%m-%d %H:%M:%S') - Verificando e atualizando o repositório..." | tee -a /tmp/monitor.log

# Atualiza o repositório
sudo git -C $REPO_PATH fetch origin

# Força a atualização do repositório local para o estado remoto, ignorando quaisquer mudanças locais
sudo git -C $REPO_PATH reset --hard origin/main

# Reinicia a aplicação
echo "$(date '+%Y-%m-%d %H:%M:%S') - Iniciando aplicação..." | tee -a /tmp/monitor.log
sudo nohup $CMD_INICIAR 2>&1 >> /tmp/monitor.log 2>&1 &
