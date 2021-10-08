import sys
import click
from pathlib import Path

from repository import Repository


@click.command(help="Creates new branch")
@click.argument('name')
def branch(name):
    repository = Repository(Path.cwd())
    if not repository.is_initialised:
        click.echo("Init a repository first")
        sys.exit()
    repository.init_required_paths()
    with open(Path(repository.heads / name), 'w') as new_branch:
        with open(repository.head) as head:
            with open(repository.cvs / head.readline()) as current_branch:
                current_commit = current_branch.readline()
        new_branch.write(current_commit)
