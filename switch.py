import os
from gpiozero import LED


class Switch:

    def __init__(self, gpio_number):
        self.gpio_number = gpio_number
        self.switch = LED(self.gpio_number)
        self.switch.off()

    def on(self):
        self.switch.on()
        if self.get_state() != 'ON':
            os.system('sudo reboot')

    def off(self):
        self.switch.off()
        if self.get_state() != 'OFF':
            os.system('sudo reboot')

    def get_state(self):
        if self.switch.is_lit:
            return 'ON'
        else:
            return 'OFF'
