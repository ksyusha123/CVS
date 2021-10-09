import sys
import click
from os.path import relpath
from pathlib import Path

from repository import Repository
from commands.reset import update_index, update_working_directory
from commands.branch import create_branch


@click.command(help="Replaces HEAD to given position")
@click.argument('position', required=False)
@click.option('-b', '--branch', 'branch_name', required=False,
              help="Creates new branch with given name")
def checkout(position, branch_name):
    repository = Repository(Path.cwd())
    if not repository.is_initialised:
        click.echo("Init a repository first")
        sys.exit()
    repository.init_required_paths()
    if branch_name:
        create_branch(repository, branch_name)
        position = relpath(
            Path(repository.heads / branch_name), repository.cvs)
        _replace_head(repository, position)
        sys.exit()
    if position in repository.branches:
        position = relpath(Path(repository.heads / position), repository.cvs)
        with open(repository.cvs / position) as current_branch:
            commit = current_branch.readline()
    _replace_head(repository, position)
    update_index(repository, commit)
    update_working_directory(repository)


def _replace_head(repository, position):
    with open(repository.head, 'w') as head:
        head.write(position)
