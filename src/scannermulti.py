import argparse
import socket
from typing import cast

SOCKET_TIMEOUT = 1
MAX_PORT = 65535


def main(host: str) -> None:
    try:
        print(f"scanning {host}...")
        scan_host(host)
    except KeyboardInterrupt:
        print("\nScan is stopping...")
    finally:
        print("Scan completed successfully.")


def scan_host(host: str) -> None:
    """
    Scan all port on a target host. Returns nothing, directly
    print all found open port.
    """
    for port in range(MAX_PORT + 1):
        is_open = scan_port(host, port)
        if is_open:
            print(f"--> Port {port}/TCP is open.")


def scan_port(host: str, port: int) -> bool:
    """
    Scan a port to see if its open or not.
    returns: True if the port is open, false if its not
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(SOCKET_TIMEOUT)

    try:
        _ = sock.connect((host, port))
        is_open = True

    except socket.error:
        is_open = False
    finally:
        sock.close()

    return is_open


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("host", help="Target host to scan")
    args = parser.parse_args()
    host: str = cast(str, args.host)

    main(host)
