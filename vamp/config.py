try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from vamp.in_a_world import get_config_file, get_install_path, \
        get_bin_path

class Config:
    __borg_state = {}

    def __init__(self):
        self.__dict__ = self.__borg_state

        self.config = configparser.ConfigParser()
        self.config_file = get_config_file()
        self.config.read(self.config_file)
        save_config = False

        # Sensible defaults
        if 'paths' not in self.config:
            self.set_defaults()
            save_config = True

        if save_config:
            self.save()

    def set_defaults(self):
        self.config['paths'] = {
            'install' : get_install_path(),
            'bin' : get_bin_path()
            }

    def save(self):
        """Save the config file."""
        with open(self.config_file, 'w') as cf:
            self.config.write(cf)
