import unittest
from pathlib import Path
import re

from commands.commit import CommitCommand
from commands.add import AddCommand
from commands.init import InitCommand
from helper import delete_directory
from repository import Repository


class TestCommit(unittest.TestCase):

    def setUp(self):
        InitCommand().execute()
        self.repository = Repository(Path.cwd())
        self.repository.init_required_paths()
        self.file = Path('file')
        self.file.touch()
        AddCommand().execute(self.file)
        CommitCommand().execute("first")

    def tearDown(self):
        delete_directory(Path(Path.cwd() / '.cvs'))
        self.file.unlink()

    def test_not_create_commit_if_no_files_to_commit(self):
        with open(self.repository.master) as branch:
            first_commit_hash = branch.readline()
        CommitCommand().execute("second")
        with open(self.repository.master) as branch:
            second_commit_hash = branch.readline()
        assert first_commit_hash == second_commit_hash
        with open(Path(self.repository.objects / first_commit_hash)) as first:
            first_commit = first.read()
        with open(Path(self.repository.objects / second_commit_hash)) as \
                second:
            second_commit = second.read()
        assert first_commit == second_commit

    def test_create_new_commit(self):
        with open(self.repository.master) as branch:
            first_commit_hash = branch.readline()
        with open(Path(self.repository.objects / first_commit_hash)) as first:
            first_commit = first.read()
        assert re.fullmatch(r'tree \w{40}\n\nfirst', first_commit)

    def test_correct_commit_connection(self):
        expected_parent_commit = self.repository.current_commit
        with open(self.file, 'w') as f:
            f.write("text")
        AddCommand().execute(self.file)
        CommitCommand().execute("second")
        child_commit = self.repository.current_commit
        with open(Path(self.repository.objects / child_commit)) as child:
            actual_parent_commit = \
                child.readlines()[1].split()[1].split('\n')[0]
        assert expected_parent_commit == actual_parent_commit

    def test_cannot_work_with_incorrect_commit(self):
        #todo
