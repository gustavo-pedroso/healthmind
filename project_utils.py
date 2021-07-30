import signal
import os
import requests
import json


def kill_previous_from_file(file):
    try:
        with open(file, "r") as f:
            pid = f.read()
        os.kill(int(pid), signal.SIGTERM)
    except ProcessLookupError as e:
        pass

    with open(file, "w+") as f:
        f.write(str(os.getpid()))


class FileLogger:

    def __init__(self, file):
        self.file = file
        self.log_buffer = []

    def log(self, log_message):
        if len(self.log_buffer) <= 100:
            self.log_buffer.append(log_message)
        else:
            with open(self.file, 'a+') as f:
                f.writelines(self.log_buffer)
                self.log_buffer = []


def get_local_weather(api_info):
    with open(api_info) as fp:
        api_json = json.load(fp)

    response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={api_json['key']}&q={api_json['q']}")
    geo_temp = response['current']['temp_c']
    geo_humidity = response['current']['humidity']
    geo_location = response['location']['name']

    local_weather_message = f"\n\nLocation: {geo_location}\n" \
                            f"Temperature: {geo_temp}°C\n" \
                            f"Humidity: {geo_humidity}%"
    return local_weather_message
