import sys
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from vamp.in_a_world import get_config_file, get_default_install_path, \
        get_default_bin_path, get_default_bank_path

class Config:
    __borg_state = {}

    def __init__(self):
        self.__dict__ = self.__borg_state

        self.config = configparser.ConfigParser()
        self.config_file = get_config_file()
        self.config.read(self.config_file)
        save_config = False

        if 'paths' not in self.config:
            self.set_defaults()
            save_config = True

        if save_config:
            self.save()

    def set_defaults(self):
        """Set some sensible defaults."""
        self.config['paths'] = {
            'install' : get_default_install_path(),
            'bin' : get_default_bin_path(),
            'bank' : get_default_bank_path()
            }
        sef.config['urls'] = {
            'bloodbank' = 'https://github.com/TheBloodbank/bank.git'
            }

    def get(self, section, setting, hard_fail=True):
        """Handles the retrieval and error reporting of config settings.

        If 'hard_fail' is True (default), then we require the setting be
        present and will exit on error.

        If 'hard_fail' is False, and we cannot find the section or setting,
        we return a None."""
        if section not in self.config:
            if hard_fail:
                print("Error! No '{0}' section in config file!".format(section))
                sys.exit(1)
            else:
                return None
        if setting not in self.config[section] and hard_fail:
            if hard_fail:
                print("Error! Setting '{0}' not found in section '{1}' in" + \
                    " the config file!".format(setting, section))
                sys.exit(1)
            else:
                return None

    def save(self):
        """Save the config file."""
        with open(self.config_file, 'w') as cf:
            self.config.write(cf)
