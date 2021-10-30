from pathlib import Path
import click

from command import Command


@click.command(help="Shows commit history for current branch")
def log():
    LogCommand().execute()


class LogCommand(Command):
    def execute(self):
        repository = self.get_repo()
        if not repository.has_commits():
            click.echo("No commits yet")
            return
        with open(repository.head) as head:
            current_branch = head.readline()
            with open(Path(repository.cvs / current_branch)) as current:
                commit = current.readline()
                self._print_commits_log(commit, repository)

    def _print_commits_log(self, commit, repository):
        commits_log = self.get_commits_log(repository, commit)
        for commit in commits_log:
            click.echo(commit)

    @staticmethod
    def get_commits_log(repository, commit):
        while True:
            with open(Path(repository.objects / commit)) as commit_obj:
                lines = commit_obj.readlines()
                yield commit, lines[-1]
                if len(lines) == 4:
                    commit = lines[1].split()[1]
                else:
                    break
