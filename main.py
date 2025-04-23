from utils.network import get_ip_list
from scanner.arp_scan import arp_scan
from scanner.icmp_scan import scan_alive_hosts
from scanner.tcp_scan import scan_ip_ports

def main():
    network = input("Enter CIDR (e.g., 192.168.1.0/24): ").strip()
    all_ips = get_ip_list(network)

    # Run ARP scan
    arp_hosts = arp_scan(network)
    arp_ips = {host['ip'] for host in arp_hosts}

    # Run ICMP ping sweep
    print(f"\n[*] Running ICMP ping sweep on {network}...")
    icmp_ips = set(scan_alive_hosts(all_ips))

    # Show full comparison
    print("\n[✓] Scan Results Summary")
    print(f"ARP-only:   {arp_ips - icmp_ips}")
    print(f"ICMP-only:  {icmp_ips - arp_ips}")
    print(f"Both:       {arp_ips & icmp_ips}")

    # Union of both sets for port scan
    final_ips = sorted(arp_ips | icmp_ips)

    # Port scan on each alive host
    print("\n[*] Starting port scans...")
    port_range = range(1, 1025)
    for ip in final_ips:
        print(f"\n[+] Scanning ports on {ip}")
        scan_ip_ports(ip, port_range)

if __name__ == "__main__":
    main()

