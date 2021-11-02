from unittest.mock import patch
from pathlib import Path

from test_command_base import TestCommand
from repository import Repository
from commands.reset import ResetCommand


class TestReset(TestCommand):

    @patch('commands.reset.replace_head_with_branch')
    def test_cannot_reset_to_wrong_commit(self, mock_replace_method):
        wrong_commit = "123"
        with patch('repository.Repository.has_commits') as \
                mock_repos_has_commits:
            mock_repos_has_commits.return_value = True
            ResetCommand().execute(wrong_commit, None)
            mock_replace_method.assert_not_called()

    @patch('commands.reset.update_index')
    def test_reset_soft_only_replace_head_with_branch(self, mock_update_index):
        with patch('commands.reset._get_commit_hash') as mock_commit_hash:
            with patch('commands.reset.replace_head_with_branch') as \
                    mock_replace_method:
                mock_commit_hash.return_value = "123"
                mock_replace_method.return_value = None
                with patch('repository.Repository.has_commits') as \
                        mock_repos_has_commits:
                    mock_repos_has_commits.return_value = True
                    ResetCommand().execute("123", None)
                    mock_update_index.assert_not_called()

    @patch('commands.reset.update_working_directory')
    def test_reset_mixed_only_update_index(self, mock_update_wd):
        with patch('commands.reset._get_commit_hash') as mock_commit_hash:
            with patch('commands.reset.replace_head_with_branch') as \
                    mock_replace_method:
                mock_commit_hash.return_value = "123"
                mock_replace_method.return_value = None
                with patch('commands.reset.update_index') as mock_update_index:
                    with patch('repository.Repository.has_commits') as \
                            mock_repos_has_commits:
                        mock_repos_has_commits.return_value = True
                        ResetCommand().execute("123", "mixed")
                        mock_update_index.assert_called_once()
                        mock_update_wd.assert_not_called()

    @patch('commands.reset.update_working_directory')
    def test_reset_hard_update_working_directory(self, mock_update_wd):
        with patch('commands.reset._get_commit_hash') as mock_commit_hash:
            with patch('commands.reset.replace_head_with_branch') as \
                    mock_replace_method:
                mock_commit_hash.return_value = "123"
                mock_replace_method.return_value = None
                with patch('commands.reset.update_index') as mock_update_index:
                    with patch('repository.Repository.has_commits') as \
                            mock_repos_has_commits:
                        mock_repos_has_commits.return_value = True
                        ResetCommand().execute("123", "hard")
                        mock_update_index.assert_called_once()
                        mock_update_wd.assert_called_once()

    # def test_replace_head_with_branch(self):
    #     #todo
    #
    # def test_update_index(self):
    #     #todo
    #
    # def test_update_working_directory(self):
    #     #todo

