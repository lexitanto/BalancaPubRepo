# hardware_module.py
import os
import time
import serial
from datetime import datetime

# Configurações – ajuste conforme seu dispositivo
PROLIFIC_PADRAO = 'usb-Prolific_Technology_Inc._USB-Serial_Controller'
DEV_PATH = '/dev/serial/by-id'
INTERVALO_RETRY = 60

class balanca():
    def __init__(self):
        self.serial_port = serial.Serial()
        self.find_and_open_serial()

    def find_and_open_serial(self):
        while True:
            dispositivo = self.find_prolific()
            if dispositivo:
                try:
                    self.serial_port.port = dispositivo
                    self.serial_port.baudrate = 9600
                    self.serial_port.timeout = 1
                    if not self.serial_port.is_open:
                        self.serial_port.open()
                        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - [Balanca] Conectado à porta {self.serial_port.port}.")
                        return
                except Exception as e:
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - [Balanca] Erro ao abrir a porta serial: {e}")
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - [Balanca] Dispositivo serial não encontrado. Tentando novamente em {INTERVALO_RETRY} segundos...")
            time.sleep(INTERVALO_RETRY)

    def find_prolific(self):
        if not os.path.exists(DEV_PATH):
            return None
        dispositivos = os.listdir(DEV_PATH)
        for dev in dispositivos:
            if PROLIFIC_PADRAO in dev:
                return os.path.join(DEV_PATH, dev)
        return None

    def run(self):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - [Balanca] Iniciando leitura dos dados...")
        while True:
            try:
                linha = self.serial_port.readline().decode('utf-8', errors='ignore').strip()
                if linha:
                    self.process_line(linha)
            except Exception as e:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - [Balanca] Erro na leitura: {e}")

    def process_line(self, linha):
        """Processa a linha recebida – implemente sua lógica de negócio aqui."""
        # Exemplo simples de interpretação:
        print(f"[Balanca] Linha recebida: {linha}")
        # Aqui você pode separar comandos, extrair dados e eventualmente enviar para um servidor ou salvar em um banco de dados.
