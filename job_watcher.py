import os


class JobWatcher:
    def __init__(self, job_names):
        self.job_names = job_names

    @staticmethod
    def reboot():
        os.system('sudo reboot')

    def scan(self):
        running = str(os.popen('ps -aux').read())
        for name in self.job_names:
            if name not in running:
                self.reboot()


if __name__ == '__main__':
    job_watcher = JobWatcher(['incubator_driver.py',
                              'terrarium_driver.py'])
    job_watcher.scan()
