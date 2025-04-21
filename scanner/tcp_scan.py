import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=0.3) as sock:
            print(f"[+] {ip}:{port} is open")
    except:
        pass  # Closed or unreachable

def scan_ip_ports(ip, ports):
    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in ports:
            executor.submit(scan_port, ip, port)
