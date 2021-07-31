import statistics

with open('/home/pi/Documents/healthmind/incubator_logs.txt') as log_file:
    lines = log_file.readlines()
temps = [float(t.split(' ')[4]) for t in lines]
states = [t.split(' ')[9].replace('\n', '') for t in lines]
print(f'mode temperature: {statistics.mode(temps)}°C')
print(f'mean temperature: {statistics.mean(temps)}°C')
print(f'median temperature: {statistics.median(temps)}°C')
print(f"heater usage: {(round(states.count('ON')/len(states), 4)) * 100}%")

distribution = {k: temps.count(k) for k in set(temps)}
print([f"{k}: {distribution[k]}\n" for k in sorted(list(distribution.keys()))])
