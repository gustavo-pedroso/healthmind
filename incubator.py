from switch import Switch
from dht_sensor import DHTSensor
from datetime import datetime
from email_util import EmailUtil
from project_utils import *


class Incubator:

    def __init__(self, sensor_gpio, heater_gpio, target_temperature, update_time, email_notify_hours, log_file,
                 json_email_info, json_api_info):

        self.sensor = DHTSensor(sensor_gpio)
        self.heater = Switch(heater_gpio)
        self.target_temperature = target_temperature
        self.email_notify_hours = email_notify_hours
        self.update_time = update_time
        self.log_buffer = []
        self.log_file = log_file
        self.json_email_info = json_email_info
        self.json_api_info = json_api_info

        if self.log_file:
            self.file_logger = FileLogger(self.log_file)

    def monitor(self):
        temperature = self.sensor.read()['temperature']
        heater_state = self.heater.get_state()

        # monitor temperature
        if temperature < self.target_temperature:
            if heater_state == 'OFF':
                self.heater.on()
            else:
                self.heater.off()
        else:
            self.heater.off()

        if self.json_email_info:
            if datetime.now().hour in self.email_notify_hours:
                self.email_notify_hours.remove(datetime.now().hour)
                email = EmailUtil(self.json_email_info, self.json_api_info)
                msg = f'Incubator Running OK\nTemperature: {temperature}°C\n'
                email.send_email(msg)

        print(f'temperature: {temperature} / {self.target_temperature} | heater: {heater_state}')
        if self.log_file:
            t = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            log_message = f'{t} - temperature: {temperature} / {self.target_temperature} | heater: ' \
                          f'{heater_state}\n'

            self.file_logger.log(log_message)
