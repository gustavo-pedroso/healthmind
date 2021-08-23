import os
import time


class JobWatcher:
    def __init__(self, job_names, files_names):
        self.job_names = job_names
        self.file_names = files_names

    @staticmethod
    def reboot():
        os.system('sudo reboot')

    def scan(self):
        running = str(os.popen('ps -aux').read())
        for name in self.job_names:
            if name not in running:
                self.reboot()

        for name in self.file_names:
            if int(time.time()) - int(os.path.getmtime(name)) > 30 * 60:
                self.reboot()


if __name__ == '__main__':
    job_watcher = JobWatcher(job_names=['/bin/sh -c sleep 60 && python3 /home/pi/Documents/healthmind/incubator_driver.py',
                              '/bin/sh -c sleep 60 && python3 /home/pi/Documents/healthmind/terrarium_driver.py',
                              'python3 /home/pi/Documents/healthmind/incubator_driver.py',
                              'python3 /home/pi/Documents/healthmind/terrarium_driver.py'],
                             files_names=['/home/pi/Documents/healthmind/incubator_logs.txt',
                                          '/home/pi/Documents/healthmind/terrarium_logs.txt'])
    job_watcher.scan()
