try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from vamp.in_a_world import get_config_file, get_install_path, \
        get_bin_path

def load_config():
    config = configparser.ConfigParser()
    config_file = get_config_file()
    config.read(config_file)
    save_config = False

    # Sensible defaults
    if 'paths' not in config:
        config['paths'] = {
                'install' : get_install_path(),
                'bin' : get_bin_path()
                }
        save_config = True

    if save_config:
        with open(config_file, 'w') as cf:
            config.write(cf)

    return config
