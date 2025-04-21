import ipaddress

def get_ip_list(cidr):
    try:
        return [str(ip) for ip in ipaddress.IPv4Network(cidr, strict=False)]
    except ValueError:
        print("Invalid CIDR notation.")
        return []
