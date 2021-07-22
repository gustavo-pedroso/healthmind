import sys
import DHTSensor

while True:
    result = DHTSensor.read(4)
    print(result)