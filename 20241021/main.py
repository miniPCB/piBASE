import subprocess
import sys
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import nmap
import ipaddress

# Setup logging
logging.basicConfig(filename='network_scan_results.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

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

def scan_ip(ip_address):
    """Scan an individual IP address."""
    scanner = nmap.PortScanner()
    logging.info(f"Scanning IP: {ip_address}")

    try:
        scan_result = scanner.scan(hosts=str(ip_address), arguments='-O -sV -p 1-1000')
        host_info = {'ip': ip_address}
        
        if ip_address in scan_result['scan']:
            host = scan_result['scan'][ip_address]
            host_info['state'] = host.get('status', {}).get('state', 'Unknown')
            host_info['mac'] = host.get('addresses', {}).get('mac', 'No MAC address available')
            host_info['hostnames'] = host.get('hostnames', 'No hostname available')
            host_info['os'] = host.get('osmatch', [{'name': 'Unknown'}])[0]['name']
            host_info['services'] = {port: host['tcp'][port] for port in host.get('tcp', {})}
        else:
            host_info['state'] = 'Host unreachable'

        return host_info

    except Exception as e:
        logging.error(f"Error scanning {ip_address}: {e}")
        return None

def scan_network_parallel(network_range, num_threads=10):
    """Scan a network range in parallel."""
    network = ipaddress.ip_network(network_range, strict=False)
    ip_blocks = list(network.hosts())
    results = []

    # Use ThreadPoolExecutor to scan in parallel
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(scan_ip, ip) for ip in ip_blocks]
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    # Log results
    for result in results:
        logging.info(f"Host: {result['ip']}")
        logging.info(f"State: {result['state']}")
        logging.info(f"MAC Address: {result['mac']}")
        logging.info(f"Hostnames: {result['hostnames']}")
        logging.info(f"Operating System: {result['os']}")
        if 'services' in result:
            for port, service in result['services'].items():
                logging.info(f"Port {port}: {service['name']} - {service.get('product', 'Unknown')} {service.get('version', 'Unknown')}")
        logging.info("\n")

if __name__ == '__main__':
    # Define your network range (e.g., '192.168.1.0/24')
    network_range = '192.168.1.0/24'

    # Run the parallel network scan
    scan_network_parallel(network_range)
