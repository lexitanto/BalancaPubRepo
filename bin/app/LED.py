import RPi.GPIO as GPIO
import time
import threading

class LEDController:
    def __init__(self, pin=21):
        self.led_pin = pin
        self.blinking = False
        self.thread = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.led_pin, GPIO.OUT) 

    def _piscar_led(self, intervalo=1):
        while self.blinking:
            GPIO.output(self.led_pin, GPIO.HIGH)
            time.sleep(intervalo)
            GPIO.output(self.led_pin, GPIO.LOW)
            time.sleep(intervalo)

    def piscar_led(self, intervalo=1):
        if not self.blinking:
            self.blinking = True
            self.thread = threading.Thread(target=self._piscar_led, args=(intervalo,), daemon=True)
            self.thread.start()

    def parar_led(self):
        self.blinking = False
        if self.thread:
            self.thread.join(timeout=1)
        GPIO.output(self.led_pin, GPIO.LOW)

    def acender_led(self):
        self.parar_led()
        GPIO.output(self.led_pin, GPIO.HIGH)

    def desligar_led(self):
        self.parar_led()
        GPIO.output(self.led_pin, GPIO.LOW)

    def cleanup(self):
        self.parar_led()
        GPIO.cleanup()
