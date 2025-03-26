import os
import time
import requests
from datetime import datetime, timezone

URL_SERVER = "https://erp.sgtrack.com.br/IoT/Balanca/status"
DEVICE_PATH = "/etc/device_id"

class tracking:
    def __init__(self):
        self.numero_serial = self._ler_device_id()

    def _ler_device_id(self):
        if os.path.exists(DEVICE_PATH):
            with open(DEVICE_PATH, "r") as f:
                return f.read().strip()
        return "UNKNOWN_DEVICE"

    def enviar_dados(self):
        while True:
            dados = f"{self.numero_serial};Dispositivo online;{datetime.now(timezone.utc)}"
            texto_byte = bytes(dados, "utf-8")
            headers = {"Content-Type": "application/octet-stream"}
            
            try:
                resposta = requests.post(URL_SERVER, data=texto_byte, headers=headers)
                print(f"[Tracking] Dados enviados: {resposta.status_code} - {resposta.text}")
            except Exception as e:
                print(f"[Tracking] Falha ao enviar dados: {e}")

            time.sleep(120)
