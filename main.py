import dht_sensor


sensor = dht_sensor.DHTSensor(4)
while True:
    result = sensor.read()
    print(result)
    print('bla')

