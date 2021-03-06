import unittest
from pathlib import Path
from os.path import relpath
from unittest.mock import patch, PropertyMock

from repository import Repository
from position import Position
from commands.branch import BranchCommand
from commands.init import InitCommand
from commands.commit import CommitCommand
from commands.add import AddCommand
from commands.tag import TagCommand
from file_manager import delete_directory


class TestRepositorySimple(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        InitCommand().execute()
        cls.repository = Repository(Path.cwd())
        cls.repository.init_required_paths()

    @classmethod
    def tearDownClass(cls):
        delete_directory(Path(Path.cwd() / '.cvs'))

    def test_repository_is_initialised(self):
        assert self.repository.is_initialised

    def test_current_position(self):
        assert relpath(Path(self.repository.heads / "master"),
                       self.repository.cvs) == \
               self.repository.current_position.path
    #
    # def test_current_position_with_type(self):
    #     self.assertEqual(("master", PositionType.branch),
    #                      (self.repository.current_position.name,
    #                       self.repository.current_position.type))

    # def test_get_type_of_position(self):
    #     params = [("refs\\heads\\master", PositionType.branch),
    #               ("refs\\heads\\main", PositionType.branch),
    #               ("refs\\tags\\tag", PositionType.tag),
    #               ("1234567891011121314151617owefjlkdnfnmmmm",
    #                PositionType.commit)]
    #     for position, expected in params:
    #         with self.subTest():
    #             self.assertEqual(expected,
    #                              self.repository._get_type_of_position(
    #                                  position))

    def test_no_branches_if_no_commit(self):
        self.assertEqual(self.repository.branches, set())

    def test_has_no_commits(self):
        self.assertFalse(self.repository.has_commits())


class TestRepositoryAfterCommit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        InitCommand().execute()
        cls.repository = Repository(Path.cwd())
        cls.repository.init_required_paths()
        Path(Path.cwd() / 'file').touch()
        AddCommand().execute('file')
        CommitCommand().execute("initial")

    @classmethod
    def tearDownClass(cls):
        Path(Path.cwd() / 'file').unlink()
        delete_directory(Path(Path.cwd() / '.cvs'))

    def test_current_commit_if_position_is_not_commit(self):
        current_commit = self.repository.current_commit
        self.assertTrue(current_commit.isalnum() and
                        len(current_commit) == 40 and
                        "\\" not in current_commit and
                        "/" not in current_commit)

    def test_has_commits(self):
        self.assertTrue(self.repository.has_commits())

    def test_repository_branches(self):
        branches = {"master"}
        self.assertEqual(self.repository.branches, branches)
        BranchCommand().execute("new_branch")
        branches.add("new_branch")
        self.assertEqual(branches, self.repository.branches)

    def test_tags_list(self):
        TagCommand().execute("tag")
        self.assertEqual(self.repository.all_tags, {"tag"})


class TestRepositoryWithMagicMock(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        InitCommand().execute()
        cls.repository = Repository(Path.cwd())
        cls.repository.init_required_paths()

    @classmethod
    def tearDownClass(cls):
        delete_directory(Path(Path.cwd() / '.cvs'))

    def test_current_commit_if_current_position_is_commit(self):
        with patch('repository.Repository.current_position',
                   new_callable=PropertyMock) as mock_current_position:
            mock_current_position.return_value = Position(
                "1234567891011121314151617owefjlkdnfnmmmm")
            assert self.repository.current_commit == \
                   "1234567891011121314151617owefjlkdnfnmmmm"
