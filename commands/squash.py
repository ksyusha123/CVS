import click
import sys
from pathlib import Path

from repository import Repository
from commands.reset import replace_current_branch
from commands.reset import get_commit_from_end
from commands.commit import commit_command


@click.command(help="Combines commits")
@click.argument('commits_number', type=int)
def squash(commits_number):
    squash_command(commits_number)


def squash_command(commits_number):
    repository = Repository(Path.cwd())
    if not repository.is_initialised:
        click.echo("Init a repository first")
        return
    repository.init_required_paths()
    current_commit = repository.current_commit
    message = _get_commit_message(repository, current_commit)
    replace_current_branch(repository,
                           get_commit_from_end(repository, commits_number))
    commit_command(message)


def _get_commit_message(repository, commit_hash):
    with open(Path(repository.objects / commit_hash)) as commit_obj:
        lines = commit_obj.readlines()
        message = lines[-1]
    return message
