import os
import time
import serial
from datetime import datetime


INTERVALO_RETRY = 60
GPS_PADRAO = 'usb-u-blox_AG_-_www.u-blox.com_u-blox_7'
DEV_PATH = '/dev/serial/by-id'

class gps():
    def __init__(self):
        self.serial_port = serial.Serial()   
        self.open_serial()

    def find_ublocx(self):
        if not os.path.exists(DEV_PATH):            
            return None

        dispositivos = os.listdir(DEV_PATH)
        for dev in dispositivos:
            if GPS_PADRAO in dev:
                return os.path.join(DEV_PATH, dev)
        return None

    def open_serial(self):
        while True:
            dispositivo = self.find_ublocx()

            if dispositivo:
                try:
                    self.serial_port.port = dispositivo
                    self.serial_port.baudrate = 9600
                    self.serial_port.timeout = 1

                    if not self.serial_port.is_open:
                        self.serial_port.open()
                        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ✅Conectado à porta {self.serial_port.port}.")
                        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Iniciando leitura...")
                        self.read_serial()  # Sai do loop de conexão e começa a ler os dados
                        return
                    
                except Exception as e:
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ❌Erro ao abrir a porta serial: {e}")

            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 🔄 Dispositivo serial não encontrado. Tentando novamente em {INTERVALO_RETRY} segundos...")
            time.sleep(INTERVALO_RETRY)

    def read_serial(self):
        if not self.serial_port.is_open:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Erro: A porta serial não está aberta.")
            return
         
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Esperando dados na serial")

        try:
            while True:
                linha = self.serial_port.readline().decode('utf-8', errors='ignore').strip()
                if linha:
                    print(linha)                

        except KeyboardInterrupt:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Leitura interrompida pelo usuário.")


    