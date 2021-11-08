from pathlib import Path
from unittest.mock import patch

from test_command_base import TestCommand
from commands.add import AddCommand
from commands.commit import CommitCommand
from commands.log import LogCommand
from commands.reset import ResetCommand
from commands.checkout import CheckoutCommand


class TestLog(TestCommand):

    @patch('click.echo')
    def test_no_commits(self, mock_click_echo):
        LogCommand().execute()
        mock_click_echo.assert_called_once_with("No commits yet")

    @patch('click.echo')
    def test_get_commits_log(self, mock_click_echo):
        Path('file').touch()
        AddCommand().execute('file')
        CommitCommand().execute('first commit')
        with open('file', 'w') as f:
            f.write('some text')
        AddCommand().execute('file')
        CommitCommand().execute('second commit')
        LogCommand().execute()
        mock_click_echo.assert_called()

    @patch('click.echo')
    def test_log_if_current_position_is_commit(self, mock_click_echo):
        Path('file').touch()
        AddCommand().execute('file')
        CommitCommand().execute('first commit')
        with open('file', 'w') as f:
            f.write('some text')
        AddCommand().execute('file')
        CommitCommand().execute('second commit')
        ResetCommand().execute('HEAD~1', None)
        mock_click_echo.assert_called()

    def test_log_should_print_commits_from_current_branch(self):
        Path('file').touch()
        AddCommand().execute('file')
        CommitCommand().execute('initial commit')
        with open('file', 'w') as f:
            f.write('some text')
        AddCommand().execute('file')
        CommitCommand().execute('second commit in master')
        ResetCommand().execute("HEAD~1", None)
        CheckoutCommand().execute(None, "new_branch")
        with open('file', 'w') as f:
            f.write('some other text')
        AddCommand().execute('file')
        CommitCommand().execute('second commit in new_branch')
        commits_log = LogCommand._get_commits_log(
            self.repository, self.repository.current_commit)
        commits_log_messages = [commit_log[1] for commit_log in
                                commits_log]
        assert 'initial commit' in commits_log_messages
        assert 'second commit in master' not in commits_log_messages
        assert 'second commit in new_branch' in commits_log_messages
