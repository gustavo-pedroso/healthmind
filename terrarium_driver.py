from terrarium import Terrarium
from project_utils import kill_previous_from_file
import time
import sys

kill_previous_from_file("/home/pi/Documents/healthmind/terrarium_last_pid.tmp")

terrarium = Terrarium(sensor_gpio=[16, 13],
                      humidifier_gpio=18,
                      fans_gpio=23,
                      heaters_gpio=25,
                      lights_gpio=12,
                      target_temperature=25,
                      target_humidity=85,
                      fans_active_time=20,
                      fans_hours=list(range(0, 24)),
                      lights_ranges=[(8, 20)],
                      update_time=10,
                      email_notify_hours=list(range(0, 24)),
                      log_file='/home/pi/Documents/healthmind/terrarium_logs.txt',
                      json_email_info='/home/pi/Documents/healthmind/terrarium_email_info.json',
                      json_api_info='/home/pi/Documents/healthmind/api_info.json')

while True:
    terrarium.monitor()
    time.sleep(terrarium.update_time)
