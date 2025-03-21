import os
import time
import serial
import pynmea2
from datetime import datetime

INTERVALO_RETRY = 60
GPS_PADRAO = 'usb-u-blox_AG_-_www.u-blox.com_u-blox_7'
DEV_PATH = '/dev/serial/by-id'
GPS_FILE = '/tmp/gps_data.txt'

class GPS:
    def __init__(self):
        self.serial_port = serial.Serial()
        self.open_serial()

    def find_ublocx(self):
        """Encontra o dispositivo USB do GPS u-blox."""
        if not os.path.exists(DEV_PATH):
            return None
        
        dispositivos = os.listdir(DEV_PATH)
        for dev in dispositivos:
            if GPS_PADRAO in dev:
                return os.path.join(DEV_PATH, dev)
        return None

    def open_serial(self):
        """Abre a conexão serial com o GPS."""
        while True:
            dispositivo = self.find_ublocx()

            if dispositivo:
                try:
                    self.serial_port.port = dispositivo
                    self.serial_port.baudrate = 9600
                    self.serial_port.timeout = 1

                    if not self.serial_port.is_open:
                        self.serial_port.open()
                        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ✅ Conectado à porta {self.serial_port.port}.")
                        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Iniciando leitura...")
                        self.read_serial()  # Começa a ler os dados
                        return
                    
                except Exception as e:
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ❌ Erro ao abrir a porta serial: {e}")

            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 🔄 Dispositivo serial não encontrado. Tentando novamente em {INTERVALO_RETRY} segundos...")
            time.sleep(INTERVALO_RETRY)

    def read_serial(self):
        """Lê e processa os dados do GPS."""
        if not self.serial_port.is_open:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ❌ Erro: A porta serial não está aberta.")
            return

        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 📡 Esperando dados do GPS...")

        try:
            while True:
                linha = self.serial_port.readline().decode('utf-8', errors='ignore').strip()
                if linha.startswith("$GPGGA"):  # Apenas processa sentenças GPGGA
                    self.process_gpgga(linha)

        except KeyboardInterrupt:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 🛑 Leitura interrompida pelo usuário.")

    def process_gpgga(self, linha):
        """Processa a linha GPGGA e grava no arquivo caso os dados sejam válidos."""
        try:
            msg = pynmea2.parse(linha)

            if msg.gps_qual > 0:  # Verifica se há um fix válido
                lat = msg.latitude
                lon = msg.longitude
                alt = msg.altitude
                hora = msg.timestamp.strftime('%H:%M:%S')

                dados_gps = f"{datetime.now().strftime('%Y-%m-%d')} {hora} | Lat: {lat} | Lon: {lon} | Alt: {alt}m\n"

                # Grava no arquivo
                with open(GPS_FILE, 'w') as f:
                    f.write(dados_gps)

                print(f"📍 Dados válidos gravados: {dados_gps.strip()}")

            else:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 🚫 Sem fix válido.")

        except pynmea2.ParseError:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ❌ Erro ao interpretar os dados NMEA.")

if __name__ == "__main__":
    GPS()
