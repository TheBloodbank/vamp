from __future__ import print_function
import sys
import os.path
import shutil
from vamp.config import Config
from vamp.git import Git
from vamp.kittening_importer import kitten_importer

class Bank:
    __borg_state = {}
    BLOODBANK = '.bloodbank'
    GITHUBBANK = '.github'

    def __init__(self):
        self.__dict__ = self.__borg_state

        self.c = Config()
        self.g = Git()

    def init_bank(self, bank=None, force=False):
        """Initializes a bank.

        'bank' should be a string of the format 'user/repo'.

        If 'bank' is not specified, will init the main bloodbank.
        """
        clone_to = None
        url = None
        if bank is None:
            url = self.c.get('urls', 'bloodbank')
            clone_to = '{0}/{1}'.format(self.c.get('paths', 'bank'),
                    self.BLOODBANK)
        else:
            url = self.g.get_url(bank)
            clone_to = '{0}/{1}/{2}'.format(self.c.get('paths', 'bank'),
                    self.GITHUBBANK, bank)

        if url is None:
            print("Error! No valid URL found for '{0}'!".format(bank))
            sys.exit(1)

        if os.path.isdir(clone_to):
            if force:
                print("!! Bank directory exists, but overwriting because " + \
                        "of --force")
                shutil.rmtree(clone_to)
                self.g.clone(url, clone_to)
            else:
                print("!! Bank directory exists, using existing")
        else:
            self.g.clone(url, clone_to)

    def get_package(self, package):
        """Given a package name, import the package object and return it."""
        # We have to run through a number of sources to get the package
        filename = '{0}/{1}/.bank/{2}.py'.format(self.c.get('paths',
            'bank', True), self.BLOODBANK, package)
        if os.path.isfile(filename):
            return kitten_importer(filename, 'bloodbank.{0}'.format(package))
        else:
            if self.g.get_url(package) is not None:
                appname = package.split('/')[-1]
                self.init_bank(package)
                filename = "{0}/{1}/.bank/{2}.py".format(self.c.get('paths',
                    'bank', True), self.GITHUBBANK, appname)
                is os.path.isfile(filename):
                    return kitten_importer(filename, 'bloodbank.{0}'.format(
                        appname))
        return None
