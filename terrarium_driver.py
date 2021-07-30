from terrarium import Terrarium
import time
import sys


start_time = int(time.time())
current_time = int(time.time())

terrarium = Terrarium(12, 25, 18, 24, 23, 30, 50)

terrarium.lights.on()
terrarium.fans.on()
while current_time - start_time < 590:
    terrarium.monitor(sys.argv[1])
    time.sleep(10)
    current_time = int(time.time())
