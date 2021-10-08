import sys
import click
from pathlib import Path

from repository import Repository


@click.command(help="Replaces HEAD to given position")
@click.argument('')
def checkout():
    repository = Repository(Path.cwd())
    if not repository.is_initialised:
        click.echo("Init a repository first")
        sys.exit()
    repository.init_required_paths()

