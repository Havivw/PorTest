PorTest 
=====

## Installation

clone the directory

```shell
$ cd TestPort
$ pip3 install .

```

## Client Usage

```shell
$ python3 client.py -h
usage: client.py [-h] --attacker ATTACKER [--tcp-method TCP_METHOD]

PortTest Client

optional arguments:
  -h, --help            show this help message and exit
  --attacker ATTACKER, -a ATTACKER
                        Attacker Listener Server IP
  --tcp-method TCP_METHOD, -t TCP_METHOD
                        TCP Method. The options are: DONTFRAG|TTL. Default:
                        DONTFRAG
```
## Server Usage
```
$ sudo python3 portest.py -h
usage: portest.py [-h] [--timeout TIMEOUT] [--source SOURCE] [--interface INTERFACE]

Port Test Server listen to the world!

optional arguments:
  -h, --help            show this help message and exit
  --timeout TIMEOUT, -t TIMEOUT
                        Timout in second. Default: 86400 (24H).
  --source SOURCE, -s SOURCE
                        Source ip if known. Default all sources.
  --interface INTERFACE, -i INTERFACE
                        Local IP to sniff packets.

```

### Run Server.

```shell
$ sudo python3 portest.py -i "<local_ip>" -s "Client_ip (optinal)"
PorTest - INFO - Start sniffing for 86400 sec...
PorTest - SUCCESS - Count Packets: 523945.
PorTest - INFO - Sniffing Done!.
$ sort Results.txt |uniq >UResults.txt
```

### Run Client

```shell
$ python3 client.py -a <IP_Server>  -t ttl
Port Test Client run against <IP_Server>, TCP-Method: TTL.
PorTest - INFO - Using 24 Threads
PorTest - INFO - 9% done
PorTest - INFO - 41% done
PorTest - INFO - 72% done
PorTest - INFO - 98% done
PorTest - INFO - Port Test finish run!
PorTest - INFO - Duration in minutes: 18.724536266666668
PorTest - INFO - Duration in seconds: 1123.472176
```


## Additional Info
* Threds number is 2 threds for each cpu core

## Contributions..

..are always welcome.
