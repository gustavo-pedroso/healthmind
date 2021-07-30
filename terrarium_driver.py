from terrarium import Terrarium
import time


terrarium = Terrarium(12, 25, 18, 25, 24, 30, 50)

terrarium.heaters.on()
terrarium.fans.on()
terrarium.lights.on()
terrarium.humidifier.on()

time.sleep(10)
