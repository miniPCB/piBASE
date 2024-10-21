import subprocess
import sys

# Function to install packages
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure required packages are installed
try:
    import nmap
except ImportError:
    print("nmap module not found, installing...")
    install_package("python-nmap")
    import nmap  # Reimport after installation

try:
    import ipaddress
except ImportError:
    print("ipaddress module not found, installing...")
    install_package("ipaddress")
    import ipaddress  # Reimport after installation

from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_ip_range(ip_range):
    # Create an instance of the PortScanner class
    scanner = nmap.PortScanner()

    # Perform a scan with OS detection, service version detection, and port scanning
    print(f"Scanning IP range: {ip_range}")
    scanner.scan(hosts=str(ip_range), arguments='-O -sV -p 1-1000')  # OS, service version detection, top 1000 ports

    # Collect scan results
    results = []
    for host in scanner.all_hosts():
        host_info = {}
        host_info['ip'] = host
        host_info['state'] = scanner[host].state()
        host_info['mac'] = scanner[host]['addresses'].get('mac', 'No MAC address available')
        host_info['hostnames'] = scanner[host]['hostnames'] if 'hostnames' in scanner[host] else 'No hostname'

        # Get OS details if available
        if 'osmatch' in scanner[host]:
            host_info['os'] = scanner[host]['osmatch'][0]['name']  # Get the first matched OS
        else:
            host_info['os'] = 'OS detection not available'

        # Get service details if available
        if 'tcp' in scanner[host]:
            host_info['services'] = {}
            for port in scanner[host]['tcp']:
                service_info = scanner[host]['tcp'][port]
                host_info['services'][port] = {
                    'service': service_info['name'],
                    'product': service_info.get('product', 'Unknown'),
                    'version': service_info.get('version', 'Unknown')
                }
        results.append(host_info)
    return results

def scan_network_parallel(network_range, num_threads=10):
    # Convert the CIDR range into individual IP addresses
    network = ipaddress.ip_network(network_range, strict=False)
    ip_blocks = list(network.hosts())  # List of all valid host IPs
    results = []

    # Use ThreadPoolExecutor to scan in parallel
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(scan_ip_range, ip) for ip in ip_blocks]
        for future in as_completed(futures):
            try:
                results.extend(future.result())
            except Exception as e:
                print(f"Error occurred during scan: {e}")

    # Print the consolidated results
    for result in results:
        print(f"Host: {result['ip']}")
        print(f"State: {result['state']}")
        print(f"MAC Address: {result['mac']}")
        print(f"Hostnames: {result['hostnames']}")
        print(f"Operating System: {result['os']}")
        if 'services' in result:
            for port, service in result['services'].items():
                print(f"Port {port}: {service['service']} - {service['product']} {service['version']}")
        print("\n")

if __name__ == '__main__':
    # Define your network range (e.g., '192.168.1.0/24')
    network_range = '192.168.1.0/24'

    # Run the parallel network scan
    scan_network_parallel(network_range)
