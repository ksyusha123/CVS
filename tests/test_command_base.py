import unittest
from pathlib import Path

from commands.init import InitCommand
from repository import Repository
from file_manager import delete_directory


class TestCommand(unittest.TestCase):
    def setUp(self):
        InitCommand().execute()
        self.repository = Repository(Path.cwd())
        self.repository.init_required_paths()

    def tearDown(self):
        delete_directory(Path(Path.cwd() / '.cvs'))
