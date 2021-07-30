from switch import Switch
from dht_sensor import DHTSensor
from datetime import datetime


class Terrarium:

    def __init__(self, sensor_gpio, humidifier_gpio, fans_gpio, heaters_gpio, lights_gpio, target_temperature, target_humidity):
        self.sensor = DHTSensor(sensor_gpio)
        self.humidifier = Switch(humidifier_gpio)
        self.fans = Switch(fans_gpio)
        self.heaters = Switch(heaters_gpio)
        self.lights = Switch(lights_gpio)
        self.target_temperature = target_temperature
        self.target_humidity = target_humidity

    