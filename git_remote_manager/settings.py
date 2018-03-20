from getpass import getuser
from os.path import join

PACKAGE_PREFIX = 'GIT_MANAGER'

DEFAULT_USER = getuser()
DEFAULT_SRC_PATH = join('/home', DEFAULT_USER, 'src')
