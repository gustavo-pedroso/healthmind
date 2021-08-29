from incubator import Incubator

# create new Incubator with sensor, switch and target temperature
incubator = Incubator(sensor_gpio=[21, 26],
                      heater_gpio=20,
                      target_temperature=27.0,
                      update_time=5,
                      email_notify_hours=list(range(0, 24)),
                      log_file='/home/pi/Documents/healthmind/incubator_logs.txt',
                      json_email_info='/home/pi/Documents/healthmind/incubator_email_info.json',
                      json_api_info='/home/pi/Documents/healthmind/api_info.json')

if __name__ == "__main__":
    from project_utils import *
    import time

    kill_previous_from_file("/home/pi/Documents/healthmind/incubator_last_pid.tmp")
    while True:
        incubator.monitor()
        time.sleep(incubator.update_time)
