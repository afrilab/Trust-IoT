import random
import numpy as np
from trustiot.core import Mote, SensorTask, AzureIoTEdgeDevice, IoTEdgeModule, Simulation

def run_simulation(setup_func, num_runs=5):
    """Runs a simulation with a user-defined setup function.

    Args:
        setup_func (function): A function that returns a tuple of (devices, servers).
        num_runs (int): The number of times to run the benchmark.

    Returns:
        dict: A dictionary containing the aggregated simulation results.
    """

    all_runs_history = {'game_theory': [], 'greedy': [], 'random': []}
    for i in range(num_runs):
        print(f"\n--- Starting Benchmark Run {i+1}/{num_runs} ---")
        devices, servers = setup_func()
        sim = Simulation(devices, servers)
        for algo in all_runs_history.keys():
            history = sim.run(algo)
            all_runs_history[algo].append(history)

    aggregated_results = {}
    for algo, histories in all_runs_history.items():
        aggregated_results[algo] = {}
        for metric in histories[0].keys():
            metric_data = np.array([run[metric] for run in histories])
            aggregated_results[algo][f'{metric}_mean'] = np.mean(metric_data, axis=0)
            aggregated_results[algo][f'{metric}_std'] = np.std(metric_data, axis=0)
    return aggregated_results