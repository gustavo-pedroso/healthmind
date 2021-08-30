from datetime import datetime
import signal
import os
import requests
import json


def kill_previous_from_file(file):
    try:
        with open(file, "r") as f:
            pid = f.read()
        os.kill(int(pid), signal.SIGTERM)
    except (ProcessLookupError, FileNotFoundError) as e:
        pass

    with open(file, "w+") as f:
        f.write(str(os.getpid()))


class FileLogger:

    def __init__(self, file):
        self.file = file
        self.log_buffer = []

    def log(self, log_message):
        if len(self.log_buffer) < 10:
            self.log_buffer.append(log_message)
        else:
            with open(self.file, 'a+') as f:
                f.writelines(self.log_buffer)
                self.log_buffer = []


def get_local_weather(api_info):
    with open(api_info) as fp:
        api_json = json.load(fp)

    response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={api_json['key']}&q={api_json['q']}")
    response = response.json()
    geo_temp = response['current']['temp_c']
    geo_humidity = response['current']['humidity']
    geo_location = response['location']['name']

    local_weather_message = f"\n\nCity Indicators: {geo_location}\n" \
                            f"Temperature: {geo_temp}°C\n" \
                            f"Humidity: {geo_humidity}%\n"
    return local_weather_message


def get_room_readings_message():
    from dht_sensor import DHTSensor
    sensor_data = DHTSensor(5).read()
    room_readings_message = f"\n\nRoom Indicators:\n" \
                            f"Temperature: {sensor_data['temperature']}°C\n" \
                            f"Humidity: {sensor_data['humidity']}%\n"
    return room_readings_message, sensor_data


def get_last_reboot_log_message():
    default_log_file = '/home/pi/Documents/healthmind/reboot_logs.txt'
    with open(default_log_file, 'r+') as f:
        last_reboot_log = f.readlines()[-1]
    last_reboot_log_message = f"Last Reboot log:\n{last_reboot_log}\n"
    return last_reboot_log_message


def read_sensors(sensors):
    temps = []
    humiditys = []
    for sensor in sensors:
        sensor_data = sensor.read()
        temps.append(sensor_data['temperature'])
        humiditys.append(sensor_data['humidity'])

    return {'temperature': float(sum(temps)/len(temps)),
            'humidity': float(sum(humiditys)/len(humiditys))}


def get_last_hour_stats(lines, hours, update_time):
    seconds_in_a_hour = 3600
    datapoints_in_a_hour = int(seconds_in_a_hour / update_time)
    total_datapoints = int(hours * datapoints_in_a_hour)
    total_datapoints = min(len(lines), total_datapoints)
    return lines[-total_datapoints:]


def safe_list_get(arr, idx, default):
    try:
        return arr[idx]
    except IndexError:
        return default


def log_reboot_causes(cause):
    default_log_file = '/home/pi/Documents/healthmind/reboot_logs.txt'
    t = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with open(default_log_file, 'a+') as f:
        f.write(f'{t}: {cause}\n')


def get_sentiment(target_t, target_h, temperature, humidity, tolerance):
    target_t = target_t if target_t else 1
    target_h = target_h if target_h else 1
    temperature = temperature if temperature else 1
    humidity = humidity if humidity else 1

    lower_tol = 1 - tolerance
    upper_tol = 1 + tolerance

    sentiment = 'NÃO TAMO BEM'
    if target_t * lower_tol < temperature < target_t * upper_tol:
        if target_h * lower_tol < humidity < target_h * upper_tol:
            sentiment = 'TAMO BEM'
    return sentiment


def get_temperature_offset(target_temperature, room_temperature):
    offset_ratio = 1 / 7
    temperature_offset = (room_temperature - target_temperature) * offset_ratio
    return temperature_offset if temperature_offset < 0 else 0
