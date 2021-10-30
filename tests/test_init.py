from pathlib import Path
import unittest
from unittest.mock import patch

from commands.init import InitCommand
from repository import Repository
from helper import delete_directory


class TestInit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        InitCommand().execute()
        cls.repository = Repository(Path.cwd())

    @classmethod
    def tearDownClass(cls):
        delete_directory(Path(Path.cwd() / '.cvs'))

    def test_create_objects_after_init(self):
        self.assertTrue(self.repository.objects.exists())
        self.assertTrue(self.repository.index.exists())
        self.assertTrue(self.repository.cvs.exists())
        self.assertTrue(self.repository.refs.exists())
        self.assertTrue(self.repository.heads.exists())
        self.assertTrue(self.repository.tags.exists())

    @patch('click.echo')
    def test_not_create_cvs_if_was_init(self, mock_print):
        InitCommand().execute()
        assert mock_print.called_once_with("Repository exists")
