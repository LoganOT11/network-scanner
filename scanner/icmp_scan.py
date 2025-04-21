import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor

def ping_ip(ip):
    """
    Sends one ICMP echo request to the given IP using the system's ping command.
    Returns True if the host is alive (responds), False otherwise.
    """
    # Use platform-specific flag: -n for Windows, -c for Unix
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]
    
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        output = result.stdout.lower()

        # Looser check: "time" and "ttl" instead of strict "time=" or "ttl="
        if "ttl" in output and "time" in output:
            return True
        return False

    except Exception:
        return False

def scan_alive_hosts(ip_list, threads=100):
    """
    Concurrently pings all IPs in the given list and returns a list of live hosts.
    """
    alive_hosts = []

    def check(ip):
        if ping_ip(ip):
            print(f"[+] Host {ip} is alive")
            alive_hosts.append(ip)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for ip in ip_list:
            executor.submit(check, ip)

    return alive_hosts
