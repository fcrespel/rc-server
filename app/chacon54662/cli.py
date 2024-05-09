import argparse

import odroid_wiringpi as wiringpi

from .protocol import transmit

__all__ = ["main"]


def parse_args():
    parser = argparse.ArgumentParser(description="Chacon 54662 remote control")
    parser.add_argument("-g", "--gpio", help="GPIO WiringPi pin number (default: 0)", type=int, choices=range(0, 30), metavar="[0-29]", default=0)
    parser.add_argument("-w", "--word", help="24-bit code word", type=int, required=True)
    parser.add_argument("-r", "--repeat", help="Number of times to repeat the message (default: 1)", type=int, default=1)
    return parser.parse_args()


def main():
    args = parse_args()

    if wiringpi.wiringPiSetup() == -1:
        raise Exception("Failed to initialize WiringPi")
    wiringpi.pinMode(args.gpio, wiringpi.OUTPUT)

    for _ in range(args.repeat):
        transmit(args.gpio, args.word)


if __name__ == "__main__":
    main()
