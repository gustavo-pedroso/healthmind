from incubator_driver import incubator
from project_utils import get_last_hour_stats, safe_list_get
import statistics
import sys

with open('/home/pi/Documents/healthmind/incubator_logs.txt') as log_file:
    lines = log_file.readlines()

hours = int(safe_list_get(sys.argv, 1, 24))
lines = get_last_hour_stats(lines, hours, incubator.update_time)


temps = [float(t.split(' ')[4]) for t in lines]
states = [t.split(' ')[9].replace('\n', '') for t in lines]
print(f'incubator data from last {hours} hours:')
print('#############################################################')
print(f'mode temperature: {statistics.mode(temps)}°C')
print(f'mean temperature: {statistics.mean(temps):.2f}°C')
print(f'median temperature: {statistics.median(temps)}°C')
print(f"heater usage: {states.count('ON')/len(states) * 100:.2f}%")

total_temps = len(temps)
distribution = {k: temps.count(k) for k in set(temps)}
for line in [f"{k}°C: {distribution[k]} -> {distribution[k]/total_temps * 100:.2f}%" for k in sorted(list(distribution.keys()))]:
    print(line)

print('#############################################################', end='\n\n')
