import argparse
import socket
from queue import Queue
from threading import Thread
from typing import Never, cast

SOCKET_TIMEOUT = 1
MAX_PORT = 65535
NUM_WORKER = 5

q: Queue[int] = Queue()


def main(host: str) -> None:
    try:
        scan_host(host)
    except KeyboardInterrupt:
        print("\nScan is stopping...")
    finally:
        print("Scan completed successfully.")


def worker(host: str) -> Never:
    """
    While running, will always try to scan port from the queue.
    When it find an open port, the worker will print the port.
    """
    while True:
        port: int = q.get()
        is_open: bool = scan_port(host, port)
        if is_open:
            print(f"--> Port {port}/TCP is open.")


def scan_host(host: str) -> None:
    # Setup workers
    workers: list[Thread] = []
    for _ in range(NUM_WORKER):
        t: Thread = Thread(target=worker, args=(host,), daemon=True)
        t.start()
        workers.append(t)

    # Setup queue
    for port in range(MAX_PORT):
        q.put(port)

    q.join()


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
