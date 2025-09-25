import random
import numpy as np


class SensorTask:
    """Represents a sensor reading ('device') from a sensor network.

    This class is used to model sensor devices in the simulation. It includes
    attributes for resource requirements, deadlines, and trust scores.
    """

    def __init__(self, task_id, mote_id, voltage_reading, is_malicious=False):
        self.id = task_id
        self.source_mote_id = mote_id
        self.cpu_request = voltage_reading  # Standardized attribute name
        self.weight_latency = 0.8
        self.weight_energy = 0.2
        self.deadline = random.uniform(25, 50)
        self.is_malicious = is_malicious
        self.trust_score = 0.1 if is_malicious else 1.0
        self.consecutive_rejections = 0

    def calculate_utility(self, latency, energy):
        """Calculates the utility for the task based on latency and energy consumption."""
        return -(self.weight_latency * latency + self.weight_energy * energy)

    def update_trust_score(self, is_assigned):
        """Updates the trust score of the task based on its behavior."""
        if is_assigned:
            if self.is_malicious:
                self.consecutive_rejections += 1
                penalty_factor = 0.90 - (0.05 * self.consecutive_rejections)
                self.trust_score = max(0.1, self.trust_score * penalty_factor)
            else:
                self.trust_score = min(1.0, self.trust_score * 1.05)
                self.consecutive_rejections = 0
        else:
            self.trust_score *= 0.995


class Mote:
    """Represents a physical sensor mote ('server') in a sensor network.

    This class is used to model the servers in the simulation. It includes
    attributes for CPU capacity and load balancing.
    """

    def __init__(self, mote_id, capacity_cpu):
        self.id = mote_id
        self.capacity_cpu = capacity_cpu if capacity_cpu > 0 else 0.5
        self.hosted_tasks = []
        self.load_balancing_weight = 1.5

    def get_current_cpu_load(self):
        """Calculates the current CPU load of the mote."""
        if not self.capacity_cpu or not self.hosted_tasks:
            return 0
        current_cpu_load = sum(task.cpu_request for task in self.hosted_tasks)
        return current_cpu_load / self.capacity_cpu

    def calculate_utility(self, tasks_to_host):
        """Calculates the utility for the mote based on the tasks it is hosting."""
        if not tasks_to_host:
            return 0
        potential_load = sum(task.cpu_request for task in tasks_to_host) / self.capacity_cpu
        avg_trust = sum(task.trust_score for task in tasks_to_host) / len(tasks_to_host)
        load_penalty = self.load_balancing_weight * (potential_load ** 2)
        return avg_trust - load_penalty


class IoTEdgeModule:
    """Represents a module ('device') in an IoT Edge environment.

    This class is used to model IoT Edge modules in the simulation. It includes
    attributes for resource requirements, deadlines, and trust scores.
    """

    def __init__(self, module_id, cpu_request, ram_request, is_malicious=False):
        self.id = module_id
        self.cpu_request = cpu_request
        self.ram_request = ram_request
        self.weight_latency = 0.8
        self.weight_energy = 0.2
        self.deadline = random.uniform(20, 40)
        self.is_malicious = is_malicious
        self.trust_score = 0.1 if is_malicious else 1.0
        self.consecutive_rejections = 0

    def calculate_utility(self, latency, energy):
        """Calculates the utility for the module based on latency and energy consumption."""
        return -(self.weight_latency * latency + self.weight_energy * energy)

    def update_trust_score(self, is_assigned):
        """Updates the trust score of the module based on its behavior."""
        if is_assigned:
            if self.is_malicious:
                self.consecutive_rejections += 1
                penalty_factor = 0.90 - (0.05 * self.consecutive_rejections)
                self.trust_score = max(0.1, self.trust_score * penalty_factor)
            else:
                self.trust_score = min(1.0, self.trust_score * 1.05)
                self.consecutive_rejections = 0
        else:
            self.trust_score *= 0.995


class AzureIoTEdgeDevice:
    """Represents a physical Edge Device ('server') in an IoT Edge environment.

    This class is used to model the servers in the simulation. It includes
    attributes for CPU and RAM capacity, and load balancing.
    """

    def __init__(self, server_id, capacity_cpu, capacity_ram):
        self.id = server_id
        self.capacity_cpu = capacity_cpu if capacity_cpu > 0 else 0.5
        self.capacity_ram = capacity_ram if capacity_ram > 0 else 0.5
        self.hosted_modules = []
        self.load_balancing_weight = 1.5

    def get_current_cpu_load(self):
        """Calculates the current CPU load of the device."""
        if not self.capacity_cpu or not self.hosted_modules:
            return 0
        current_cpu_load = sum(mod.cpu_request for mod in self.hosted_modules)
        return current_cpu_load / self.capacity_cpu

    def calculate_utility(self, modules_to_host):
        """Calculates the utility for the device based on the modules it is hosting."""
        if not modules_to_host:
            return 0
        potential_load = sum(mod.cpu_request for mod in modules_to_host) / self.capacity_cpu
        avg_trust = sum(mod.trust_score for mod in modules_to_host) / len(modules_to_host)
        load_penalty = self.load_balancing_weight * (potential_load ** 2)
        return avg_trust - load_penalty


