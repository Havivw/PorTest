import sys
import socket
import argparse
import threading
from queue import Queue
from datetime import datetime
from multiprocessing import cpu_count

DEFAULT_THREAD = 2 * cpu_count()
DEFAULT_TIMEOUT = 0.05
DEFAULT_RETRIES = 4
PRINT_LOCK = threading.Lock()
TCP_SCAN_METHOD = {
    "DONTFRAG": (socket.IPV6_DONTFRAG, 1),
    "TTL": (socket.IP_TTL, 245)
}


def get_duration(current_time, created_time, time_unit='M'):
    """ Calculate duration between 2 times.
        parsing created string to created time
        by default is time unit is minute"""
    duration = (current_time - created_time).total_seconds()
    if time_unit == 'M':
        duration /= 60
    return duration

def tcp_port_connection(host, port, method, timeout=DEFAULT_TIMEOUT):
    try:
        sock = socket.socket()
        sock.setsockopt(socket.IPPROTO_IP, TCP_SCAN_METHOD[method][0], TCP_SCAN_METHOD[method][1])
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        return True
    except (socket.timeout, ConnectionResetError) as e:
        if str(e) != 'timed out':
            print(e)
        return False

def udp_port_connection(host, port, timeout=DEFAULT_TIMEOUT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b"PortTest"
    sock.sendto(data, (host, port))
    if timeout:
        sock.settimeout(timeout)
    try:
        _ = ((sock.recvfrom(1024)))
        return True
    except (socket.timeout, ConnectionResetError) as e:
        if str(e) != 'timed out':
            print(e)
        return False

def repettetive_tcp(host, port, method, timeout, retries=DEFAULT_RETRIES):
    attempts = 0
    success = False
    while attempts < retries and not success:
        success = tcp_port_connection(host, port, method, timeout)
        attempts = attempts + 1
    return success

def repettetive_udp(host, port, timeout, retries=DEFAULT_RETRIES):
    attempts = 0
    success = False
    while attempts < retries and not success:
        success = udp_port_connection(host, port, timeout)
        attempts = attempts + 1
    return success

def run_worker(queue_of_ports, host, tcp_method):
    while not queue_of_ports.empty():
        port = queue_of_ports.get(timeout=2)
        tcp_method = tcp_method.upper()
        if port:
            repettetive_udp(host, int(port), timeout=DEFAULT_TIMEOUT, retries=DEFAULT_RETRIES)
            repettetive_tcp(host, int(port), method=tcp_method, timeout=DEFAULT_TIMEOUT, retries=DEFAULT_RETRIES)
        with PRINT_LOCK:
            print(f"PorTest - INFO - {100 - (len(queue_of_ports.queue) * 100) // (2**16)}% done", end='\r')

def start_scan(host, tcp_method):
    pool = []
    queue_of_ports = Queue()
    for port in range(1, 2**16):
        queue_of_ports.put(port)
    for procId in range(1, DEFAULT_THREAD + 1):
        pool.append(threading.Thread(target=run_worker, args=(queue_of_ports, host, tcp_method)))
    print(f"PorTest - INFO - 0% done", end='\r')
    for proc in pool:
        proc.start()
    for proc in pool:
        proc.join()
    print("PorTest - INFO - Port Test finish run!")

def parse_argumets():
    parser = argparse.ArgumentParser(description='PortTest Client')
    parser.add_argument('--attacker', '-a', help="Attacker Listener Server IP", type=str, required=True)
    parser.add_argument('--tcp-method', '-t', help=f"TCP Method. The options are: {'|'.join(TCP_SCAN_METHOD.keys())}. Default: DONTFRAG", type=str, default="DONTFRAG")
    return parser.parse_args()

def main():
    args = parse_argumets()
    attacker = args.attacker
    print("Port Test Client run against {0}.".format(attacker))
    print("PorTest - INFO - Using {0} Threads".format(DEFAULT_THREAD))
    start_scan(host=attacker, tcp_method=args.tcp_method)

if __name__ == '__main__':
    start = datetime.now()
    main()
    end = datetime.now()
    dur_min = get_duration(end, start, time_unit='M')
    dur_sec = get_duration(end, start, time_unit='S')
    print("PorTest - INFO - Duration in minutes: {0}".format(dur_min))
    print("PorTest - INFO - Duration in seconds: {0}".format(dur_sec))
