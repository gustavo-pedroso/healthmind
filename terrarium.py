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

    def monitor(self, log_file=None):
        sensor_data = self.sensor.read()
        temperature = sensor_data['temperature']
        humidity = sensor_data['humidity']

        if temperature < self.target_temperature:
            self.heaters.on()
        else:
            self.heaters.off()

        if humidity < self.target_humidity:
            self.humidifier.on()
        else:
            self.humidifier.off()

        print(f'current temperature: {temperature}°C / target temperature {self.target_temperature}°C')
        print(f'heaters state: {self.heaters.get_state()}')

        print(f'current humidity: {humidity}% / target humidity {self.target_temperature}%')
        print(f'humidifier state: {self.humidifier.get_state()}')

        if log_file:
            with open(log_file, 'a+') as f:
                t = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                f.write(f'{t} - {temperature} / {self.target_temperature} / {self.heaters.get_state()}\n')
                f.write(f'{t} - {humidity} / {self.target_humidity} / {self.humidifier.get_state()}\n')