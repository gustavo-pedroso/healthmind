import statistics

with open('/home/pi/Documents/healthmind/incubator_logs.txt') as log_file:
    lines = log_file.readlines()
temps = [float(t.split(' ')[4]) for t in lines]
print(f'mode temperature: {statistics.mode(temps)}°C')
print(f'mean temperature: {statistics.mean(temps)}°C')
print(f'median temperature: {statistics.median(temps)}°C')
