# Intrusion-detection

Intrusion detection script in python

This script will scan the network of your choice and will alert you of any devices not present in the whitelist. The whitelist is a list of MAC address that YOU trust. The first time you run the script, the whitelist will be empty, it's up to up to add your trusted devices to the whitelist. 

See the whitelist section for more information


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Software package: **python3** and **nmon**



**Ubuntu / Debian**

```
sudo apt install python3 nmon
```

**Arch/Manjaro/Antergos** 

```
sudo pacman -S nmon python3
```

**CentOS 7/ Redhat 7**

```
sudo yum install python3 nmon
```

**Fedora**

```
sudo dnf install python3 nmon
```



### Installing

Download and unzip, and make sure you have installed the **Prerequisites**


## Whitelist
Every time you run the detection script, a list of all detected devices will be written in the file 'devices.mac'. 

If you trust all these devices, you can import them with the following command:

```
sudo ./trust-devices.py  data.db devices.mac
```

If you don't trust all of them, you can erase the one that you don't want and still import the file.

The following command will flush the current whitelist and import the entries in devices.mac

```
sudo ./trust-devices.py  data.db devices.mac
```



## Deployment

copy the following scripts to any folder. The folder should be writable (because a devices.mac is generated)

- detect.py
- trust-devices.py

you should launch both commands with sudo:

- detect.py : nmon requires root privileges to get the MAC addresses
- trust-devices.py : requires root privileges because the database will be created with root. If you modify the database so that it's writable for someone else, you won't need sudo anymore.

## Running

The database filename can be anything, it will be created if absent. The network must be specified in the **network/mask** notation.

example of valid networks:

- 192.168.0.0/24
- 192.168.1.0/24
- 192.168.2.0/24

```
Syntax:
	sudo ./detect.py  network_range  database

example: 
sudo ./detect.py 192.168.2.0/24 data.db
```

on the first run, all devices should be listed as untrusted, read the whitelist section. You need to run other script to import your trusted devices list.


## Built With

* [Visual studio code](https://code.visualstudio.com/) - Editor

## Built on
* [Manjaro](https://manjaro.org/) - Manjaro


## Authors

* **Luc Raymond** - *Initial work* - [My Github profile](https://github.com/slayerizer)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* feel free to drop me an email if you find it useful (french,english)
