import dht_sensor
import rele


# sensor = dht_sensor.DHTSensor(4)
# while True:
#     result = sensor.read()
#     print(result)


rele = rele.Rele(17)

while True:
    a = input()
    a = int(a)
    if a == 0:
        rele.off()
    elif a == 1:
        rele.on()
