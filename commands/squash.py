import click
from pathlib import Path

from command import Command
from commands.reset import replace_current_branch
from commands.reset import get_commit_from_end
from commands.commit import CommitCommand


@click.command(help="Combines commits")
@click.argument('commits_number', type=int)
def squash(commits_number):
    SquashCommand().execute(commits_number)


class SquashCommand(Command):

    def execute(self, commits_number):
        repository = self.get_repo()
        current_commit = repository.current_commit
        message = _get_commit_message(repository, current_commit)
        replace_current_branch(repository,
                               get_commit_from_end(repository, commits_number))
        CommitCommand().execute(message)


def _get_commit_message(repository, commit_hash):
    with open(Path(repository.objects / commit_hash)) as commit_obj:
        lines = commit_obj.readlines()
        message = lines[-1]
    return message
