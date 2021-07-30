from switch import Switch
from dht_sensor import DHTSensor
from datetime import datetime


class Incubator:

    def __init__(self, sensor_gpio, heater_gpio, target_temperature):
        self.sensor = DHTSensor(sensor_gpio)
        self.heater = Switch(heater_gpio)
        self.target_temperature = target_temperature

    def set_temperature(self, target_temperature):
        self.target_temperature = target_temperature

    def monitor(self, log_file=None):
        temperature = self.sensor.read()['temperature']
        if temperature < self.target_temperature:
            self.heater.on()
        elif temperature >= self.target_temperature:
            self.heater.off()

        print(f'current temperature: {temperature}°C / target temperature {self.target_temperature}°C')
        print(f'heater state: {self.heater.get_state()}')
        if log_file:
            with open(log_file, 'a+') as f:
                t = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                f.write(f'{t} - {temperature} / {self.target_temperature} / {self.heater.get_state()}\n')
