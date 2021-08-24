import sys
import argparse
from controller import SmartController


def main(args):
    controller = SmartController(args.logfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Control a variety of smarthome devices as specified by ~/.ossmarthome/conf')
    parser.add_argument('--configuration', help="Configuration file to use for SmartController. See README for questions about formatting.")
    parser.add_argument('--logfile', help="A file to log information to during the run.")
    args = parser.parse_args()
    main(args)
