import click
from pathlib import Path

from command import Command
from commands.reset import ResetCommand
from commands.commit import CommitCommand


@click.command(help="Combines commits")
@click.argument('commits_number')
def squash(commits_number):
    SquashCommand().execute(commits_number)


class SquashCommand(Command):

    def execute(self, commits_number):
        repository = self.get_repo()
        if not repository.has_commits():
            click.echo("Can't squash without any commit")
            return
        current_commit = repository.current_commit
        message = self._get_commit_message(repository, current_commit)
        ResetCommand().execute(f"HEAD~{commits_number}", "soft")
        CommitCommand().execute(message)

    @staticmethod
    def _get_commit_message(repository, commit_hash):
        with open(Path(repository.objects / commit_hash)) as commit_obj:
            lines = commit_obj.readlines()
            message = lines[-1]
        return message
