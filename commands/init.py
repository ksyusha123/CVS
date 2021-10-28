from os.path import relpath
import click

from command import Command


@click.command(help="Initialises a repository for current working directory")
def init():
    InitCommand().execute()


class InitCommand(Command):

    def __init__(self):
        super().__init__("Repository exists")

    def check(self, repository):
        return not repository.is_initialised

    def execute(self):
        repository = self.get_repo()
        repository.index.touch()
        with open(repository.head, 'w') as head:
            head.write(relpath(repository.master, repository.cvs))
        click.echo("Repository has been created successfully")
