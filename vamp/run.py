#!/usr/bin/env python

from __future__ import print_function
import sys
import argparse
import textwrap

from vamp.in_a_world import get_max_lines, get_max_columns

MAX_PAGE_LINES = get_max_lines()
MAX_PAGE_WIDTH = get_max_columns()

# Command Methods
def command_init():
    """Foo"""
    pass

commands = {
        'init' : {
            'method' : command_init,
            'desc' : 'Initialize the system.'
        }
    }

# Main entry point
def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="The command to run", nargs="?")
    parser.add_argument("-l", "--list", help="List the commands available",
        action="store_true")
    args = parser.parse_args()

    if args.list:
        key_len = len(max(commands.keys(), key=len))
        desc_len = MAX_PAGE_WIDTH - 5 - key_len
        for cmd in sorted(commands.keys()):
            desc = textwrap.wrap(commands[cmd]['desc'], desc_len)
            print('  {0} : {1}'.format(cmd.rjust(key_len), desc[0]))
            for i in range(1, len(desc)):
                print(' ' * (5 + key_len) + '{0}'.format(desc[i]))
        sys.exit(0)

    if args.command in commands:
        commands[args.command]['method']()
    else:
        print("Valid command required!")
        parser.print_usage()
        sys.exit(1)
