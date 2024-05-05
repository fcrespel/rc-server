# Remote Control REST API

REST API to use an RF 433 MHz transmitter as a remote control. It currently only supports the Chacon DIO 1.0 protocol.

It has only been tested on an ODROID-C4 board and uses an ODROID-specific WiringPi version. It should be easy to adapt it for other boards (e.g. Raspberry Pi).

## Installation

Execute the following commands on a Debian or Ubuntu system to install the required dependencies:
```
apt-get update
apt-get install -y build-essential python3-dev python3-pip
pip install -r requirements.txt
```

## Usage

First, connect an RF 433 MHz transmitter to the GPIO pin of your choice. Take note of the corresponding WiringPi pin number (see [pinout.xyz](https://pinout.xyz/pinout/wiringpi)).

### Server

Execute the following command to run the server locally:

```
./app/server.py
```

You may then go to http://127.0.0.1:8001 to browse the documentation and test the API.

The following arguments are available:

```
./app/server.py [-h] [-a ADDRESS] [-p PORT] [-g GPIO] [-l LOG_LEVEL]

Optional arguments:
  -h, --help                           Show help message and exit
  -a ADDRESS, --address ADDRESS        Address to bind to (default: 127.0.0.1)
  -p PORT, --port PORT                 Port to listen on (default: 8001)
  -g GPIO, --gpio GPIO                 GPIO WiringPi pin number (default: 0)
  -l LOG_LEVEL, --log-level LOG_LEVEL  Log level: CRITICAL, ERROR, WARNING, INFO, DEBUG (default: INFO)
```

A Docker image is also available for the arm64 architecture:

```
docker run -it --rm --privileged -p 8001:8001 ghcr.io/fcrespel/rc-server:master [-h] [-a ADDRESS] [-p PORT] [-g GPIO] [-l LOG_LEVEL]
```

You may want to run it in the background using commands such as the following:

```
# Create and start container
docker run -d --name rc-server --privileged -p 127.0.0.1:8001:8001 ghcr.io/fcrespel/rc-server:master

# Stop server
docker stop rc-server

# Start server
docker start rc-server

# Show live logs
docker logs -f rc-server
```

NOTE: the API port is not secured, make sure to only expose it locally or to trusted clients.

### Client

You may call the API with any HTTP client such as curl:

```
# Replace 12345678 with the actual Chacon DIO 1.0 sender code (arbitrary 26-bit integer)

# Get button 1 status:
curl -sSf -XGET http://127.0.0.1:8001/chacondio10/12345678/1

# Set button 1 to ON:
curl -sSf -XPUT http://127.0.0.1:8001/chacondio10/12345678/1 -d 1

# Set button 1 to OFF:
curl -sSf -XPUT http://127.0.0.1:8001/chacondio10/12345678/1 -d 0
```
