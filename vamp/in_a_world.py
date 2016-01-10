"""Utility module for a world gone mad..."""

import os
from os.path import expanduser
import subprocess

# Initialize the pager stuff. Note, this will probably only work on *nixes
def get_max_lines():
    max_lines = None
    try:
        max_lines = subprocess.check_output(['tput', 'lines'])
    except (subprocess.CalledProcessError, FileNotFoundError):
        max_lines = os.environ.get('LINES', 30)
    return int(max_lines)

def get_max_columns():
    max_columns = None
    try:
        max_columns = subprocess.check_output(['tput', 'cols'])
    except (subprocess.CalledProcessError, FileNotFoundError):
        max_columns = os.environ.get('COLUMNS', 70)
    return int(max_columns)

def ensure_path(path):
    """Ensures a path exists"""
    if not os.path.exists(path):
        # Possible race condition, but fuck it
        os.makedirs(path)

def get_config_file():
    """Returns the system-specific config file. Will be created if it doesn't
    exist"""
    if 'XDG_CONFIG_HOME' in os.environ:
        config_home = expanduser(os.environ['XDG_CONFIG_HOME'])
    elif 'HOME' in os.environ:
        config_home = '{0}/.config'.format(expanduser(os.environ['HOME']))
    else:
        # Well, shit... Fuck it, dude, let's go bowling...
        config_home = '{0}/.config'.format(expanduser("~"))

    my_config = "{0}/vamp".format(config_home)

    ensure_path(my_config)

    return "{0}/config.ini".format(my_config)

def get_install_path():
    """Returns the system-specific default path for installation. Will be
    created if it doesn't exist"""
    if 'HOME' in os.environ:
        base_path = expanduser(os.environ['HOME'])
    else:
        base_path = expanduser("~")

    install_path = "{0}/vamp/install".format(base_path)

    ensure_path(install_path)

    return install_path

def get_bin_path():
    """Returns the system-specific default bin directory. Will be created if it
    doesn't exist"""
    if 'HOME' in os.environ:
        base_path = expanduser(os.environ['HOME'])
    else:
        base_path = expanduser("~")

    bin_path = "{0}/vamp/bin".format(base_path)

    ensure_path(bin_path)

    return bin_path
