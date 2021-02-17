CocaEnum 
=====

## Installation

clone the directory

```shell
$ cd CocaEnum
$ pip3 install .

```


## Usage

```shell
$ cocaenum -h
Usage: cocaenum [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  scan
  sniff

$ cocaenum sniff -h
Usage: cocaenum sniff [OPTIONS]

Options:
  -c, --count INTEGER    number of packets to catch.
  -t, --timeout INTEGER  Timout in second.
  -v, --verbose
  -i, --interfaces TEXT  Interfaces name for sniffing Default all interfaces.
  -h, --help             Show this message and exit.

$ cocaenum scan -h
Usage: cocaenum scan [OPTIONS]

Options:
  -i, --interface TEXT  interface name for change ip and scan.
  -s, --subnets TEXT    Network subnets for scan.(file is possible.) for
                        example: 192.168.0.0/24 or specific ip: 192.168.0.1
  -v, --verbose
  -p, --protocol TEXT   ARP or ICMP
  --dhcp                Return to DHCP setting after finish. Default last
                        settings.
  -h, --help            Show this message and exit.

```

### Run network sniffing to get address.

```shell
$ sudo  cocaenum sniff -c 10000 -v
PROCESS  - CocaEnum -  Start sniffing...
10000
INFO     - CocaEnum -  Stop sniffing
SUCCESS  - CocaEnum -  ['192.168.xx.4', '192.168.xx.17', '192.168.xx.3', '192.168.yy.15', '192.168.yy.4', '192.168.yy.7']
```

### Run IP scan with ARP

```shell
$ $ sudo cocaenum scan  -i enp0s3 -v -p arp -s 192.168.20.0/24 --dhcp
PROCESS  - CocaEnum -  Getting MAC and IP's address from 192.168.20.0/24 subnet.
SUCCESS  - CocaEnum -  Hosts found in subnet: 192.168.20.0/24.
INFO     - CocaEnum -  [('192.168.20.30', 'AA:BB:CC:00:11:22'), ('192.168.20.31', 'AA:BB:CC:00:11:22'), ('192.168.20.32', 'AA:BB:CC:00:11:22'), ('192.168.20.33', 'AA:BB:CC:00:11:22'), ('192.168.20.34', 'AA:BB:CC:00:11:22'), ('192.168.20.35', 'AA:BB:CC:00:11:22'), ('192.168.20.36', 'AA:BB:CC:00:11:22'), ('192.168.20.37', 'AA:BB:CC:00:11:22'), ('192.168.20.38', 'AA:BB:CC:00:11:22'), ('192.168.20.39', 'AA:BB:CC:00:11:22'), ('192.168.20.40', 'AA:BB:CC:00:11:22')]
```
### Run IP scan with ICMP

```shell
$ $ sudo cocaenum scan  -i enp0s3 -v -p arp -s 192.168.20.0/24 --dhcp
PROCESS  - CocaEnum -  Getting MAC and IP's address from 192.168.20.0/24 subnet.
SUCCESS  - CocaEnum -  Hosts found in subnet: 192.168.20.0/24.
INFO     - CocaEnum -  [('192.168.20.30', 'AA:BB:CC:00:11:22'), ('192.168.20.31', 'AA:BB:CC:00:11:22'), ('192.168.20.32', 'AA:BB:CC:00:11:22'), ('192.168.20.33', 'AA:BB:CC:00:11:22'), ('192.168.20.34', 'AA:BB:CC:00:11:22'), ('192.168.20.35', 'AA:BB:CC:00:11:22'), ('192.168.20.36', 'AA:BB:CC:00:11:22'), ('192.168.20.37', 'AA:BB:CC:00:11:22'), ('192.168.20.38', 'AA:BB:CC:00:11:22'), ('192.168.20.39', 'AA:BB:CC:00:11:22'), ('192.168.20.40', 'AA:BB:CC:00:11:22')]
```



## Additional Info

* Cloned repositories are stored under ~/.surch/clones
* Result files are stored under ~/.surch/results

## Testing

NOTE: Running the tests require an internet connection

```shell
git clone git@github.com:cloudify-cosmo/surch.git
cd surch
pip install tox
tox
```

## Contributions..

..are always welcome.
