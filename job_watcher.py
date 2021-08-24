import os
import time
from datetime import datetime


class JobWatcher:
    def __init__(self, job_names, files_names):
        self.job_names = job_names
        self.file_names = files_names

    @staticmethod
    def reboot():
        os.system('sudo reboot')

    def scan(self):
        running = str(os.popen('ps -aux').read())
        for name in self.job_names.keys():
            if running.count(name) < self.job_names[name]:
                print(f'ops :| linux says we are missing some required processes. Rebooting :(')
                self.reboot()

        for name in self.file_names:
            last_modified_date = int(os.path.getmtime(name))
            now = int(time.time())
            last_modified_date_ts = datetime.fromtimestamp(last_modified_date).strftime('%Y-%m-%d %H:%M:%S')
            print(f'{name} was last modified at: {last_modified_date_ts}')
            if now - last_modified_date > 60 * 30:
                print(f'{name} was not updated in the last 30min, rebooting :/')
                self.reboot()


if __name__ == '__main__':
    job_watcher = JobWatcher(job_names={'terrarium_driver.py': 2, 'incubator_driver.py': 2},
                             files_names=['/home/pi/Documents/healthmind/incubator_logs.txt',
                                          '/home/pi/Documents/healthmind/terrarium_logs.txt'])
    job_watcher.scan()
