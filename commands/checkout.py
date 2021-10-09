import sys
import click
from os.path import relpath
from pathlib import Path

from repository import Repository
from commands.reset import update_index, update_working_directory


@click.command(help="Replaces HEAD to given position")
@click.argument('position', required=True)
# @click.option('-b', '--branch', required=False)
def checkout(position):
    repository = Repository(Path.cwd())
    if not repository.is_initialised:
        click.echo("Init a repository first")
        sys.exit()
    repository.init_required_paths()
    if position in repository.branches:
        position = relpath(Path(repository.heads / position), repository.cvs)
        with open(repository.cvs / position) as current_branch:
            commit = current_branch.readline()
    with open(repository.head, 'w') as head:
        head.write(position)
    update_index(repository, commit)
    update_working_directory(repository)
