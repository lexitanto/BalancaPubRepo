import os
import time
import serial
import getpass
import requests
from datetime import datetime
from connection import database_connection

#Constantes
CPU_NUMBER = ''
NUMERO_SERIAL = ''
DEVICE_MODEL = ''
SERIAL_FILE = '/etc/device_serial'
MAX_TENTATIVAS = 5        
INTERVALO_RETRY = 60
PROLIFIC_PADRAO = 'usb-Prolific_Technology_Inc._USB-Serial_Controller'
DEV_PATH = "/dev/serial/by-id"
URL_SERVER = 'https://9271-170-80-64-72.ngrok-free.app/IoT/Balanca'
URL_PAYLOAD = '/payload'
URL_EQUIPAMENTO = '/check_equipamento'
DB = database_connection()


class app_serial():
    def __init__(self):
        self.serial_port = serial.Serial()   
        self.check_equipamento()
        self.open_serial()
        
    def check_equipamento(self):
        global NUMERO_SERIAL
        global CPU_NUMBER
        global DEVICE_MODEL

        if os.path.exists(SERIAL_FILE):
            # Se o arquivo existe, lê o número serial armazenado
            with open(SERIAL_FILE, 'r') as f:
                NUMERO_EQUIPAMENTO = f.read().strip()
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Numero do equipamento carregado: {NUMERO_EQUIPAMENTO}")
        else:
            CPU_NUMBER = self.get_rpi_serial()
            DEVICE_MODEL = self.get_model()
            if CPU_NUMBER:
                try:
                    string_dados = f"{CPU_NUMBER};{DEVICE_MODEL}"
                    texto_byte = bytes(string_dados, 'utf-8')
                    response = self.POST_to_server(texto_byte, URL_EQUIPAMENTO)
                    if response:
                        NUMERO_EQUIPAMENTO = response.get("equipamento")

                        if NUMERO_EQUIPAMENTO:
                            with open(SERIAL_FILE, 'w') as f:
                                f.write(NUMERO_EQUIPAMENTO)
                            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Novo número serial obtido e salvo: {NUMERO_EQUIPAMENTO}")
                        else:
                            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Erro: Nenhum número serial retornado pela API.")

                except requests.RequestException as e:
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Erro ao fazer a requisição para a API: {e}")

            else:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Erro: Não foi possível obter o número serial da CPU.")

    def get_equipamento(self):
        return getpass.getuser()

    def get_rpi_serial(self):        
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if line.startswith("Serial"):
                        return line.strip().split(":")[1].strip()

        except Exception as e:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Erro ao ler o número de série: {e}")
            return None
        
    def get_model(self):
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if line.startswith("Model"):
                        return line.strip().split(":")[1].strip()

        except Exception as e:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Erro ao ler o número de série: {e}")
            return None

    def find_device(self):
        dispositivos = os.listdir(DEV_PATH)
        for dev in dispositivos:
            if PROLIFIC_PADRAO in dev:
                return os.path.join(DEV_PATH, dev)  # Retorna o caminho completo
        return None

    def open_serial(self):
        while True:
            dispositivo = self.find_device()      

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

            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 🔄Dispositivo não encontrado. Tentando novamente em {INTERVALO_RETRY} segundos...")
            time.sleep(INTERVALO_RETRY)

    def read_serial(self):
        if not self.serial_port.is_open:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Erro: A porta serial não está aberta.")
            return
         
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Esperando dados na serial")

        try:
            evento_balanca = eventos_balanca()
            while True:
                linha = self.serial_port.readline().decode('utf-8', errors='ignore').strip()
                if linha:
                    self.interpret_serial(linha, evento_balanca)                    

        except KeyboardInterrupt:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Leitura interrompida pelo usuário.")    

    def interpret_serial(self, linha, evento_balanca): 
        if '[h0][g0]' in linha:
            self.process_load(linha, evento_balanca)
        else:
            self.process_print(linha, evento_balanca)

    def process_load(self, linha, evento_balanca):
        print(f"Linha de CARREGAMENTO recebida: {linha}")
        data_Evento = datetime.now()
        evento_balanca.Cod_identificador = 1
        evento_balanca.Peso_atual = linha[25:30].lstrip('0')
        evento_balanca.Peso_total = linha[44:51].lstrip('0')
        evento_balanca.DataEvento = data_Evento.strftime("%Y-%m-%d %H:%M:%S")
                        
        string_dados =(f'{NUMERO_SERIAL};{evento_balanca.Cod_identificador};'
                       f'{evento_balanca.DataEvento};{evento_balanca.Peso_atual};'
                       f'{evento_balanca.Peso_total}')
                        
        texto_byte = bytes(string_dados, 'utf-8')
        self.POST_eventos(texto_byte, URL_PAYLOAD)

    def process_print(self, linha, evento_balanca):
        if 'PCS:' in linha:
            total_de_pesagens = linha.replace('PCS:', '').replace(' ', '')
            evento_balanca.Total_de_pesagens = total_de_pesagens
        elif 'TOT' in linha:
            peso_total = linha.replace('TOT:', '').replace('kg', '').replace(' ', '').lstrip('0')
            evento_balanca.Peso_total = peso_total    
        elif 'SET' in linha:
            peso_maximo = linha.replace('SET:', '').replace('kg', '').replace(' ', '') 
            evento_balanca.Peso_maximo = peso_maximo
        elif 'CAMINHAO' in linha:
            caminhao = linha.replace('CAMINHAO:', '').replace(' ', '')
            evento_balanca.Caminhao = caminhao
        elif 'MATERIAIS' in linha:
            material = linha.replace('MATERIAIS:', '').replace(' ', '')
            evento_balanca.Produto = material
        elif 'OPER' in linha:
            operador = linha.replace('OPER:', '').replace(' ', '')
            evento_balanca.Operador = operador
        elif 'HORA' in linha:
            hora = linha.replace('HORA:', '').replace(' ', '')
        elif 'DATA' in linha:
            data = linha.replace('DATA:', '').replace(' ', '')
        elif 'NO.' in linha:
            id_pesagem = linha.replace('NO.:', '').replace(' ', '')
            evento_balanca.Id_Pesagem = id_pesagem
        elif '----------------' not in linha and 'REGISTRO PESAGEM' not in linha and 'kg' not in linha:
            usuario = linha
            evento_balanca.Usuario = usuario
        elif 'REGISTRO PESAGEM' in linha:
            evento_balanca.Cod_identificador = 2
            data_Evento = datetime.now()
            evento_balanca.DataEvento = data_Evento.strftime("%Y-%m-%d %H:%M:%S")

            string_dados = ( f"{NUMERO_SERIAL};{evento_balanca.Cod_identificador};"
                             f"{evento_balanca.DataEvento};{evento_balanca.Peso_atual};"
                             f"{evento_balanca.Peso_total};{evento_balanca.Peso_maximo};"
                             f"{evento_balanca.Total_de_pesagens};{evento_balanca.Id_Pesagem};"
                             f"{evento_balanca.Usuario};{evento_balanca.Operador};"
                             f"{evento_balanca.Caminhao};{evento_balanca.Produto}"
                            )


            texto_byte = bytes(string_dados, 'utf-8')
            self.POST_eventos(texto_byte, URL_PAYLOAD)    

    def refatorar_eventos(self):
        registros = self.fetch_data()
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - registros: {registros}")

        if registros:
            for registro in registros:
                id_registro, data = registro
                response = self.POST_ultimasTransmissoes(data, URL_PAYLOAD)
                if not response:
                    break

                self.delete_data(id_registro)
    
    def POST_eventos(self, data, api_url):
        self.refatorar_eventos()
 
        try:            
            headers = {"Content-Type": "application/octet-stream"}
            endpoint = URL_SERVER + api_url
            response = requests.post(endpoint, data=data, headers=headers)
            json_data = response.json() if response.headers.get("Content-Type") == "application/json" else None

            if response.ok:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ✅Sucesso! Eventos enviados      -> {json_data}")
            else:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ❌Erro: {response.status_code}      -> {json_data}")
                self.salvar_ultimaTransmissao(data)

        except Exception as e:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Erro ao enviar dados ao servidor: {e}")

    def POST_ultimasTransmissoes(self, data, api_url):
        try:            
            headers = {"Content-Type": "application/octet-stream"}
            endpoint = URL_SERVER + api_url
            response = requests.post(endpoint, data=data, headers=headers)
            json_data = response.json() if response.headers.get("Content-Type") == "application/json" else None

            if response.ok:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ✅Sucesso! Eventos enviados      -> {json_data}")
                return True
            else:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ❌Erro: {response.status_code}      -> {json_data}")

        except Exception as e:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Erro ao enviar dados ao servidor: {e}")

    def POST_to_server(self, data, api_url):
        tentativas = 0

        while tentativas <= MAX_TENTATIVAS:
            try:            
                headers = {"Content-Type": "application/octet-stream"}
                endpoint = URL_SERVER + api_url
                response = requests.post(endpoint, data=data, headers=headers)
                json_data = response.json()

                if response.ok:
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ✅Sucesso no POST!      -> {response.json()}")
                    return json_data
                else:
                    tentativas += 1
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ❌Erro: {response.status_code}      -> {json_data}")
                    if tentativas < MAX_TENTATIVAS:
                        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Tentativa {tentativas}/{MAX_TENTATIVAS}. Nova tentativa em {INTERVALO_RETRY} segundos...")
                        time.sleep(INTERVALO_RETRY)             

            except Exception as e:
                tentativas += 1
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ❌Erro ao enviar dados ao servidor: {e}")
                if tentativas < MAX_TENTATIVAS:
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Tentativa {tentativas}/{MAX_TENTATIVAS}. Nova tentativa em {INTERVALO_RETRY} segundos...")
                    time.sleep(INTERVALO_RETRY)

    def salvar_ultimaTransmissao(self, data):
        with DB:
            DB.salvar_transmissoes(data)

    def fetch_data(self):
        with DB:
            registros = DB.connect_to_db()
            return registros
        
    def delete_data(self, id):
        with DB:
            DB.delete_at_index(id)        

class eventos_balanca:
    def __init__(self):
        self.Peso_atual = None
        self.Peso_total = None
        self.Operador = None
        self.Caminhao = None
        self.Produto = None
        self.DataEvento = None
        self.Total_de_pesagens = None
        self.Usuario = None
        self.Id_Pesagem = None
        self.Cod_identificador = None
        self.Peso_maximo = None
        

    # def send_serial(self, data):
    #     dado_send = str(data)+'\n'
    #     self.serial_port.write(dado_send.encode())
    #     self.serial_port.flushOutput()

    # def close_serial(self):
    #     if self.serial_port.is_open:
    #         self.serial_port.close()
    #         print("Porta serial fechada.")
    #     else:
    #         print("A porta já está fechada.")