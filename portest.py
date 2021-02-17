#!/usr/bin/env python3

import argparse
import threading

from scapy.all import *
from requests import get


PACKET_COUNTER = 1
EXTERNAL_IP = get('https://checkip.amazonaws.com/').text.rstrip("\n")
LOCAL_IP = ''
SOURCE_IP = '.'
RESULT_FILE = open('Results.txt', 'w')
LOCK_FILE = threading.Lock()
LOCK_COUNTER = threading.Lock()


def get_packet(pkt):
    global PACKET_COUNTER
    global LOCAL_IP
    global SOURCE_IP
    global RESULT_FILE
    global LOCK_FILE
    global LOCK_COUNTER

    if IP in pkt:
        ip_src = pkt[IP].src
        ip_dst = pkt[IP].dst
        if SOURCE_IP in ip_src:
            if TCP in pkt and (str(pkt[IP].flags) == 'DF' or pkt[IP].ttl > 220) and str(pkt[TCP].flags) == 'S':
                tcp_dport = pkt[TCP].dport
                if str(ip_dst) == EXTERNAL_IP or str(ip_dst) == LOCAL_IP:
                    string = "{0} {1} [TCP]\n".format(str(ip_src), str(tcp_dport))
                    with LOCK_FILE:
                        RESULT_FILE.write(string)
                        RESULT_FILE.flush()
                    with LOCK_COUNTER:
                        sys.stdout.write('\x1b[1A')
                        sys.stdout.write('\x1b[2K')
                        print('PorTest - SUCCESS - Count Packets: {0}.'.format(PACKET_COUNTER))
                        PACKET_COUNTER = PACKET_COUNTER + 1

            elif UDP in pkt:
                tcp_dport = pkt[UDP].dport
                if raw(pkt.getlayer(UDP).getlayer(1)) == b"PortTest":
                    if str(ip_dst) == EXTERNAL_IP or str(ip_dst) == LOCAL_IP:
                        string = "{0} {1} [UDP]\n".format(str(ip_src), str(tcp_dport))
                        with LOCK_FILE:
                            RESULT_FILE.write(string)
                            RESULT_FILE.flush()
                        with LOCK_COUNTER:
                            sys.stdout.write('\x1b[1A')
                            sys.stdout.write('\x1b[2K')
                            print('PorTest - SUCCESS - Count Packets: {0}.'.format(PACKET_COUNTER))
                            PACKET_COUNTER = PACKET_COUNTER + 1


def sniff_function(timeout=None):
    conf.sniff_promisc=True
    print("PorTest - INFO - Start sniffing for {0} sec...".format(timeout))
    print(" ")
    sniff(filter="ip", prn=get_packet, timeout=timeout, store=False)
    print("PorTest - INFO - Sniffing Done!.")

def parse_argumets():
    parser = argparse.ArgumentParser(description='Port Test Server listen to the world!')
    parser.add_argument('--timeout', '-t', default=86400, type=int, help='Timout in second. Default: 86400 (24H).')
    parser.add_argument('--source', '-s', default='.', type=str, help='Source ip if known. Default all sources.')
    parser.add_argument('--interface', '-i', default=None, type=str, help='Local IP to sniff packets.')
    return parser.parse_args()

def main():
    global LOCAL_IP
    global SOURCE_IP

    args = parse_argumets()
    LOCAL_IP = args.interface
    SOURCE_IP = args.source

    sniff_function(timeout=args.timeout)
    RESULT_FILE.close()

if __name__ == '__main__':
    main()




