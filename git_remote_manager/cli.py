# coding=utf-8
from fabric.tasks import execute, WrappedCallableTask
from fabric.api import env
from getpass import getpass
from osconf import config_from_environment
from urlparse import urlparse

import logging
import click

from git_remote_manager import fabfile
from git_remote_manager.settings import PACKAGE_PREFIX, DEFAULT_USER
from git_remote_manager.settings import DEFAULT_SRC_PATH


def configure_logging(verbose=False, debug=False):
    level = logging.WARNING
    if debug:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
    logging.basicConfig(
        format='%(message)s',
        level=level
    )
    return logging.getLogger(PACKAGE_PREFIX)


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
    logger = logging.getLogger(PACKAGE_PREFIX)
    if not required:
        required = []
    try:
        return config_from_environment(
            PACKAGE_PREFIX, required,
            **defaults
        )
    except Exception as err:
        logger.critical(err.message)
        return False


@click.command(name='get_repos')
@click.option(
    '-h', '--host', type=str, default=False,
    help='Host to connect at ({env_var})[{value}]'.format(
        env_var='{}_HOST'.format(PACKAGE_PREFIX),
        value='ssh://{}@hostname'.format(DEFAULT_USER)))
@click.option(
    '-u', '--user', type=str, default=False,
    help='User for remote connection ({env_var})[{value}]'.format(
        env_var='{}_USER'.format(PACKAGE_PREFIX),
        value=DEFAULT_USER))
@click.option(
    '-s', '--src', type=str, default=False,
    help='User for remote connection ({env_var})[{value}]'.format(
        env_var='{}_USER'.format(PACKAGE_PREFIX),
        value=DEFAULT_USER))
@click.option(
    '-r', '--repository', type=str, default=False,
    help='Repository to check for (empty to list all repositories)')
@click.option(
    '-b', '--branch', type=str, default=False,
    help='Branch to check the repository is in(requires "-r" )')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Verbose level as INFO')
@click.option('-d', '--debug', is_flag=True, default=False,
              help='Verbose level as DEBUG')
def check_repositories(**kwargs):
    logger = configure_logging(verbose=kwargs.get('verbose', False),
                               debug=kwargs.get('debug', False))
    confs = manager_confs(kwargs, required=['host'])
    if confs is False:
        exit(-1)
    for key, value in kwargs.items():
        if key in confs.keys() and kwargs[key] is not False \
                and confs[key] != value:
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

    src_path = (confs['src'] or DEFAULT_SRC_PATH).strip()

    check_repositories_task = WrappedCallableTask(fabfile.check_repos)
    execute(
        check_repositories_task, src=src_path, host=url.hostname,
        repository=kwargs.get('repository', False),
        branch=kwargs.get('branch', False),
    )


if __name__ == '__main__':
    check_repositories()
