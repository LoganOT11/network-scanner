import socket

def grab_banner(ip, port, timeout=2):
    """
    Attempts to grab the service banner from an open TCP port.
    Returns banner string if found, or None.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            banner = s.recv(1024).decode(errors="ignore").strip()
            return banner if banner else None
    except Exception:
        return None
