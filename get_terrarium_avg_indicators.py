from project_utils import get_last_hour_stats
from terrarium_driver import terrarium
import statistics
import sys

with open('/home/pi/Documents/healthmind/terrarium_logs.txt') as log_file:
    lines = log_file.readlines()

if len(sys.argv) > 1:
    lines = get_last_hour_stats(lines, int(sys.argv[1]), terrarium.update_time)
else:
    lines = get_last_hour_stats(lines, 24, terrarium.update_time)

temps = [float(t.split(' ')[4]) for t in lines]
humiditys = [float(t.split(' ')[9]) for t in lines]
state_heaters = [t.split(' ')[14] for t in lines]
state_humidifier = [t.split(' ')[17] for t in lines]

print(f'terrarium data from last {int(sys.argv[1])} hours:')
print('#############################################################')
print(f'mode temperature: {statistics.mode(temps)}°C')
print(f'mean temperature: {statistics.mean(temps):.2f}°C')
print(f'median temperature: {statistics.median(temps)}°C')
print(f"heater usage: {state_heaters.count('ON')/len(state_heaters) * 100:.2f}%")

total_temps = len(temps)
distribution = {k: temps.count(k) for k in set(temps)}
for line in [f"{k}°C: {distribution[k]} -> {distribution[k]/total_temps * 100:.2f}%" for k in sorted(list(distribution.keys()))]:
    print(line)
print('-----------------------------------------------------')
print(f'mode humidity: {statistics.mode(humiditys)}°C')
print(f'mean humidity: {statistics.mean(humiditys):.2f}°C')
print(f'median humidity: {statistics.median(humiditys)}°C')
print(f"humidifier usage: {state_humidifier.count('ON')/len(state_humidifier) * 100:.2f}%")
total_humiditys = len(humiditys)
distribution = {k: humiditys.count(k) for k in set(humiditys)}
for line in [f"{k}°C: {distribution[k]} -> {distribution[k]/total_humiditys * 100:.2f}%" for k in sorted(list(distribution.keys()))]:
    print(line)

print('#############################################################', end='\n\n')



