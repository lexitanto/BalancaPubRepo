#!/bin/bash

REPO_PATH="/opt/BalancaPubRepo"
CMD_INICIAR="python3 $REPO_PATH/bin/app/index.py"

echo "$(date '+%Y-%m-%d %H:%M:%S') - Verificando e atualizando o repositório..." | tee -a /tmp/monitor.log

# Atualiza o repositório
git -C $REPO_PATH fetch origin

# Força a atualização do repositório local para o estado remoto, ignorando quaisquer mudanças locais
git -C $REPO_PATH reset --hard origin/main

if ! pgrep -f "python3 $REPO_PATH/bin/app/index.py" > /dev/null; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Iniciando aplicação..." | tee -a /tmp/monitor.log
    $CMD_INICIAR
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - A aplicação já está rodando." | tee -a /tmp/monitor.log
fi
