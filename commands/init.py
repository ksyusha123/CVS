import sys
from os.path import relpath
from pathlib import Path
import click

from repository import Repository


@click.command(help="Initialises a repository for current working directory")
def init():
    init_command()


def init_command():
    repository = Repository(Path.cwd())
    if repository.is_initialised:
        click.echo("Repository already exists")
        sys.exit()
    repository.init_required_paths()
    repository.index.touch()
    with open(repository.head, 'w') as head:
        head.write(relpath(repository.master, repository.cvs))
    click.echo("Repository has been created successfully")
