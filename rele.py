from gpiozero import LED


class Rele:

    def __init__(self, gpio_number):
        self.gpio_number = gpio_number
        self.rele = LED(self.gpio_number)

    def on(self):
        self.rele.on()

    def off(self):
        self.rele.off()
