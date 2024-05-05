import argparse

import odroid_wiringpi as wiringpi

from .protocol import transmit


def parse_args():
  parser = argparse.ArgumentParser(description="Chacon DIO 1.0 remote control")
  parser.add_argument("-g", "--gpio", help="GPIO WiringPi pin number (default: 0)", type=int, choices=range(0, 30), metavar="[0-29]", default=0)
  parser.add_argument("-s", "--sender", help="Sender code 26-bit number", type=int, required=True)
  parser.add_argument("-b", "--button", help="Button number between 0 and 15, -1 for all (group function)", type=int, choices=range(-1, 16), metavar="[0-15]", required=True)
  parser.add_argument("-o", "--onoff", help="0 (OFF) or 1 (ON)", type=int, choices=range(0, 2), metavar="[0-1]", required=True)
  parser.add_argument("-r", "--repeat", help="Number of times to repeat the message (default: 5)", type=int, default=5)
  return parser.parse_args()

def main():
  args = parse_args()
  group = True if args.button < 0 else False
  button = 0 if args.button < 0 else args.button
  onoff = True if args.onoff > 0 else False

  if wiringpi.wiringPiSetup() == -1:
    raise Exception("Failed to initialize WiringPi")
  wiringpi.pinMode(args.gpio, wiringpi.OUTPUT)

  for i in range(args.repeat):
    transmit(args.gpio, args.sender, group, button, onoff)

if __name__ == "__main__":
  main()
