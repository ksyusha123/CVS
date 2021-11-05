import click
from os.path import relpath
from pathlib import Path

from command import Command
import file_manager
from commands.branch import BranchCommand
from position import Position


@click.command(help="Replaces HEAD to given position")
@click.argument('position', required=False)
@click.option('-b', '--branch', 'branch_name', required=False,
              help="Creates new branch with given name")
def checkout(position, branch_name):
    CheckoutCommand().execute(position, branch_name)


class CheckoutCommand(Command):

    def execute(self, position, branch_name):
        repository = self.get_repo()
        if not repository.has_commits():
            click.echo("Create repository first")
            return
        if branch_name:
            self._create_branch(repository, branch_name)
            return
        if position in repository.branches:
            position = Position(relpath(Path(repository.heads / position),
                                        repository.cvs))
            with open(repository.cvs / position.path) as current_branch:
                commit = current_branch.readline()
        elif position in repository.all_tags:
            with open(repository.tags / position) as tag:
                commit = tag.readline()
                position = Position(commit)
        else:
            if not Path(repository.objects / position).exists():
                click.echo("That commit does not exist. Check its correctness")
                return
            commit = position
            position = Position(position)
        self._replace_head(repository, position)
        file_manager.update_index(repository, commit)
        file_manager.update_working_directory(repository)

    @staticmethod
    def _replace_head(repository, position):
        with open(repository.head, 'w') as head:
            head.write(position.path)

    def _create_branch(self, repository, branch_name):
        BranchCommand.create_branch(repository, branch_name)
        position = Position(relpath(
            Path(repository.heads / branch_name), repository.cvs))
        self._replace_head(repository, position)
