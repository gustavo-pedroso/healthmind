import os
from project_utils import log_reboot_causes
from gpiozero import LED
import time


class Switch:

    def __init__(self, gpio_number):
        self.gpio_number = gpio_number
        self.switch = LED(self.gpio_number)
        self.switch.off()

    def on(self):
        retry = 0
        self.switch.on()
        while self.get_state() != 'ON' and retry < 3:
            self.switch.on()
            retry += 1
            time.sleep(0.5)

        if self.get_state() != 'ON':
            log_reboot_causes('get_state != ON after setting to ON')
            os.system('sudo reboot')

    def off(self):
        retry = 0
        self.switch.off()
        while self.get_state() != 'OFF' and retry < 3:
            self.switch.off()
            retry += 1
            time.sleep(0.5)

        if self.get_state() != 'OFF':
            log_reboot_causes('get_state != OFF after setting to OFF')
            os.system('sudo reboot')

    def get_state(self):
        if self.switch.is_lit:
            return 'ON'
        else:
            return 'OFF'
