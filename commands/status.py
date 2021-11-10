import click
from command import Command


@click.command(help="Prints information about files in repository")
def status():
    StatusCommand().execute()


class StatusCommand(Command):

    def execute(self):
        repository = self.get_repo()
        click.echo()
        self._print_current_position(repository)
        self._print_untracked_files(repository)
        self._print_files_ready_for_commit(repository)
        self._print_modified_files(repository)

    @staticmethod
    def _print_files(files, message_if_no_files,
                     message):
        if len(files) == 0:
            click.echo(message_if_no_files)
        else:
            click.echo(message)
            for file in files:
                click.echo(f"\t{file}")
        click.echo()

    def _print_modified_files(self, repository):
        self._print_files(repository.modified_files,
                          "Working tree clean",
                          "Files not staged for commit:")

    def _print_files_ready_for_commit(self, repository):
        self._print_files(repository.files_ready_for_commit,
                          "Nothing to commit",
                          "Files ready for commit:")

    def _print_untracked_files(self, repository):
        self._print_files(repository.untracked_files,
                          "No untracked files",
                          "Untracked files:")

    @staticmethod
    def _print_current_position(repository):
        current_position = repository.current_position
        click.echo(
            f"On {current_position.type.name} {current_position.name}\n")
