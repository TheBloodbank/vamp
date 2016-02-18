from __future__ import print_function
import subprocess
import requests
from vamp.config import Config

def check_git():
    """Checks to see if git is available in path."""
    try:
        subprocess.check_output(['git', '--version'])
        return True
    except OSError:
        return False

class Git:
    """Git interface for vamp."""
    __borg_state = {}

    GITHUB_API_URL = 'https://api.github.com'

    def __init__(self):
        self.__dict__ = self.__borg_state

        self.c = Config()

    def get_url(self, full_name):
        """Get a URL ready for cloning given a 'full_name'.

        'full_name' must be of the format 'user/repo'.

        Returns the clone-able URL or None if no URL was found.
        """
        api_url = "{0}/repos/{1}".format(self.GITHUB_API_URL, full_name)
        r = requests.get(api_url)
        if r.status_code == 200:
            j = r.json()
            return j.get('clone_url', None)
        else:
            return None

    def clone(self, url, dest):
        """Clones the git repo at 'url' to the path at 'dest'."""
        print("> Cloning from '{0}'...".format(url))
        r = subprocess.check_output(['git', 'clone', url, dest])
        if self.c.get('globals', 'verbose', False):
            print(r)
