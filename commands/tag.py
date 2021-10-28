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
            _print_all_tags(repository)
            return
        _create_tag(repository, tag_name, commit)


def _print_all_tags(repository):
    for tag_name in repository.all_tags:
        click.echo(tag_name)


def _create_tag(repository, name, commit):
    if commit is None:
        commit = _get_last_commit(repository)
    with open(Path(repository.tags / name), 'w') as new_tag:
        new_tag.write(commit)


def _get_last_commit(repository):
    with open(repository.head) as head:
        with open(repository.cvs / head.readline()) as current_branch:
            current_commit = current_branch.readline()
    return current_commit
