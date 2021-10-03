import sys
from pathlib import Path
import click

from Repository import Repository


@click.command()
def init():
    repository = Repository(Path.cwd())
    if repository.is_initialised:
        click.echo("Repository already exists")
        sys.exit()
    repository.init_required_paths()
    Path(repository.path/'.cvs').mkdir()
    Path(repository.cvs/'objects').mkdir()
    with open(repository.index, 'w') as index:
        pass
    click.echo("Repository has been created successfully")
