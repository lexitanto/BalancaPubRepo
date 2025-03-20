import RPi.GPIO as GPIO
import time
import sys

# Configuração do GPIO
GPIO.setmode(GPIO.BCM)  # Usa a numeração BCM dos pinos
GPIO.setwarnings(False)

# Defina o pino que você conectou o LED
led_pin = 17  # Exemplo: GPIO17

# Configura o pino do LED como saída
GPIO.setup(led_pin, GPIO.OUT)

# Função para piscar o LED
def piscar_led():
    while True:
        GPIO.output(led_pin, GPIO.HIGH)  # Liga o LED
        time.sleep(1)  # Aguarda 1 segundo
        GPIO.output(led_pin, GPIO.LOW)   # Desliga o LED
        time.sleep(1)  # Aguarda 1 segundo

# Função para manter o LED aceso
def acender_led():
    GPIO.output(led_pin, GPIO.HIGH)

# Função para desligar o LED
def desligar_led():
    GPIO.output(led_pin, GPIO.LOW)

# Inicia o controle do LED
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "piscar":
        piscar_led()  # Começa a piscar o LED
    else:
        acender_led()  # Mantém o LED aceso