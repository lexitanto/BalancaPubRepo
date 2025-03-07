#!/bin/bash

# Configuração
NOME_PROCESSO="index.py" # Nome do processo Python
CAMINHO_APP="$HOME/monitorPython/ProjetoBalanca"
CMD_INICIAR="python3 index.py" # Comando para iniciar a aplicação
INTERVALO=3600 # Tempo (segundos) entre verificações

> /tmp/monitor.log

# Espera até que a conexão com a internet esteja disponível
while ! ping -c 1 8.8.8.8 &> /dev/null; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Sem conexão. Tentando novamente em 3 segundos..." | tee -a /tmp/monitor.log
    sleep 3
done
echo "$(date '+%Y-%m-%d %H:%M:%S') - Conectado à internet!" | tee -a /tmp/monitor.log

# Loop principal para verificar o status do processo
while :; do
    # Verifica se a aplicação está rodando
    if ! pgrep -f "$NOME_PROCESSO" > /dev/null; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Aplicação caiu! Reiniciando..." | tee -a /tmp/monitor.log
        
        # Navega até o diretório da aplicação
        cd "$CAMINHO_APP" || exit

        # Atualiza o código
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Atualizando código..." | tee -a /tmp/monitor.log
        git pull origin main
        
        # Mata qualquer processo anterior para evitar duplicatas
        pkill -f "$NOME_PROCESSO"
        
        # Reinicia a aplicação
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Iniciando aplicação..." | tee -a /tmp/monitor.log
        nohup $CMD_INICIAR 2>&1 >> /tmp/monitor.log 2>&1 &
    fi

    # Espera o intervalo definido antes de verificar novamente
    sleep "$INTERVALO"
done