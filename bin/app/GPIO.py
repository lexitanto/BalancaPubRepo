import RPi.GPIO as GPIO
import time

# Define o modo de numeração (BCM ou BOARD)
GPIO.setmode(GPIO.BCM)  

# Define os pinos
LED_PIN = 18

# Configuração dos pinos
GPIO.setup(LED_PIN, GPIO.OUT)       # Saída para LED

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Liga o LED        
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(2)

except KeyboardInterrupt:
    print("\nSaindo...")
    GPIO.cleanup()  # Libera os pinos GPIO
