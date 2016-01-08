from vamp.in_a_world import get_config_file

try:
    import ConfigParser at configparser
except ImportError:
    import configparser

def load_config():
    config_file = get_config_file()

