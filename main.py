from utils.network import get_ip_list
from scanner.icmp_scan import scan_alive_hosts
from scanner.tcp_scan import scan_ip_ports

def main():
    network = input("Enter CIDR (e.g., 192.168.1.0/24): ")
    ip_list = get_ip_list(network)

    # Step 1: Ping sweep to find live hosts
    print("[*] Performing ICMP host discovery...")
    alive_hosts = scan_alive_hosts(ip_list)

    # Step 2: Only scan ports on live hosts
    port_range = range(1, 1025)
    for ip in alive_hosts:
        scan_ip_ports(ip, port_range)

if __name__ == "__main__":
    main()
