
[![Build Status](https://travis-ci.org/ytturi/git_remote_manager.svg?branch=master)](https://travis-ci.org/ytturi/git_remote_manager)

## Description

A python-based remote repository manager package.

Using [Fabric Tools](http://www.fabfile.org) for remote management and
[Click](http://click.pocoo.org/5/) for console-based scripts.

Using existing packages, and creating new ones, this repo is intended to:

- [x] Check existing repositories in a path
- [ ] Clone new repositories
- [ ] Get Status info
- [ ] Clean repository (checkout)
- [ ] Get Stash info
- [ ] Stash current changes
- [ ] Pop stash changes
- [ ] Get Branch info
- [ ] Change Branch (create, rename or move)
- [ ] Get Applied PRs (using [apply_pr](https://github.com/gisce/apply_pr))
- [ ] Deploy PR (using [apply_pr](https://github.com/gisce/apply_pr))
- [ ] Get tags info (describe)

And many more (yet to discover!)

## Usage

> Not yet (..)

- Check existing repositories in a path

python git_remote_manager/cli.py --host ssh://user@hostname
