from pathlib import Path
import click

from command import Command
from position_type import PositionType
from file_manager import update_index, update_working_directory


@click.command(help='Replaces HEAD and current branch to given commit')
@click.option('--soft', 'option', is_flag=True, default=True,
              flag_value='soft',
              help='Is default option')
@click.option('--hard', 'option', is_flag=True,
              flag_value='hard',
              help='Updates index and working directory')
@click.option('--mixed', 'option', is_flag=True,
              flag_value='mixed',
              help='Updates index')
@click.argument('commit', required=True)
def reset(commit, option):
    ResetCommand().execute(commit, option)


class ResetCommand(Command):

    def execute(self, commit, option):
        repository = self.get_repo()
        if not repository.has_commits():
            click.echo("No commits yet")
            return
        commit = repository.get_commit_hash_of(commit)
        if commit is None:
            click.echo("There is no such commit")
            return
        self._replace_head_with_branch(repository, commit)
        if option == 'mixed' or option == 'hard':
            update_index(repository, commit)
            if option == 'hard':
                update_working_directory(repository)

    @staticmethod
    def _replace_head_with_branch(repository, commit):
        with open(Path(repository.cvs / 'ORIG_HEAD'), 'w') as orig_head:
            orig_head.write(repository.current_commit)
        current_position = repository.current_position
        if current_position.type == PositionType.branch:
            with open(Path(repository.cvs / repository.current_position.path),
                      'w') as current:
                current.write(commit)
        else:
            with open(repository.head, 'w') as head:
                head.write(commit)
