import socket
from utils.protocol_probes import smart_probe

def grab_banner(ip, port, timeout=2):
    """
    Grabs a banner from an open port using a smart protocol-aware approach.
    Falls back to passive grab if unknown port.
    """
    # Try smart fingerprinting first
    banner = smart_probe(ip, port, timeout)
    if banner:
        return banner

    # Passive fallback
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            return s.recv(1024).decode(errors="ignore").strip()
    except:
        return None

