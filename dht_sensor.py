import Adafruit_DHT


class DHTSensor:

    def __init__(self, gpio_number):
        self.gpio_number = gpio_number

        self.min_t = -2.0
        self.max_t = 52.0
        self.min_h = 15.0
        self.max_h = 95.0

    def read(self):
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(11, self.gpio_number)
            if self.min_t <= temperature <= self.max_t and self.min_h <= humidity <= self.max_h:
                return {'humidity': humidity, 'temperature': temperature}
