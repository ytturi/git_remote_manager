# coding=utf-8
from fabric.api import run, cd, task
from fabric.state import output
from tqdm import tqdm
from fabric import colors


for k in output.keys():
    output[k] = False


def is_git_repository(path):
    with cd(path):
        files = run('ls -a')
        return '.git' in files


@task
def check_repos(src):
    with cd(src):
        dirs = run('ls -da *').split()
        for dir_name in tqdm(dirs, desc='Checking {}'.format(src)):
            if is_git_repository(dir_name):
                tqdm.write('\t'+colors.green(dir_name))

