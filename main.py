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

    # Comparison sets
    arp_only = arp_ips - icmp_ips
    icmp_only = icmp_ips - arp_ips
    both = arp_ips & icmp_ips

    # Show summary with cleaned formatting
    def fmt(result_set):
        return str(result_set) if result_set else "{}"

    print("\n[✓] Scan Results Summary")
    print(f"ARP-only:   {fmt(arp_only)}")
    print(f"ICMP-only:  {fmt(icmp_only)}")
    print(f"Both:       {fmt(both)}")

    # Final IPs to scan = union of all discovered hosts
    final_ips = sorted(arp_ips | icmp_ips)

    def discovery_method(ip):
        if ip in arp_ips and ip in icmp_ips:
            return "ARP + ICMP"
        elif ip in arp_ips:
            return "ARP only"
        elif ip in icmp_ips:
            return "ICMP only"
        else:
            return "Unknown"  # Should never happen with current logic

    # Run port scan
    print("\n[*] Starting port scans...")
    port_range = range(1, 1025)
    for ip in final_ips:
        label = discovery_method(ip)
        print(f"\n[+] Scanning ports on {ip} ({label})")
        scan_ip_ports(ip, port_range)

if __name__ == "__main__":
    main()
