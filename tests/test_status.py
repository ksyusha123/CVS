from pathlib import Path

from commands.init import InitCommand
from commands.status import StatusCommand
from commands.add import AddCommand
from commands.commit import commit
from commands.reset import reset
from repository import Repository
from helper import delete_directory
from test_command_base import TestCommand


class TestStatus(TestCommand):

    def setup(self):
        InitCommand().execute()
        self.repository = Repository(Path.cwd())
        self.repository.init_required_paths()
        self.file = Path('file')
        self.file.touch()

    def teardown(self):
        delete_directory(Path(Path.cwd() / '.cvs'))
        self.file.unlink()

