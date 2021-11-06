from unittest.mock import patch
from pathlib import Path

from test_command_base import TestCommand
from commands.reset import ResetCommand
from commands.add import AddCommand
from commands.commit import CommitCommand


class TestReset(TestCommand):

    @patch('commands.reset.ResetCommand._replace_head_with_branch')
    def test_cannot_reset_to_wrong_commit(self, mock_replace_method):
        wrong_commit = "123"
        with patch('repository.Repository.has_commits') as \
                mock_repos_has_commits:
            mock_repos_has_commits.return_value = True
            ResetCommand().execute(wrong_commit, None)
            mock_replace_method.assert_not_called()

    @patch('file_manager.update_index')
    def test_reset_soft_only_replace_head_with_branch(self, mock_update_index):
        with patch('repository.Repository.get_commit_hash_of') \
                as mock_commit_hash, patch(
            'commands.reset.ResetCommand._replace_head_with_branch') \
                as mock_replace_method:
            mock_commit_hash.return_value = "123"
            mock_replace_method.return_value = None
            with patch('repository.Repository.has_commits') as \
                    mock_repos_has_commits:
                mock_repos_has_commits.return_value = True
                ResetCommand().execute("123", None)
                mock_update_index.assert_not_called()

    @patch('commands.reset.update_working_directory')
    def test_reset_mixed_only_update_index(self, mock_update_wd):
        with patch('repository.Repository.get_commit_hash_of') as \
                mock_commit_hash, \
             patch('commands.reset.ResetCommand._replace_head_with_branch') \
                as mock_replace_method:
            mock_commit_hash.return_value = "123"
            mock_replace_method.return_value = None
            with patch('commands.reset.update_index') as mock_update_index, \
                    patch('repository.Repository.has_commits') as \
                    mock_repos_has_commits:
                mock_repos_has_commits.return_value = True
                ResetCommand().execute("123", "mixed")
                mock_update_index.assert_called_once()
                mock_update_wd.assert_not_called()

    @patch('commands.reset.update_working_directory')
    def test_reset_hard_update_working_directory(self, mock_update_wd):
        with patch('repository.Repository.get_commit_hash_of') as \
                mock_commit_hash, patch(
            'commands.reset.ResetCommand._replace_head_with_branch') as \
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

    def test_replace_head_with_branch(self):
        Path('file').touch()
        AddCommand().execute('file')
        CommitCommand().execute('initial')
        first_commit = self.repository.current_commit
        with open(Path('file'), 'w') as f:
            f.write("text")
        AddCommand().execute('file')
        CommitCommand().execute('second')
        second_commit = self.repository.current_commit
        ResetCommand().execute("HEAD~1", option="soft")
        with open(self.repository.master) as master:
            assert first_commit == master.readline()
        with open(Path(self.repository.cvs / 'ORIG_HEAD')) as orig_head:
            assert second_commit == orig_head.readline()
        Path('file').unlink()
