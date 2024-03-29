from switch import Switch
from dht_sensor import DHTSensor
from email_util import EmailUtil
from datetime import datetime
from project_utils import *
import time


class Terrarium:

    def __init__(self, sensor_gpio, humidifier_gpio, fans_gpio, heaters_gpio, lights_gpio, target_temperature,
                 target_humidity, humidity_cycles, fans_active_time, fans_hours, lights_ranges, update_time, email_notify_hours,
                 log_file, json_email_info, json_api_info):

        self.sensor = [DHTSensor(pin) for pin in sensor_gpio]
        self.humidifier = Switch(humidifier_gpio)
        self.fans = Switch(fans_gpio)
        self.heaters = Switch(heaters_gpio)
        self.lights = Switch(lights_gpio)
        self.target_temperature = target_temperature
        self.target_humidity = target_humidity
        self.humidity_cycles = humidity_cycles
        self.fans_active_time = fans_active_time
        self.fans_hours = fans_hours
        self.lights_ranges = lights_ranges
        self.update_time = update_time
        self.email_notify_hours = email_notify_hours
        self.fan_start = -9999999
        self.log_file = log_file
        self.json_email_info = json_email_info
        self.json_api_info = json_api_info
        self.cycles_on = 0
        self.cycles_off = 0

        if self.log_file:
            self.file_logger = FileLogger(self.log_file)

    def monitor(self):
        sensor_data = read_sensors(self.sensor)
        temperature = sensor_data['temperature']
        humidity = sensor_data['humidity']
        heaters_state = self.heaters.get_state()
        humidifier_state = self.humidifier.get_state()
        lights_state = self.lights.get_state()
        fans_state = self.fans.get_state()

        # monitor temperature
        if temperature < self.target_temperature:
            self.heaters.on()
        else:
            self.heaters.off()

        # monitor humidity
        # if humidity < self.target_humidity:
        #     self.humidifier.on()
        # else:
        #     self.humidifier.off()

        if self.cycles_on < self.humidity_cycles:
            self.cycles_on += 1
            self.humidifier.on()
        else:
            self.cycles_off += 1
            self.humidifier.off()
            if self.cycles_off > 100 - self.humidity_cycles:
                self.cycles_off = 0
                self.cycles_on = 0

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
            if start > end:
                r = list(range(start, 24)) + list(range(0, end))
            else:
                r = range(start, end)
            if datetime.now().hour in r:
                self.lights.on()
            else:
                self.lights.off()

        if self.json_email_info:
            if datetime.now().hour in self.email_notify_hours:
                time.sleep(30)
                self.email_notify_hours.remove(datetime.now().hour)
                email = EmailUtil(self.json_email_info, self.json_api_info)

                msg = f"Terrarium Indicators:\n" \
                      f"Temperature: {temperature}°C, target: {self.target_temperature}°C\n" \
                      f"Humidity: {humidity}%, target: {self.target_humidity}%\n" \
                      f"Terrarium Devices:\n" \
                      f"Heaters: {self.heaters.get_state()}\n" \
                      f"Humidifier: {self.humidifier.get_state()}\n" \
                      f"Lights: {self.lights.get_state()}\n" \
                      f"Fans: {self.fans.get_state()}\n"

                sentiment = get_sentiment(self.target_temperature, self.target_humidity, temperature, humidity, 0.1)
                email.send_email(msg, sentiment)

        print(f'temperature: {temperature} / {self.target_temperature} | heater: {heaters_state} | ', end='')
        print(f'humidity: {humidity} / {self.target_humidity} | humidifier: {humidifier_state}')

        if self.log_file:
            t = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            log_message = f'{t} - temperature: {temperature} / {self.target_temperature} | ' \
                          f'humidity: {humidity} / {self.target_humidity} | ' \
                          f'heaters: {heaters_state} | ' \
                          f'humidifier: {humidifier_state} | ' \
                          f'lights: {lights_state} | ' \
                          f'fans: {fans_state}\n'

            self.file_logger.log(log_message)

