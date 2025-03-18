#!/bin/bash

# Caminho para o repositório
CAMINHO_APP="/opt/BalancaPubRepo"
CMD_INICIAR="python3 index.py" # Comando para iniciar a aplicação

# Navega até o diretório do repositório
cd "$CAMINHO_APP" || exit

# Atualiza o repositório remoto sem fazer alterações no local
echo "$(date '+%Y-%m-%d %H:%M:%S') - Verificando se há alterações no repositório..." | tee -a /tmp/monitor.log
git fetch origin

# Verifica se há mudanças na branch remota em relação à local
if git diff --quiet origin/main; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Nenhuma alteração no código." | tee -a /tmp/monitor.log
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Atualizando código..." | tee -a /tmp/monitor.log
    git pull origin main
fi

# Inicia a aplicação
echo "$(date '+%Y-%m-%d %H:%M:%S') - Iniciando aplicação..." | tee -a /tmp/monitor.log
sudo nohup $CMD_INICIAR 2>&1 >> /tmp/monitor.log 2>&1 &
