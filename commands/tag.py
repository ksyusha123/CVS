import click
from pathlib import Path

from command import Command


@click.command(help="Creates tag to commit")
@click.argument('name', required=False)
@click.argument('commit', required=False)
def tag(name, commit):
    TagCommand().execute(name, commit)


class TagCommand(Command):

    def execute(self, tag_name, commit=None):
        repository = self.get_repo()
        if tag_name is None:
            self._print_all_tags(repository)
            return
        if not repository.has_commits():
            click.echo("Make a commit first")
            return
        if tag_name in repository.all_tags:
            click.echo(f"{tag_name} already exists")
            return
        self._create_tag(repository, tag_name, commit)

    @staticmethod
    def _print_all_tags(repository):
        for tag_name in repository.all_tags:
            click.echo(tag_name)

    @staticmethod
    def _create_tag(repository, name, commit):
        if commit is None:
            commit = repository.current_commit
        else:
            commit = repository.get_commit_hash_of(commit)
            if commit is None:
                commit = repository.current_commit
        with open(Path(repository.tags / name), 'w') as new_tag:
            new_tag.write(commit)
