import subprocess
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

    def __init__(self):
        self.__dict__ = self.__borg_state

        self.c = Config()
