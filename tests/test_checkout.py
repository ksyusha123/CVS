from unittest.mock import patch
from pathlib import Path

from test_command_base import TestCommand
from commands.checkout import CheckoutCommand
from commands.add import AddCommand
from commands.commit import CommitCommand
from commands.branch import BranchCommand
from commands.tag import TagCommand
from position import Position


class TestCheckout(TestCommand):

    @patch('commands.checkout.CheckoutCommand._replace_head')
    def test_cannot_checkout_if_no_commit(self, mock_replace_head):
        CheckoutCommand().execute("some_position", None)
        mock_replace_head.assert_not_called()

    @patch('commands.checkout.CheckoutCommand._replace_head')
    def test_cannot_checkout_if_not_exist(self, mock_replace_head):
        with patch('repository.Repository.has_commits') as \
                mock_repos_has_commits:
            mock_repos_has_commits.return_value = True
            CheckoutCommand().execute("non-existing-position", None)
            mock_replace_head.assert_not_called()

    @patch('commands.checkout.CheckoutCommand._replace_head')
    def test_checkout_on_commit(self, mock_replace_head):
        Path('file').touch()
        AddCommand().execute('file')
        CommitCommand().execute('initial')
        initial_commit = self.repository.current_commit
        with open(Path('file'), 'w') as f:
            f.write('some text')
        AddCommand().execute('file')
        CommitCommand().execute('second')
        with patch('file_manager.update_index') as mock_update_index:
            with patch('file_manager.update_working_directory') as \
                    mock_update_wd:
                CheckoutCommand().execute(initial_commit, None)
                mock_replace_head.assert_called_once()
                mock_update_index.assert_called_once()
                mock_update_wd.assert_called_once()
        Path('file').unlink()

    @patch('commands.checkout.CheckoutCommand._create_branch')
    def test_checkout_with_creating_branch(self, mock_create_branch):
        Path('file').touch()
        AddCommand().execute('file')
        CommitCommand().execute('initial')
        CheckoutCommand().execute(None, "other_branch")
        mock_create_branch.assert_called_once()
        Path('file').unlink()

    @patch('commands.checkout.CheckoutCommand._replace_head')
    def test_checkout_on_tag(self, mock_replace_head):
        Path('file').touch()
        AddCommand().execute('file')
        CommitCommand().execute('initial')
        TagCommand().execute("tag")
        with patch('file_manager.update_index') as mock_update_index:
            with patch('file_manager.update_working_directory') as \
                    mock_update_wd:
                CheckoutCommand().execute("tag", None)
                mock_replace_head.assert_called_once()
                mock_update_index.assert_called_once()
                mock_update_wd.assert_called_once()

    @patch('commands.checkout.CheckoutCommand._replace_head')
    def test_checkout_on_branch(self, mock_replace_head):
        Path('file').touch()
        AddCommand().execute('file')
        CommitCommand().execute('initial')
        BranchCommand().execute("branch")
        with patch('file_manager.update_index') as mock_update_index:
            with patch('file_manager.update_working_directory') as \
                    mock_update_wd:
                CheckoutCommand().execute("branch", None)
                mock_replace_head.assert_called_once()
                mock_update_index.assert_called_once()
                mock_update_wd.assert_called_once()
        Path('file').unlink()

    def test_replace_head(self):
        CheckoutCommand._replace_head(self.repository, Position("path"))
        with open(self.repository.head) as head:
            assert "path" == head.readline()

    def test_create_branch(self):
        Path('file').touch()
        AddCommand().execute('file')
        CommitCommand().execute('initial')
        CheckoutCommand()._create_branch(self.repository, "some_branch")
        assert "some_branch" in self.repository.branches
        with open(self.repository.head) as head:
            assert "some_branch" in head.readline()
        Path('file').unlink()
