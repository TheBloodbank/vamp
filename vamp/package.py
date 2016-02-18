from __future__ import print_function
import sys
from vamp.config import Config
from vamp.bank import Bank

class PackageHandler:
    __borg_state = {}

    def __init__(self, force=False):
        self.__dict__ = self.__borg_state

        self.c = Config()
        self.force = force
        self.b = Bank()

    def get_package(self, package):
        """Given a package name, will find the associated packae file in the
        bank and import it."""
        pass

    def install(self, package):
        """Installs a package."""
        package = self.get_package(package)
