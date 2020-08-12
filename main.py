#!/usr/bin/env python

import click
import netifaces
from scapy.all import *
from requests import get
from colorlog import ColoredFormatter

i = 1
intip = ''
sshPort = ''
source = set()
destnation = set()
extip = get('https://api.ipify.org').text


def get_interface_configuration(logger, interface=None):
    global intip
    interfaces = [interface, 'eth0', 'enp0s3']
    for interface in interfaces:
        if interface:
            try:
                intip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                return
            except:
                continue
    logger.error("Can't find network interface!")
    sys.exit(0)

def setup_logger(verbose=False):
    """Return a logger with a default ColoredFormatter."""
    logging.addLevelName(21, 'SUCCESS')
    logging.addLevelName(22, 'PROCESS')
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s - %(name)-5s -  %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'ERROR':    'red',
            'CRITICAL': 'red',
            'INFO':     'cyan',
            'DEBUG':    'white',
            'SUCCESS':  'green',
            'PROCESS':  'purple',
            'WARNING':  'yellow',})

    logger = logging.getLogger('PorTest')
    setattr(logger, 'success', lambda *args: logger.log(21, *args))
    setattr(logger, 'process', lambda *args: logger.log(22, *args))
    fh = logging.FileHandler('PorTest.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(handler)
    if not verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)
    return logger



def get_packet(pkt):
    global i
    global intip
    global extip
    global sshPort
    global destnation

    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
    print(i)
    if IP in pkt:
        ip_src = pkt[IP].src
        ip_dst = pkt[IP].dst
        if TCP in pkt:
            tcp_dport = pkt[TCP].dport
            if str(tcp_dport) != sshPort:

                if str(ip_dst) == intip or str(ip_dst) == extip:
                    string = "{0}: {1}".format(str(ip_src), str(tcp_dport))
                    destnation.add(string)
    i = i + 1


def sniff_function(logger, timeout=None, count=None):
    conf.sniff_promisc=True
    logger.process("Start sniffing...")
    print("")
    if count:
        sniff(filter="ip", prn=get_packet, count=count)
    if timeout:
        sniff(filter="ip", prn=get_packet, timeout=timeout)
    logger.info("Stop sniffing")
    logger.success(list(destnation))

def check_os(logger):
    if sys.platform[0:5] == 'linux':
        pass
    elif sys.platform[0:3] == 'win':
        logger.error("NOT SUPPORT IN WINDOWS OS.")
        sys.exit(0)
    else:
        logger.error("Error on detecting OS!")
        sys.exit(0)

def check_root_priv(logger):
    if sys.platform != "win32":
        user = os.getuid()
        if user != 0:
            logger.error("This program requires root privileges.  Run as root using 'sudo'.")
            sys.exit()

###################################CLICK- CLI########################################

CLICK_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'], token_normalize_func=lambda param: param.lower())
timeout = click.option('-t', '--timeout', default=None, type=int, help='Timout in second.')
count = click.option('-c', '--count', default=None, type=int, help='number of packets to catch.')
ssh = click.option('-s', '--ssh', default='22', help='ssh port on the server to ignore. Default: 22')
interface = click.option('-i', '--interface', default=None, help='interface name For listen. Default: eth0/enp0s3')

verbose = click.option('-v', '--verbose', default=False, is_flag=True)

@click.group(context_settings=CLICK_CONTEXT_SETTINGS)
def main():
    pass


@main.command(name='listen')
@ssh
@count
@timeout
@verbose
@interface
def listen_cli(timeout, ssh, count, interface, verbose):
    global sshPort
    sshPort = ssh
    logger = setup_logger(verbose=verbose)
    check_os(logger=logger)
    check_root_priv(logger=logger)
    get_interface_configuration(logger=logger, interface=interface)
    sniff_function(logger=logger, timeout=timeout, count=count)


