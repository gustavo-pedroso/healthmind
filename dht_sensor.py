import Adafruit_DHT


class DHTSensor:

    def __init__(self, gpio_number):
        self.gpio_number = gpio_number

    def read(self):
        humidity, temperature = Adafruit_DHT.read_retry(11, self.gpio_number)
        return {'humidity': humidity, 'temperature': temperature}
