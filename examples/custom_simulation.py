import random
from trustiot.core import AzureIoTEdgeDevice, IoTEdgeModule

def setup():
    """Sets up devices and servers for a custom simulation."""
    num_edge_devices = 10
    servers = [AzureIoTEdgeDevice(server_id=f"edge-device-{i}", capacity_cpu=random.uniform(2.0, 8.0), capacity_ram=random.uniform(4.0, 16.0)) for i in range(num_edge_devices)]
    num_modules = 200
    num_malicious = int(num_modules * 0.15)
    devices = [IoTEdgeModule(module_id=f"module-{i}", cpu_request=random.uniform(0.1, 1.0), ram_request=random.uniform(0.1, 0.5), is_malicious=(i < num_malicious)) for i in range(num_modules)]
    random.shuffle(devices)
    print(f"Simulating with {len(devices)} modules and {len(servers)} edge devices ({num_malicious} malicious).")
    return devices, servers
