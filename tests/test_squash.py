from unittest.mock import patch
from pathlib import Path

from test_command_base import TestCommand
from commands.squash import SquashCommand


class TestSquash(TestCommand):
    def test_get_commit_message(self):
        with open(Path(self.repository.objects / "commit_hash"), 'w') as \
                commit:
            commit.write("commit message")
        assert "commit message" == SquashCommand._get_commit_message(
            self.repository, "commit_hash")

    # def test_squash(self):
    #     #todo

    # def test_cannot_squash_if_wrong_number_of_params(self):

    @patch('commands.reset.ResetCommand.execute')
    def test_cannot_squash_if_no_commits(self, mock_reset):
        SquashCommand().execute(1)
        mock_reset.assert_not_called()
