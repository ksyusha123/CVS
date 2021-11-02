from unittest.mock import patch, Mock, PropertyMock, call

from commands.branch import BranchCommand
from test_command_base import TestCommand

from commands.add import AddCommand
from commands.commit import CommitCommand
from pathlib import Path


class TestBranch(TestCommand):

    @patch('commands.branch.create_branch')
    def test_cannot_create_branch_if_no_commits(self, mock_create_branch):
        mock_create_branch.assert_not_called()

    @patch('commands.branch.create_branch')
    def test_create_branch(self, mock_create_branch):
        with patch('repository.Repository.current_position',
                   new_callable=PropertyMock) as mock_current_position:
            with patch('repository.Repository.has_commits',
                       new_callable=Mock) as mock_has_commits:
                mock_has_commits.return_value = True
                mock_current_position.return_value = "1234567890"
                BranchCommand().execute("main")
                assert "main" in mock_create_branch.call_args.args

    @patch('click.echo')
    def test_get_list_of_branches(self, mock_click_echo):
        Path('file').touch()
        AddCommand().execute('file')
        CommitCommand().execute('commit')
        BranchCommand().execute("second_branch")
        BranchCommand().execute("third_branch")
        BranchCommand().execute(None)
        mock_click_echo.assert_has_calls([call('  third_branch'),
                                          call('  second_branch'),
                                          call('->master')], any_order=True)
        Path('file').unlink()

    @patch('commands.branch.create_branch')
    def test_cannot_create_branch_if_exists(self, mock_create_branch):
        Path('file').touch()
        AddCommand().execute('file')
        CommitCommand().execute('commit')
        BranchCommand().execute("master")
        mock_create_branch.assert_not_called()
        Path('file').unlink()
