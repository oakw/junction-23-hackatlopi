import psutil
import time


class Monitor:
    pass

def monitor_process(pid, duration):
    process = psutil.Process(pid)
    cpu_load_history = []
    
    start_time = time.time()
    print(start_time)
    end_time = start_time + duration
    
    while time.time() < end_time:
        cpu_percent = process.cpu_percent(interval=0.1)
        cpu_load_history.append(cpu_percent)
        
    return cpu_load_history

def calculate_energy_consumption(pid, duration):
    process = psutil.Process(pid)
    start_time = time.time()
    end_time = start_time + duration
    start_energy = process.cpu_times()
    
    while time.time() < end_time:
        pass
    
    end_energy = process.cpu_times()
    print(start_energy, end_energy)
    exit()
    total_energy = end_energy - start_energy
    # Convert CPU time to Watts
    cpu_energy = total_energy / process.cpu_count() / process.cpu_freq().current * 100

    # Convert Watts to Watt-hours
    energy_consumption = cpu_energy * duration / 3600
    
    return energy_consumption


if __name__ == "__main__":
    process = psutil.Process(15288)
    print(process.cpu_percent(interval=0.001))
    print()
    # print(monitor_process(15288, 2))
    print(calculate_energy_consumption(15288, 2))


