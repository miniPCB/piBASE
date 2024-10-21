import subprocess
import sys
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import nmap
import ipaddress
import time
from tqdm import tqdm  # Import tqdm for progress bar

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

try:
    from tqdm import tqdm
except ImportError:
    print("tqdm module not found, installing...")
    install_package("tqdm")
    from tqdm import tqdm  # Reimport after installation

def scan_ip(ip_address):
    """Scan an individual IP address."""
    scanner = nmap.PortScanner()
    logging.info(f"Scanning IP: {ip_address}")
    print(f"Scanning IP: {ip_address}")  # Add a print statement to track progress in real time

    try:
        # Simplified scan: no OS detection, only the first 100 common ports.
        scan_result = scanner.scan(hosts=str(ip_address), arguments='-T4 -F')  # -F scans fewer ports, -T4 for normal speed
        host_info = {'ip': ip_address}
        
        if ip_address in scan_result['scan']:
            host = scan_result['scan'][ip_address]
            host_info['state'] = host.get('status', {}).get('state', 'Unknown')
            host_info['mac'] = host.get('addresses', {}).get('mac', 'No MAC address available')
            host_info['hostnames'] = host.get('hostnames', 'No hostname available')
            host_info['os'] = 'OS detection disabled'
            host_info['services'] = {port: host['tcp'][port] for port in host.get('tcp', {})}
        else:
            host_info['state'] = 'Host unreachable'

        return host_info

    except Exception as e:
        logging.error(f"Error scanning {ip_address}: {e}")
        return None

def scan_network_parallel(network_range, num_threads=5, delay=0.5):
    """Scan a network range in parallel."""
    network = ipaddress.ip_network(network_range, strict=False)
    ip_blocks = list(network.hosts())
    results = []

    try:
        # Initialize progress bar
        with tqdm(total=len(ip_blocks), desc="Scanning IPs") as pbar:
            # Use ThreadPoolExecutor to scan in parallel with limited threads
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = []
                for ip in ip_blocks:
                    futures.append(executor.submit(scan_ip, ip))
                    pbar.update(1)  # Update the progress bar after submitting each task
                    time.sleep(delay)  # Introduce delay to reduce load on the system
                
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        results.append(result)
    
    except KeyboardInterrupt:
        logging.warning("Scan interrupted by user. Shutting down gracefully...")
        executor.shutdown(wait=False)  # Ensure the threads stop immediately
        sys.exit(0)  # Exit the program cleanly

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

    # Run the parallel network scan with optimized settings for Raspberry Pi
    try:
        scan_network_parallel(network_range, num_threads=2, delay=1)  # 2 threads and 1-second delay
    except KeyboardInterrupt:
        print("Scan interrupted by user.")
