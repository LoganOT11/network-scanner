from scapy.all import ARP, Ether, srp

def arp_scan(network_range, timeout=2):
    """
    Sends ARP requests to the given CIDR network.
    Returns a list of dictionaries: {ip, mac}
    """
    print(f"\n[*] Running ARP scan on {network_range}...")
    
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network_range)
    result = srp(packet, timeout=timeout, verbose=False)[0]

    hosts = []
    for _, received in result:
        hosts.append({
            "ip": received.psrc,
            "mac": received.hwsrc
        })
        print(f"[ARP] Found: {received.psrc} ({received.hwsrc})")
    
    return hosts
