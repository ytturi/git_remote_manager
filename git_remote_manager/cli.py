# coding=utf-8
from fabric.tasks import execute, WrappedCallableTask
from fabric.api import env
from getpass import getuser, getpass
from osconf import config_from_environment
from os.path import join
from urlparse import urlparse
import click


from git_remote_manager import fabfile


PACKAGE_PREFIX = 'GIT_MANAGER'
DEFAULT_USER = getuser()
DEFAULT_SRC_PATH = join('/home', DEFAULT_USER, 'src')


def manager_confs(defaults, required=False):
    """
    Check for MANAGER confs in environment.
    Default values and required keys can be provided
    :param defaults: Default Values if not found on environment
    :type defaults:  dict
    :param required: Required Keys to be set either by environment or defaults
    :type required:  list
    :return:         Dictionary with all values from environment or
                        False if missing required values
    :rtype:          dict
    """
    if not required:
        required = []
    try:
        return config_from_environment(
            PACKAGE_PREFIX, required,
            **defaults
        )
    except Exception as err:
        print(err.message)
        return False


@click.command(name='get_repos')
@click.option(
    '-h', '--host', type=str, default='',
    help='Host to connect at ({env_var})[{value}]'.format(
        env_var='{}_HOST'.format(PACKAGE_PREFIX),
        value='ssh://{}@hostname'.format(DEFAULT_USER),
    )
)
@click.option(
    '-u', '--user', type=str, default='',
    help='User for remote connection ({env_var})[{value}]'.format(
        env_var='{}_USER'.format(PACKAGE_PREFIX),
        value=DEFAULT_USER,
    )
)
@click.option(
    '-s', '--src', type=str, default='',
    help='User for remote connection ({env_var})[{value}]'.format(
        env_var='{}_USER'.format(PACKAGE_PREFIX),
        value=DEFAULT_USER,
    )
)
def check_repositories(**kwargs):
    confs = manager_confs(kwargs, required=['host'])
    if confs is False:
        exit(-1)
    for key, value in kwargs:
        if key in confs.keys() and confs[key] != value:
            confs.update({key: value})
    url = urlparse(confs['host'])

    env.user = (
        url.username or confs['user'] or DEFAULT_USER
    ).strip()

    env.password = (
        url.password or
        confs.get('passwd', False) or
        getpass(
            'Password for [{}](empty if working with keys):'
            ''.format(confs['host'])) or
        ''
    ).strip()

    src_path = (
        confs['src'] or DEFAULT_SRC_PATH
    ).strip()

    check_repositories_task = WrappedCallableTask(fabfile.check_repos)
    execute(check_repositories_task, src=src_path, host=url.hostname)


if __name__ == '__main__':
    check_repositories()
