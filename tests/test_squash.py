from unittest.mock import patch
from pathlib import Path

from test_command_base import TestCommand
from commands.squash import SquashCommand
from commands.add import AddCommand
from commands.commit import CommitCommand


class TestSquash(TestCommand):
    def test_get_commit_message(self):
        with open(Path(self.repository.objects / "commit_hash"), 'w') as \
                commit:
            commit.write("commit message")
        assert "commit message" == SquashCommand._get_commit_message(
            self.repository, "commit_hash")

    # def test_squash(self):
    #     Path('file').touch()
    #     AddCommand().execute('file')
    #     CommitCommand().execute('initial')
    #     initial_commit = self.repository.current_commit
    #     with open(Path('file'), 'w') as f:
    #         f.write('text')
    #     AddCommand().execute('file')
    #     CommitCommand().execute('second')
    #     SquashCommand().execute(1)
    #     with open(Path('file')) as f:
    #         assert 'text' == f.readline()
    #     assert initial_commit == self.repository.current_commit
    #     Path('file').unlink()

    # def test_cannot_squash_if_wrong_number_of_params(self):

    @patch('commands.reset.ResetCommand.execute')
    def test_cannot_squash_if_no_commits(self, mock_reset):
        SquashCommand().execute(1)
        mock_reset.assert_not_called()
