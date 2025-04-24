import socket
import ssl

def http_probe(ip, port, timeout):
    try:
        with socket.create_connection((ip, port), timeout=timeout) as s:
            s.sendall(f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n".encode())
            return s.recv(1024).decode(errors="ignore").strip()
    except:
        return None

def https_probe(ip, port, timeout):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((ip, port), timeout=timeout) as raw_sock:
            with context.wrap_socket(raw_sock, server_hostname=ip) as ssock:
                request = (
                    f"GET / HTTP/1.1\r\n"
                    f"Host: {ip}\r\n"
                    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
                    "Accept: */*\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )
                ssock.sendall(request.encode())

                # Read just enough to extract headers (1024B usually covers it)
                response = ssock.recv(1024).decode(errors="ignore")

                # Only keep response headers (before first blank line)
                headers = response.split("\r\n\r\n")[0].splitlines()

                # Look for Server header first
                for line in headers:
                    if line.lower().startswith("server:"):
                        return line.strip()  # e.g. Server: nginx/1.18.0

                # If no Server header, return HTTP status line
                if headers:
                    return headers[0].strip()  # e.g. HTTP/1.1 400 Bad Request

                return None
    except:
        return None

def smtp_probe(ip, port, timeout):
    try:
        with socket.create_connection((ip, port), timeout=timeout) as s:
            return s.recv(1024).decode(errors="ignore").strip()
    except:
        return None

def ftp_probe(ip, port, timeout):
    try:
        with socket.create_connection((ip, port), timeout=timeout) as s:
            return s.recv(1024).decode(errors="ignore").strip()
    except:
        return None

def ssh_probe(ip, port, timeout):
    try:
        with socket.create_connection((ip, port), timeout=timeout) as s:
            s.settimeout(timeout)
            banner = s.makefile('rb').readline().decode(errors="ignore").strip()
            return banner
    except:
        return None

# Mapping ports to probe functions
PORT_PROBES = {
    21: ftp_probe,
    22: ssh_probe,
    25: smtp_probe,
    80: http_probe,
    443: https_probe,
    587: smtp_probe,
    8080: http_probe,
}

def smart_probe(ip, port, timeout=2):
    """
    Performs protocol-specific probing based on the port number.
    Returns the banner string or None.
    """
    probe_fn = PORT_PROBES.get(port)
    if probe_fn:
        return probe_fn(ip, port, timeout)
    return None
