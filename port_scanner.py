import socket
import time
from datetime import datetime

# Only scan targets authorized by the assignment.
ALLOWED_HOSTS = {
    "127.0.0.1",
    "localhost",
    "scanme.nmap.org"
}


def scan_ports(host, start_port, end_port):
    # Restrict scanning to authorized targets.
    if host not in ALLOWED_HOSTS:
        print("Error: Target is not authorized.")
        return

    # Check that the port numbers are valid.
    if not (1 <= start_port <= end_port <= 65535):
        print("Error: Invalid port range. Use 1-65535.")
        return

    try:
        # Convert the hostname into an IP address.
        target_ip = socket.gethostbyname(host)

        print(f"\nScanning {host} ({target_ip})")
        print(f"Port range: {start_port}-{end_port}")
        print(f"Started: {datetime.now()}")
        print("-" * 40)

        start_time = time.time()
        open_ports = []

        for port in range(start_port, end_port + 1):
            # Create a TCP socket for each port.
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)

                # Attempt a connection to the target port.
                result = sock.connect_ex((target_ip, port))

                if result == 0:
                    print(f"Port {port}: OPEN")
                    open_ports.append(port)
                else:
                    print(f"Port {port}: CLOSED or FILTERED")

            # Add a delay to avoid aggressive scanning.
            time.sleep(0.1)

        elapsed = time.time() - start_time

        print("-" * 40)
        print(f"Open ports found: {len(open_ports)}")
        print(f"Scan duration: {elapsed:.2f} seconds")
        print(f"Finished: {datetime.now()}")

    except socket.gaierror:
        print("Error: Hostname could not be resolved.")

    except OSError as error:
        print(f"Network error: {error}")


def main():
    try:
        host = input("Enter target host: ").strip().lower()
        start_port = int(input("Enter starting port: "))
        end_port = int(input("Enter ending port: "))

        scan_ports(host, start_port, end_port)

    except ValueError:
        print("Error: Please enter valid integer port numbers.")


if __name__ == "__main__":
    import sys
    from unittest.mock import patch

    if "--test-unreachable" in sys.argv:
        print("Testing simulated unreachable host...")
        print(f"Started: {datetime.now()}")

        # Simulate a DNS resolution failure without network traffic.
        with patch(
            "socket.gethostbyname",
            side_effect=socket.gaierror("Host unreachable")
        ):
            scan_ports("127.0.0.1", 80, 80)

        print(f"Finished: {datetime.now()}")
    else:
        main()
