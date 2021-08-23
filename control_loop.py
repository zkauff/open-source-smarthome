import sys
import argparse
from controller import SmartController


def main(args):
    controller = SmartController(args.devices)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Control a variety of smarthome devices as specified by ~/.ossmarthome/conf')
    parser.add_argument('--log', help="Log information during the run.")
    args = parser.parse_args()
    main(args)
