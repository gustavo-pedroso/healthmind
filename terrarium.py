from switch import Switch
from dht_sensor import DHTSensor
from datetime import datetime
import time


class Terrarium:

    def __init__(self, sensor_gpio, humidifier_gpio, fans_gpio, heaters_gpio, lights_gpio, target_temperature,
                 target_humidity, fans_active_time, fans_hours, lights_ranges, update_time):
        self.sensor = DHTSensor(sensor_gpio)
        self.humidifier = Switch(humidifier_gpio)
        self.fans = Switch(fans_gpio)
        self.heaters = Switch(heaters_gpio)
        self.lights = Switch(lights_gpio)
        self.target_temperature = target_temperature
        self.target_humidity = target_humidity
        self.fans_active_time = fans_active_time
        self.fans_hours = fans_hours
        self.lights_ranges = lights_ranges
        self.update_time = update_time
        self.fan_start = -9999999

    def monitor(self, log_file=None):
        sensor_data = self.sensor.read()
        temperature = sensor_data['temperature']
        humidity = sensor_data['humidity']

        # monitor temperature
        if temperature < self.target_temperature:
            self.heaters.on()
        else:
            self.heaters.off()

        # monitor humidity
        if humidity < self.target_humidity:
            self.humidifier.on()
        else:
            self.humidifier.off()

        # monitor fans activation cycles
        if datetime.now().hour in self.fans_hours:
            self.fans.on()
            self.fans_hours.remove(datetime.now().hour)
            self.fan_start = int(time.time())
        if int(time.time()) - self.fan_start >= self.fans_active_time:
            self.fans.off()
            self.fan_start = -999999

        # monitor lights activation cycles
        for start, end in self.lights_ranges:
            if datetime.now().hour in range(start, end):
                self.lights.on()
            else:
                self.lights.off()

        print(f'temperature: {temperature} / {self.target_temperature} | heater: {self.heaters.get_state()} | ', end='')
        print(f'humidity: {humidity} / {self.target_temperature} | humidifier: {self.humidifier.get_state()}')

        if log_file:
            with open(log_file, 'a+') as f:
                t = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                f.write(f'{t} - temperature: {temperature} / {self.target_temperature} | ')
                f.write(f'humidity: {humidity} / {self.target_humidity} | ')
                f.write(f'heaters: {self.heaters.get_state()} | ')
                f.write(f'humidifier: {self.humidifier.get_state()} | ')
                f.write(f'lights: {self.lights.get_state()} | ')
                f.write(f'fans: {self.fans.get_state()}\n')
