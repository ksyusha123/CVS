import pytest
from pathlib import Path

from commands.init import InitCommand
from commands.status import StatusCommand
from commands.add import AddCommand
from commands.commit import commit
from commands.reset import reset
from repository import Repository
from helper import delete_directory


class TestStatus:

    def setup(self):
        InitCommand().execute()
        self.repository = Repository(Path.cwd())
        self.repository.init_required_paths()
        self.file = Path('file')
        self.file.touch()

    def teardown(self):
        delete_directory(Path(Path.cwd() / '.cvs'))
        self.file.unlink()

    # def test_print_position(self):


    def test_position_is_branch(self, capfd):
        StatusCommand().execute()
        out, err = capfd.readouterr()
        position = out.split('\n')[2]
        assert position == "On branch master"

    # def test_position_is_commit(self, capfd):
    #     add_command(self.file)

