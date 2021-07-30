from terrarium import Terrarium
import time
import sys


start_time = int(time.time())
current_time = int(time.time())

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


while current_time - start_time < 86400 - terrarium.update_time:
    terrarium.monitor(sys.argv[1], sys.argv[2])
    time.sleep(terrarium.update_time)
    current_time = int(time.time())
