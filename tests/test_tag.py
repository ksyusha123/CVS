from unittest.mock import patch, PropertyMock
from pathlib import Path

from test_command_base import TestCommand
from commands.tag import TagCommand


class TestTag(TestCommand):

    @patch('repository.Repository.all_tags', new_callable=PropertyMock)
    def test_cannot_create_tag_if_name_exists(self, mock_all_tags):
        mock_all_tags.return_value = {"tag"}
        TagCommand().execute("tag")
        with patch('commands.tag.TagCommand._create_tag') as mock_create_tag:
            mock_create_tag.assert_not_called()

    @patch('commands.tag.TagCommand._create_tag')
    def test_cannot_create_tag_without_commit(self, mock_create_tag):
        TagCommand().execute("tag")
        mock_create_tag.assert_not_called()

    @patch('repository.Repository.current_commit', new_callable=PropertyMock)
    def test_create_tag_on_current_commit(self, mock_current_commit):
        mock_current_commit.return_value = "1234"
        TagCommand._create_tag(self.repository, "tag", None)
        assert Path(self.repository.tags / "tag").exists()
        with open(Path(self.repository.tags / "tag")) as tag:
            assert "1234" == tag.readline()

    @patch('repository.Repository.get_commit_hash_of')
    def test_create_tag_on_commit(self, mock_get_commit_hash_of):
        mock_get_commit_hash_of.return_value = "1234"
        TagCommand._create_tag(self.repository, "tag", "1234")
        assert Path(self.repository.tags / "tag").exists()
        with open(Path(self.repository.tags / "tag")) as tag:
            assert "1234" == tag.readline()

    def test_cannot_create_tag_on_wrong_commit(self):
        TagCommand._create_tag(self.repository, "tag", "non-existing commit")
        assert not Path(self.repository.tags / "tag").exists()
