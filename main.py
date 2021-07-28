import dht_sensor
import switch
from incubator import Incubator
import time


# sensor = dht_sensor.DHTSensor(17)
# while True:
#     result = sensor.read()
#     print(result)


# rele = switch.Switch(17)
#
# while True:
#     a = input()
#     a = int(a)
#     if a == 0:
#         rele.off()
#     elif a == 1:
#         rele.on()
#     print(a)

incubator = Incubator(18, 23, 30)

while True:
    incubator.monitor()
    time.sleep(3)
