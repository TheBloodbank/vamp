from __future__ import print_function
import sys
from vamp.config import Config
from vamp.bank import Bank

class PackageBase:
    """The base definition of a package class."""

    # Simple requirements array. Should contain a list of packages this
    # package requires
    requires = []

    def __init__(self):
        pass

    def check_system_requirements(self):
        """Check the system requirements.

        When called, this should check to see if the necessary things are
        present on the system for this package to be installed and run.

        Returns True if they are met or False if they are not."""
        pass

    def test(self):
        print("Test from base class!")

class PackageHandler:
    __borg_state = {}

    def __init__(self, force=False):
        self.__dict__ = self.__borg_state

        self.c = Config()
        self.force = force
        self.b = Bank()

    def install(self, package):
        """Installs a package."""
        package = self.b.get_package(package)
        package.test()
