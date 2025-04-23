import socket
from concurrent.futures import ThreadPoolExecutor
from utils.banner_grab import grab_banner

def scan_ip_ports(ip, ports, timeout=1):
    """
    Scans a given IP for a list of TCP ports.
    Prints open ports and banner info (if available).
    """
    def scan_port(port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((ip, port))
                print(f"[OPEN] {ip}:{port}", end='')

                banner = grab_banner(ip, port)
                if banner:
                    print(f"  →  {banner}")
                else:
                    print(f"  →  No banner found")
        except:
            pass  # silently ignore closed/filtered ports

    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in ports:
            executor.submit(scan_port, port)
