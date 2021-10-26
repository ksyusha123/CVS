import sys
from pathlib import Path
import click

from repository import Repository


@click.command(help="Shows commit history for current branch")
def log():
    log_command()


def log_command():
    repository = Repository(Path.cwd())
    if not repository.is_initialised:
        click.echo("Init a repository first")
        return
    repository.init_required_paths()
    if not repository.has_commits():
        click.echo("No commits yet")
        return
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
