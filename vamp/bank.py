from __future__ import print_function
import sys
import os.path
import shutil
from vamp.config import Config
from vamp.git import Git

# Various package types
class BloodbankPackage:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Bloodbank Package '{0}'>".format(self.name)

class GitRepoPackage:
    def __init__(self, name, url, cloned=False):
        self.name = name
        self.url = url
        self.already_cloned = cloned

    def __repr__(self):
        return "<Git Repo Package '{0}:{1}'>".format(self.name, self.url)

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

    def identify_package(self, package):
        """Given a package name, identify what type of package this is."""
        filename = '{0}/.bloodbank/.bank/{1}.py'.format(self.c.get('paths',
            'bank', True), package)
        if os.path.isfile(filename):
            return BloodbankPackage(package)
        else:
            if self.g.is_repo(package):
                return GitRepoPackage(package, package, False)
            else:
                # Check to see if it's a github user/repo string
                url = self.g.get_url(package)
                if url is not None:
                    return GitRepoPackage(package, url, False)
                else:
                    # Finally, see if it's already a cloned alt
                    namecoupled = package.split('/')
                    if len(namecoupled) == 2:
                        filepath = "{0}/{1}".format(self.c.get('paths',
                            'bank', True), namecoupled[1])
                        if self.g.is_repo(filepath) and os.path.isfile(
                                '{0}/.bank/{1}.py'.format(filepath,
                                namecoupled[1])):
                            return GitRepoPackage(package, filepath, True)
        return None
