import click
from pathlib import Path

from command import Command


@click.command(help="Creates new branch")
@click.argument('branch_name', required=False)
def branch(branch_name):
    BranchCommand().execute(branch_name)


class BranchCommand(Command):

    def execute(self, branch_name):
        repository = self.get_repo()
        if branch_name is None:
            _print_all_branches(repository)
            return
        if not self._check_repository_is_ready(repository):
            click.echo("Make initial commit first")
        create_branch(repository, branch_name)

    @staticmethod
    def _check_repository_is_ready(repository):
        return repository.has_commits()


def create_branch(repository, name):
    with open(Path(repository.heads / name), 'w') as new_branch:
        with open(repository.head) as head:
            with open(repository.cvs / head.readline()) as current_branch:
                current_commit = current_branch.readline()
        new_branch.write(current_commit)


def _print_all_branches(repository):
    current_branch = repository.current_position.split('\\')[-1]
    for branch_name in repository.branches:
        if branch_name == current_branch:
            click.echo(f"->{current_branch}")
        else:
            click.echo(f"  {branch_name}")
