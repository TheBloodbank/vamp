import json
import os.path

from vamp.in_a_world import get_manifest_file

class Manifest:
    __borg_state = {}

    def __init__(self):
        self.__dict__ = self.__borg_state

        self.manifest = {}
        self.manifest_file = get_manifest_file()

        if os.path.isfile(self.manifest_file):
            with open(self.manifest_file, 'r') as f:
                self.manifest = json.load(f)
        else:
            self.save()

    def set(self, section, key, value):
        """Set the value stored at 'key' in section 'section'."""
        if section not in self.manifest:
            self.manifest[section] = {}

        self.manifest[section][key] = value

    def get(self, section, key, default=None):
        """Get the value stored at 'key' in section 'section'."""
        if section in self.manifest:
            if key in self.manifest[section]:
                return self.manifest[section][key]
            else:
                return default
        else:
            return default

    def save(self):
        """Saves the current manifest to disk."""
        with open(self.manifest_file, 'w') as f:
            json.dump(self.manifest, f, indent=2)
