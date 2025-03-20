import RPi.GPIO as GPIO
import time
import sys

class LEDController:
    def __init__(self, pin=17):
        self.led_pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.led_pin, GPIO.OUT)
    
    def piscar_led(self, intervalo=1):
        """Pisca o LED em intervalos definidos."""
        try:
            while True:
                GPIO.output(self.led_pin, GPIO.HIGH)
                time.sleep(intervalo)
                GPIO.output(self.led_pin, GPIO.LOW)
                time.sleep(intervalo)
        except KeyboardInterrupt:
            self.cleanup()
    
    def acender_led(self):
        """Liga o LED."""
        GPIO.output(self.led_pin, GPIO.HIGH)
    
    def desligar_led(self):
        """Desliga o LED."""
        GPIO.output(self.led_pin, GPIO.LOW)
    
    def cleanup(self):
        """Libera os recursos do GPIO."""
        GPIO.cleanup()

# Inicia o controle do LED
if __name__ == "__main__":
    controller = LEDController()
    if len(sys.argv) > 1 and sys.argv[1] == "piscar":
        controller.piscar_led()  # Começa a piscar o LED
    else:
        controller.acender_led()  # Mantém o LED aceso
