from utils.network import get_ip_list
from scanner.tcp_scan import scan_ip_ports

def main():
    network = input("Enter CIDR notation (e.g., 192.168.1.0/24): ")
    port_range = range(1, 1025)  # Well-known ports

    ip_list = get_ip_list(network)
    for ip in ip_list:
        scan_ip_ports(ip, port_range)

if __name__ == "__main__":
    main()
