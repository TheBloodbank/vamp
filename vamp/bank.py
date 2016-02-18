from __future__ import print_function
import sys
import os.path
import shutil
from vamp.config import Config
from vamp.git import Git

class Bank:
    __borg_state = {}

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
            clone_to = '{0}/.bloodbank'.format(self.c.get('paths', 'bank'))
        else:
            url = self.g.get_url(bank)
            clone_to = '{0}/{1}'.format(self.c.get('paths', 'bank'))

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
