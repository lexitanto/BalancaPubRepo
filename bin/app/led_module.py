# led_module.py
import RPi.GPIO as GPIO
import time
from datetime import datetime

class led():
    def __init__(self, pin=21):
        self.led_pin = pin
        self.blinking = False
        self.setup_gpio()

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.led_pin, GPIO.OUT)

    def _piscar_led(self, intervalo=1):
        while self.blinking:
            GPIO.output(self.led_pin, GPIO.HIGH)
            time.sleep(intervalo)
            GPIO.output(self.led_pin, GPIO.LOW)
            time.sleep(intervalo)

    def run(self):
        """
        Exemplo de loop do LED.
        Aqui você pode, por exemplo, piscar o LED enquanto nenhum dado válido for recebido,
        ou seguir outro critério definido pela aplicação.
        """
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - [LED] Loop iniciado.")
        # Exemplo: piscar o LED a cada 0.5 segundos.
        self.start_blinking(intervalo=0.5)
        try:
            while True:
                # Este loop pode ser usado para atualizar o estado do LED com base em eventos externos.
                time.sleep(1)
        except KeyboardInterrupt:
            self.cleanup()

    def start_blinking(self, intervalo=1):
        """Inicia o piscar do LED em uma thread separada (se necessário)."""
        if not self.blinking:
            self.blinking = True
            from threading import Thread
            t = Thread(target=self._piscar_led, args=(intervalo,), daemon=True)
            t.start()

    def acender_led(self):
        """Acende o LED de forma contínua."""
        self.stop_blinking()
        GPIO.output(self.led_pin, GPIO.HIGH)

    def desligar_led(self):
        """Desliga o LED."""
        self.stop_blinking()
        GPIO.output(self.led_pin, GPIO.LOW)

    def stop_blinking(self):
        """Para o piscar do LED."""
        self.blinking = False

    def cleanup(self):
        """Finaliza e limpa a configuração do GPIO."""
        self.stop_blinking()
        GPIO.cleanup()
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - [LED] GPIO limpo e LED desligado.")
