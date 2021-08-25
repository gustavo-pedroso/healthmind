import os
from project_utils import log_reboot_causes
from gpiozero import LED


class Switch:

    def __init__(self, gpio_number):
        self.gpio_number = gpio_number
        self.switch = LED(self.gpio_number)
        self.switch.off()

    def on(self):
        self.switch.on()
        if self.get_state() != 'ON':
            log_reboot_causes('get_state != ON after setting to ON')
            os.system('sudo reboot')

    def off(self):
        self.switch.off()
        if self.get_state() != 'OFF':
            log_reboot_causes('get_state != OFF after setting to OFF')
            os.system('sudo reboot')

    def get_state(self):
        if self.switch.is_lit:
            return 'ON'
        else:
            return 'OFF'
