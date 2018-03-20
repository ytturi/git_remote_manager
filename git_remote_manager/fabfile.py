# coding=utf-8
from fabric.api import run, cd, task
from fabric.state import output
from fabric import colors
from os.path import join
from tqdm import tqdm


from git_remote_manager.cli import PACKAGE_PREFIX
import logging

logger = logging.getLogger(PACKAGE_PREFIX.lower())

for k in output.keys():
    output[k] = False


def is_git_repository(path):
    with cd(path):
        files = run('ls -a')
        return '.git' in files


def is_repo_in_branch(src, repository, branch):
    with cd(join(src, repository)):
        res = run('git branch | grep \* | cut -d ' ' -f2-')
        return branch if branch in res else False


def list_repos(src):
    """
    List all repositories in src path
    :param src:         Source Path to list repositories
    :type src:          str
    :return:            A list of found reports
    :rtype:             list
    """
    repos = []
    with cd(src):
        dirs = run('ls -da *').split()
        for dir_name in tqdm(dirs, desc='Checking {}'.format(src)):
            if is_git_repository(dir_name):
                if logger.level <= logging.INFO:
                    tqdm.write('\t'+colors.green(dir_name))
                repos.append(dir_name)
    if not repos:
        logger.info(colors.red('No repositories found!'))
    return repos


@task
def check_repos(src, repository=False, branch=False):
    """
    Check for repositories in the source path. An specific repository or branch
    can be provided to check for specific branch on specific repository.
    :param src:         Source Path to list repositories
    :type src:          str
    :param repository:  Repository Name to find
    :type repository:   str
    :param branch:      Branch name which the repository must be
    :type branch:       str
    :return:            True if:
                        - There is any repo in `src`
                        - `repository` is in `src`
                        - `repository` is in `src` and
                            it's current branch name is `branch`
                        Else: False
    :rtype:             bool
    """
    repos = list_repos(src=src)
    if not repos:
        return False
    if repository and repository not in repos:
        logger.info(colors.red('Repository {} not found'.format(repository)))
        return False
    elif repository:
        logger.info(colors.green('Repositort {} found in {}'.format(
            repository, src
        )))
    if branch and not repository:
        logger.error('Repository is required to check for a branch!')
    if branch:
        return is_repo_in_branch(src, repository, branch)
    return any(repos)


