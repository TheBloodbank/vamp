#!/usr/bin/env python3

from __future__ import print_function
import sys
import argparse
import textwrap
from colorama import init, Fore, Style

try:
    get_input = raw_input
except NameError:
    get_input = input

try:
    # Win32
    from msvcrt import getch
except ImportError:
    # UNIX
    def getch():
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

from vamp.in_a_world import get_max_lines, get_max_columns

# UI setup
MAX_PAGE_LINES = get_max_lines()
MAX_PAGE_WIDTH = get_max_columns()
CURRENT_LINE = 0
PAGE_TEXT = Style.BRIGHT + \
    "Press any key to continue, Q to quit...\r" + Style.NORMAL
CLEAR_TEXT = ' ' * len(PAGE_TEXT) + "\r"
RESET_TEXT = Fore.RESET + Style.NORMAL
init()

# The pagination method
def pager(line=""):
    if not args.machine:
        global CURRENT_LINE
        global MAX_PAGE_LINES
        if CURRENT_LINE > MAX_PAGE_LINES - 3 and not args.no_page:
            print(PAGE_TEXT, end="")
            c = getch()
            print(CLEAR_TEXT, end="")
            CURRENT_LINE = 0
            MAX_PAGE_LINES = get_max_lines()
            if c == 'q' or c == 'Q' or ord(c) == 3:
                sys.exit(0)
        try:
            print(line)
        except UnicodeEncodeError:
            print(line.encode('ascii', 'replace'))
        if not args.no_page:
            CURRENT_LINE = CURRENT_LINE + 1

# Parser setup
parser = argparse.ArgumentParser()
parser.add_argument("command", help="The command to run", nargs="?")
parser.add_argument("subcommand", help="Optional sub-command.", nargs="?")
parser.add_argument("-l", "--list", help="List the commands available",
    action="store_true")
args = parser.parse_args()

# Command Methods
def command_init():
    """Foo"""
    pass

def command_help():
    """Display the help system"""
    if args.subcommand in commands:
        pager(Style.BRIGHT + "SYNOPSIS" + RESET_TEXT)
        pager("   vamp {0}".format(args.subcommand))
        pager()
        pager(Style.BRIGHT + "DESCRIPTION" + RESET_TEXT)
        desc_len = MAX_PAGE_WIDTH - 5
        desc = textwrap.wrap(commands[args.subcommand]['desc'], desc_len)
        for i in range(1, len(desc)):
            pager("   {0}".format(desc[i]))
        # ERE I AM JH, display help
    else:
        parser.print_usage()

commands = {
        'init' : {
            'method' : command_init,
            'desc' : 'Initialize the system.',
            'help' : [
                'Sub-commands:',
                '-------------',
                '',
                'all : Initialize all sub-systems. This is the ' + \
                        'default behavior if no sub-command is specified',
                'config : Initialize/prepare a default configuration',
                'bank : Initialize the bank'
                ]
        },
        'help' : {
            'method' : command_help,
            'desc' : 'Display vamp command help.',
            'help' : [
                'When called with no sub-command, will display the ' + \
                'vamp usage information.',
                '',
                'When called with the name of a command, display the help ' + \
                'for that command.'
                ]
        }
    }

# Main entry point
def run():
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
