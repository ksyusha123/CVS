import sys
import click
from pathlib import Path

from repository import Repository


@click.command(help="Creates new branch")
@click.argument('name', required=False)
def branch(name):
    repository = Repository(Path.cwd())
    if not repository.is_initialised:
        click.echo("Init a repository first")
        sys.exit()
    repository.init_required_paths()
    if name is None:
        _print_all_branches(repository)
        sys.exit()
    create_branch(repository, name)


def create_branch(repository, name):
    with open(Path(repository.heads / name), 'w') as new_branch:
        with open(repository.head) as head:
            with open(repository.cvs / head.readline()) as current_branch:
                current_commit = current_branch.readline()
        new_branch.write(current_commit)


def _print_all_branches(repository):
    current_branch = get_current_position(repository).split('\\')[-1]
    for branch_name in repository.branches:
        if branch_name == current_branch:
            click.echo(f"->{current_branch}")
        else:
            click.echo(f"  {branch_name}")


def get_current_position(repository):
    with open(repository.head) as head:
        current_branch = head.readline()
    return current_branch
