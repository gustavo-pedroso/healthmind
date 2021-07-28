from switch import Switch
from dht_sensor import DHTSensor


class Incubator:

    def __init__(self, sensor_gpio_number, switch_gpio_number, target_temperature):
        self.sensor = DHTSensor(sensor_gpio_number)
        self.switch = Switch(switch_gpio_number)
        self.target_temperature = target_temperature

    def set_temperature(self, target_temperature):
        self.target_temperature = target_temperature

    def monitor(self):
        temperature = self.sensor.read()['temperature']
        print(f'current temperature: {temperature}°C / target temperature {self.target_temperature}°C')
        if temperature < self.target_temperature:
            self.switch.on()
        elif temperature >= self.target_temperature:
            self.switch.off()
        print(f'heater state: {self.switch.get_state()}')
