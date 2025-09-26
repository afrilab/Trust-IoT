# TrustIoT

**A flexible and extensible simulation framework for task allocation in edge computing environments.**

TrustIoT is a Python library that allows you to simulate and compare different task allocation algorithms in edge computing environments. It is designed to be highly customizable, allowing you to use your own datasets and define your own simulation scenarios.

## Key Features

- **Extensible Simulation Engine:** The core of TrustIoT is a powerful and flexible simulation engine that can be easily extended to support new algorithms and scenarios.
- **Built-in Algorithms:** TrustIoT comes with three built-in task allocation algorithms:
    - **Game-Theoretic:** A sophisticated algorithm based on game theory, where tasks and servers make strategic decisions to maximize their utility. This algorithm also incorporates a trust mechanism to handle malicious or unreliable devices.
    - **Greedy:** A simple and efficient algorithm that assigns tasks to the best available server based on a simple utility calculation.
    - **Random:** A baseline algorithm that assigns tasks randomly, useful for comparison and benchmarking.
- **Customizable Setups:** You can easily define your own simulation setups by providing a Python script that creates your custom devices and servers. This allows you to test the algorithms with your own data and in your own specific scenarios.
- **Detailed Visualization:** TrustIoT provides detailed plots and tables to help you visualize and understand the simulation results. This includes plots for average device utility, server load balancing, trust score evolution, and more.
- **Command-Line Interface:** TrustIoT comes with a user-friendly command-line interface (CLI) that makes it easy to run simulations and generate results.

## Project Structure

The project is organized as follows:

```
├───.gitignore
├───LICENSE
├───pyproject.toml
├───README.md
├───examples\
│   ├───custom_simulation.py
│   └───__pycache__\
├───src\
│   ├───icedge.egg-info\
│   ├───trustiot\
│   │   ├───__init__.py
│   │   ├───cli.py
│   │   ├───core.py
│   │   ├───simulation.py
│   │   ├───visualize.py
│   │   └───__pycache__\
│   └───trustiot.egg-info\
└───tests\
```

- **`src/trustiot`**: The main source code for the TrustIoT library.
    - `core.py`: Contains the core classes for devices, servers, and the simulation engine.
    - `simulation.py`: Implements the simulation logic and the different task allocation algorithms.
    - `cli.py`: The command-line interface for running simulations.
    - `visualize.py`: Functions for generating plots and tables.
- **`examples`**: Example scripts for running custom simulations.
- **`tests`**: Unit tests for the TrustIoT library.
- **`pyproject.toml`**: The project's build configuration.
- **`README.md`**: This file.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/afrilab/Trust-IoT.git
    cd trustiot
    ```

2.  **Install the package:**

    ```bash
    pip install .
    ```

## Getting Started

To get started with TrustIoT, you need to create a Python script that defines your simulation setup. This script must contain a function named `setup` that returns a tuple of `(devices, servers)`.

### 1. Create a Setup Script

Here is an example of a simple setup script (`my_simulation.py`):

```python
import random
from trustiot.core import AzureIoTEdgeDevice, IoTEdgeModule

def setup():
    """Sets up devices and servers for a custom simulation."""
    # Create a list of servers (edge devices)
    num_edge_devices = 10
    servers = [AzureIoTEdgeDevice(server_id=f"edge-device-{i}", capacity_cpu=random.uniform(2.0, 8.0), capacity_ram=random.uniform(4.0, 16.0)) for i in range(num_edge_devices)]

    # Create a list of devices (IoT modules)
    num_modules = 200
    num_malicious = int(num_modules * 0.15)  # 15% of devices are malicious
    devices = [IoTEdgeModule(module_id=f"module-{i}", cpu_request=random.uniform(0.1, 1.0), ram_request=random.uniform(0.1, 0.5), is_malicious=(i < num_malicious)) for i in range(num_modules)]
    random.shuffle(devices)

    print(f"Simulating with {len(devices)} modules and {len(servers)} edge devices ({num_malicious} malicious).")

    return devices, servers
```

### 2. Run the Simulation

Once you have created your setup script, you can run the simulation using the `trustiot` CLI:

```bash
trustiot my_simulation.py [OPTIONS]
```

**Arguments:**

- `SETUP_SCRIPT`: Path to your Python setup script.

**Options:**

- `--num-runs INTEGER`: The number of times to run the benchmark. The results will be aggregated. Defaults to 5.
- `--show-plots / --no-plots`: Whether to display the results plots. Defaults to `--show-plots`.

**Example:**

```bash
trustiot my_simulation.py --num-runs 10 --show-plots
```

### 3. Interpreting the Results

After the simulation is complete, TrustIoT will print a detailed table of the results and display a series of plots. Here's how to interpret them:

- **Final Mean Metrics Comparison:** This table shows the final aggregated results for each algorithm across all the benchmark runs. It includes metrics like average device utility, server load standard deviation, task completion ratio, deadline adherence, and malicious task acceptance rate.
- **Average Device Utility Convergence:** This plot shows how the average utility of the devices changes over the simulation iterations. A higher utility is better.
- **Server Load Std. Dev. Convergence:** This plot shows how the standard deviation of the server load changes over the simulation iterations. A lower standard deviation indicates better load balancing.
- **Trust Score Discrimination:** This plot shows how the trust scores of honest and malicious devices change over time. A good trust mechanism should be able to distinguish between the two, with the trust scores of honest devices increasing and the trust scores of malicious devices decreasing.
- **Multi-Metric Performance Comparison (Radar Chart):** This radar chart provides a holistic view of the performance of each algorithm across multiple metrics.
- **Final Server Load Heatmap:** This heatmap shows the final load distribution across all the servers for each algorithm.

## Contributing

Contributions are welcome! If you have any ideas for new features, improvements, or bug fixes, please feel free to open an issue or submit a pull request.

## Citing the Paper

If you use TrustIoT in your research, please cite the following paper:

```bibtex
@article{arxiv,
  title={Trust-Aware Game-Theoretic Allocation for Secure and Efficient IoT-Edge Systems},
  author={Kushagra Agrawal, Oishani Banarjee and Polat Goktas},
  journal={arXiv preprint},
  year={2025}
}
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