class Simulation:
    """Manages the simulation execution.

    This class is the core of the simulation engine. It takes a list of devices
    and servers as input, and provides a `run` method to run the simulation
    with a specified algorithm.
    """

    def __init__(self, devices, servers):
        self.devices = devices
        self.servers = servers
        self.cost_matrix = {
            dev.id: {
                srv.id: {
                    'latency': np.random.lognormal(mean=2.5, sigma=0.8),
                    'energy': random.uniform(1, 5)
                } for srv in self.servers
            } for dev in self.devices
        }

    def _get_dynamic_cost(self, device, server):
        """Calculates the dynamic cost of running a device on a server."""
        base_cost = self.cost_matrix[device.id][server.id]
        load_factor = 1 + server.get_current_cpu_load()
        processing_time = (device.cpu_request / server.capacity_cpu) if server.capacity_cpu > 0 else float('inf')
        latency = base_cost['latency'] * load_factor
        return latency, base_cost['energy'], processing_time

    def _assign_devices_to_servers(self, assignments):
        """Assigns devices to servers based on the given assignments."""
        for server in self.servers:
            if isinstance(server, Mote):
                server.hosted_tasks = []
            elif isinstance(server, AzureIoTEdgeDevice):
                server.hosted_modules = []

        for dev_id, srv_id in assignments.items():
            if srv_id is not None:
                server = next((s for s in self.servers if s.id == srv_id), None)
                device = next((d for d in self.devices if d.id == dev_id), None)
                if server and device:
                    if isinstance(server, Mote):
                        server.hosted_tasks.append(device)
                    elif isinstance(server, AzureIoTEdgeDevice):
                        server.hosted_modules.append(device)

    def run(self, algorithm, iterations=50):
        """Runs the simulation for a given algorithm.

        Args:
            algorithm (str): The algorithm to use for task allocation.
                Can be 'game_theory', 'greedy', or 'random'.
            iterations (int): The number of simulation iterations.

        Returns:
            dict: A dictionary containing the simulation history.
        """
        history = {
            'avg_device_utility': [], 'server_load_std_dev': [],
            'avg_trust_honest': [], 'avg_trust_malicious': [],
            'completion_ratio': [], 'deadline_adherence': [],
            'malicious_accepted': [], 'total_energy': []
        }

        for i in range(iterations):
            assignments = {}
            if algorithm == 'game_theory':
                # Game-Theoretic Algorithm
                proposals = {srv.id: [] for srv in self.servers}
                for device in self.devices:
                    best_server_id, max_utility = None, -float('inf')
                    for server in self.servers:
                        latency, energy, _ = self._get_dynamic_cost(device, server)
                        utility = device.calculate_utility(latency, energy) * device.trust_score
                        if utility > max_utility:
                            max_utility, best_server_id = utility, server.id
                    if best_server_id is not None:
                        proposals[best_server_id].append(device)

                final_assignments = {}
                for server in self.servers:
                    requesting_devices = proposals[server.id]
                    if not requesting_devices:
                        continue

                    requesting_devices.sort(key=lambda d: d.trust_score, reverse=True)
                    accepted_devices, best_utility = [], server.calculate_utility([])

                    for device in requesting_devices:
                        potential_new_set = accepted_devices + [device]
                        if server.calculate_utility(potential_new_set) > best_utility:
                            accepted_devices = potential_new_set
                            best_utility = server.calculate_utility(accepted_devices)
                    for device in accepted_devices:
                        final_assignments[device.id] = server.id
                assignments = final_assignments

            elif algorithm in ['greedy', 'random']:
                # Greedy and Random Algorithms
                for device in self.devices:
                    if algorithm == 'greedy':
                        best_server_id, max_utility = None, -float('inf')
                        for server in self.servers:
                            latency, energy = self.cost_matrix[device.id][server.id]['latency'], self.cost_matrix[device.id][server.id]['energy']
                            utility = device.calculate_utility(latency, energy)
                            if utility > max_utility:
                                max_utility, best_server_id = utility, server.id
                        assignments[device.id] = best_server_id
                    else:  # Random
                        assignments[device.id] = random.choice(self.servers).id
                if i > 0:
                    for key in history:
                        if history[key]:
                            history[key].append(history[key][0])
                    continue

            # Update trust scores and record history
            assigned_ids = set(assignments.keys())
            for device in self.devices:
                device.update_trust_score(is_assigned=(device.id in assigned_ids))

            total_utility, deadlines_met, malicious_accepted, total_energy = 0, 0, 0, 0
            assigned_count = 0

            for dev_id, srv_id in assignments.items():
                if srv_id is None:
                    continue
                assigned_count += 1
                device = next(d for d in self.devices if d.id == dev_id)
                server = next(s for s in self.servers if s.id == srv_id)

                latency, energy, proc_time = self._get_dynamic_cost(device, server)
                total_utility += device.calculate_utility(latency, energy)
                total_energy += energy
                if (latency + proc_time) <= device.deadline:
                    deadlines_met += 1
                if device.is_malicious:
                    malicious_accepted += 1

            history['avg_device_utility'].append(total_utility / len(self.devices) if self.devices else 0)
            self._assign_devices_to_servers(assignments)
            server_loads = [s.get_current_cpu_load() for s in self.servers]
            history['server_load_std_dev'].append(np.std(server_loads))

            honest_trust = [d.trust_score for d in self.devices if not d.is_malicious]
            malicious_trust = [d.trust_score for d in self.devices if d.is_malicious]
            history['avg_trust_honest'].append(np.mean(honest_trust) if honest_trust else 1.0)
            history['avg_trust_malicious'].append(np.mean(malicious_trust) if malicious_trust else 0.1)

            num_malicious_total = len(malicious_trust) if malicious_trust else 0
            history['completion_ratio'].append(assigned_count / len(self.devices) if self.devices else 0)
            history['deadline_adherence'].append(deadlines_met / assigned_count if assigned_count > 0 else 0)
            history['malicious_accepted'].append(malicious_accepted / num_malicious_total if num_malicious_total > 0 else 0)
            history['total_energy'].append(total_energy)

        return history
