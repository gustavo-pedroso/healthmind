from gpiozero import LED


class Switch:

    def __init__(self, gpio_number):
        self.gpio_number = gpio_number
        self.switch = LED(self.gpio_number)

    def on(self):
        self.switch.on()

    def off(self):
        self.switch.off()

    def get_state(self):
        if self.switch.is_lit():
            return 'ON'
        else:
            return 'OFF'
