import os
from os.path import expanduser

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
