from __future__ import annotations
import time
import threading
import docker
import datetime
import sys

# Intel's RAPL energy API location on Linux
# Used to measure the CPU's power consumption
RAPL_ENERGY_API_LOCATION = "/sys/class/powercap/intel-rapl/intel-rapl:0"

# Record of the docker stats object
class Measurement:
    def __init__(self, stats_object: object, cpu_energy: int) -> None:
        self.read_time = datetime.datetime.fromisoformat(stats_object["read"][:-1])
        self.total_cpu_usage = stats_object["cpu_stats"]["cpu_usage"]["total_usage"]
        self.total_cpu_system_usage = stats_object["cpu_stats"]["system_cpu_usage"]
        self.memory_usage = stats_object["memory_stats"]["usage"]
        self.paged_in_from_disk = stats_object["memory_stats"]["stats"]["total_pgpgin"]
        self.paged_out_to_disk = stats_object["memory_stats"]["stats"]["total_pgpgout"]
        self.networks = dict([(key, stats_object["networks"][key]) for key in stats_object["networks"] if key != "lo"])
        self.cpu_energy = cpu_energy

    def __str__(self) -> str:
        return self.__dict__.__str__()      


# All measurements of the docker container's stats during the monitoring period
class Results:
    def __init__(self) -> None:
        self.measurements = []

    def __str__(self):
        return str([str(measurement) for measurement in self.measurements])

    def add_measurement(self, stats_object) -> None:
        self.measurements.append(stats_object)


# Summary of the docker container's stats during the monitoring period
class Summary:
    def __init__(self, results: Results) -> Summary:
        return self.summarize(results)
    
    def __str__(self) -> str:
        return self.__dict__.__str__()     

    # Use the results array to calculate the summary
    def summarize(self, results: Results) -> Summary:
        last_measurement = results.measurements[-1]
        first_measurement = results.measurements[0]
        self.start_read_datetime = first_measurement.read_time
        self.end_read_datetime = last_measurement.read_time

        # Quantitative analysis is done by taking the difference between the first and last measurements
        self.cpu_usage_delta = last_measurement.total_cpu_usage - first_measurement.total_cpu_usage
        self.cpu_system_usage_delta = last_measurement.total_cpu_system_usage - first_measurement.total_cpu_system_usage
        self.memory_usage_delta = last_measurement.memory_usage - first_measurement.memory_usage
        self.paged_in_from_disk_delta = last_measurement.paged_in_from_disk - first_measurement.paged_in_from_disk
        self.paged_out_to_disk_delta = last_measurement.paged_out_to_disk - first_measurement.paged_out_to_disk
        self.average_cpu_percent = self.cpu_usage_delta / self.cpu_system_usage_delta * 100

        if last_measurement.cpu_energy is not None and first_measurement.cpu_energy is not None:
            self.cpu_energy_delta = last_measurement.cpu_energy - first_measurement.cpu_energy
            self.cpu_process_energy_delta = self.cpu_energy_delta * self.average_cpu_percent / 100
        else:
            self.cpu_energy_delta = None

        self.networks = {}
        for network in last_measurement.networks:
            self.networks[network] = {}
            for measure_key in dict.keys(last_measurement.networks[network]):
                self.networks[network][measure_key] = last_measurement.networks[network][measure_key] - first_measurement.networks[network][measure_key]
        

# Monitor for a docker container
class DockerMonitor:
    def __init__(self, container_name) -> None:
        self.client = docker.from_env()
        self.currently_monitoring = False
        self.results = Results()
        self.stats_stream = self.client.api.stats(container_name, decode=True, stream=True)

    # Start monitoring the docker container
    def start(self) -> None:
        self.currently_monitoring = True
        self.measurement = threading.Thread(target=self.collect_data)
        self.measurement.start()

    # Stop monitoring the docker container
    def end(self) -> Results:
        self.currently_monitoring = False
        return self.results

    # Collect data regarding the docker using the docker stats stream
    def collect_data(self) -> None:
        for capture in self.stats_stream:
            if self.currently_monitoring:
                self.results.add_measurement(Measurement(capture, self.get_cpu_power_comsumption()))
            else:
                break
    
    def get_results(self) -> Results:
        return self.results
    
    def get_summary(self) -> Summary:
        return Summary(self.results)
    
    # Get CPU power consumption in microjoules if available
    def get_cpu_power_comsumption(self) -> int|None:
        try:
            return int(open(f"{RAPL_ENERGY_API_LOCATION}/energy_uj", 'r').read())
        except:
            return None


# Test using the following command:
# python3 docker_monitor.py <docker container name> <time to monitor in seconds>
if __name__ == "__main__":
    monitor = DockerMonitor(sys.argv[1])
    monitor.start()
    time.sleep(int(sys.argv[2]))
    monitor.end()
    print(monitor.get_summary())