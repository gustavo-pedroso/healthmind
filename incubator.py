from switch import Switch
from dht_sensor import DHTSensor
from datetime import datetime
from email_util import EmailUtil


class Incubator:

    def __init__(self, sensor_gpio, heater_gpio, target_temperature, update_time, email_notify_hours):
        self.sensor = DHTSensor(sensor_gpio)
        self.heater = Switch(heater_gpio)
        self.target_temperature = target_temperature
        self.email_notify_hours = email_notify_hours
        self.update_time = update_time

    def set_temperature(self, target_temperature):
        self.target_temperature = target_temperature

    def monitor(self, json_email_info, log_file=None):
        temperature = self.sensor.read()['temperature']

        # monitor temperature
        if temperature < self.target_temperature:
            self.heater.on()
        else:
            self.heater.off()

        if json_email_info:
            if datetime.now().hour in self.email_notify_hours:
                self.email_notify_hours.remove(datetime.now().hour)
                email = EmailUtil(json_email_info)
                msg = f'Incubator Running OK\nTemperature: {temperature}\n'
                email.send_email(msg)

        print(f'temperature: {temperature} / {self.target_temperature} | heater: {self.heater.get_state()}')
        if log_file:
            with open(log_file, 'a+') as f:
                t = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                f.write(f'{t} - temperature: {temperature} / {self.target_temperature} | heater: {self.heater.get_state()}\n')
