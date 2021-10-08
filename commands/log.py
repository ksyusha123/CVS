import sys
from pathlib import Path
import click

from repository import Repository


@click.command(help="Shows commit history for current branch")
def log():
    repository = Repository(Path.cwd())
    if not repository.is_initialised:
        click.echo("Init a repository first")
        sys.exit()
    repository.init_required_paths()
    if not repository.has_commits():
        click.echo("No commits yet")
        sys.exit()
    with open(repository.head) as head:
        current_branch = head.readline()
        with open(Path(repository.cvs / current_branch)) as current:
            commit = current.readline()
            _print_commits_tree(commit, repository)


def _print_commits_tree(commit, repository):
    while True:
        with open(Path(repository.objects / commit)) as commit_obj:
            lines = commit_obj.readlines()
            click.echo(f"{commit} {lines[-1]}")
            if len(lines) == 4:
                commit = lines[1].split()[1]
            else:
                break
