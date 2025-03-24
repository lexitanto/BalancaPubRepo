#!/bin/bash

REPO_PATH="/opt/BalancaPubRepo"
CMD_INICIAR="python3 $REPO_PATH/bin/app/main.py"
LOG_FILE="/tmp/monitor.log"
onehour=3600

echo "$(date '+%Y-%m-%d %H:%M:%S') - [Monitor] Monitor iniciado" | tee -a "$LOG_FILE"

while true; do
    if ! pgrep -f "python3 $REPO_PATH/bin/app/main.py" > /dev/null; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - [Monitor] Iniciando aplicação..." | tee -a "$LOG_FILE"
        $CMD_INICIAR &
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - [Monitor] Connection is alive" | tee -a "$LOG_FILE"
    fi
    sleep "$onehour"
done