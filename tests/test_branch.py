import unittest
from unittest.mock import patch, Mock
from pathlib import Path

from commands.init import InitCommand
from commands.branch import BranchCommand
from repository import Repository
from helper import delete_directory


class TestBranch(unittest.TestCase):

    def setUp(self):
        InitCommand().execute()
        self.repository = Repository(Path.cwd())
        self.repository.init_required_paths()

    def tearDown(self):
        delete_directory(Path(Path.cwd() / '.cvs'))

    @patch('commands.branch.create_branch')
    def test_cannot_create_branch_if_no_commits(self, mock_create_branch):
        assert not mock_create_branch.called

    @patch('commands.branch.create_branch')
    def test_create_branch(self, mock_create_branch):
        self.repository.current_position = Mock(return_value=
                                   "kdjfusfjijwoefksflknsdnfnjbsbd134324kjns")
        BranchCommand().execute("main")
        assert mock_create_branch.called_once_with("main")


