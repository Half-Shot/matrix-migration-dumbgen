#!/usr/bin/env python3
import argparse
import logging
import sys

from hipchatGenerator import HipchatGenerator
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hipchat", help="select hipchat format",
                    action="store_true")
    parser.add_argument("-p", "--pass", help="Passphrase (omit if not encrypting)",
                    type=str)
    parser.add_argument("-u", "--users", help="N users to create",
                    type=int, default=0)
    parser.add_argument("-r", "--rooms", help="N rooms to create",
                    type=int, default=0)
    parser.add_argument("--min-msgs", help="Minimum number of messages to be created in a room",
                    type=int, default=200)
    parser.add_argument("--max-msgs", help="Maximum number of messages to be created in a room",
                    type=int, default=500)
    parser.add_argument("--email", help="E-mail address of the dummy users",
                    type=str)
    parser.add_argument("-P", help="N personal messages to create",
                    type=int, default=0)
    parser.add_argument("outfile", help="File to output to",
                    type=str)
    args = parser.parse_args()
    if args.users == 0 or args.rooms == 0:
        logging.critical("No users or rooms given to create. Specify with --users and --rooms")
        sys.exit(1)
    try:
        if args.hipchat:
            HipchatGenerator(args).start()
            pass
        else:
            logging.critical("No format given, not doing anything")
            sys.exit(1)
    except Exception as ex:
        logging.critical("Failed to run");
        raise ex

if __name__ == "__main__":
    main()