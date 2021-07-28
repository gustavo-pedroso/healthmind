from switch import Switch
from dht_sensor import DHTSensor
from datetime import datetime


class Incubator:

    def __init__(self, sensor_gpio_number, switch_gpio_number, target_temperature):
        self.sensor = DHTSensor(sensor_gpio_number)
        self.switch = Switch(switch_gpio_number)
        self.target_temperature = target_temperature

    def set_temperature(self, target_temperature):
        self.target_temperature = target_temperature

    def monitor(self, log_file=None):
        temperature = self.sensor.read()['temperature']
        if temperature < self.target_temperature:
            self.switch.on()
        elif temperature >= self.target_temperature:
            self.switch.off()

        print(f'current temperature: {temperature}°C / target temperature {self.target_temperature}°C')
        print(f'heater state: {self.switch.get_state()}')
        if log_file:
            with open(log_file, 'w+') as f:
                t = datetime.now().isoformat()
                f.write(f'{t} - {temperature}/{self.target_temperature}/{self.switch.get_state()}\n')
