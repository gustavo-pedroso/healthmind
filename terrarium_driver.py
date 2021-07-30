from terrarium import Terrarium
from project_utils import kill_previous_from_file
import time
import sys

kill_previous_from_file("/home/pi/Documents/healthmind/terrarium_last_pid.tmp")

terrarium = Terrarium(sensor_gpio=12,
                      humidifier_gpio=25,
                      fans_gpio=18,
                      heaters_gpio=24,
                      lights_gpio=23,
                      target_temperature=30,
                      target_humidity=50,
                      fans_active_time=30,
                      fans_hours=[0, 8, 16],
                      lights_ranges=[(20, 8)],
                      update_time=10,
                      email_notify_hours=list(range(0, 24)))

while True:
    terrarium.monitor(sys.argv[1], sys.argv[2])
    time.sleep(terrarium.update_time)
