import pytest
from pathlib import Path
from checksumdir import dirhash

from commands import commit
from commands import add
from commands import init
from helper import delete_directory
from repository import Repository


class TestCommit:

    def setup(self):
        init.init_command()
        self.repository = Repository(Path.cwd())
        self.repository.init_required_paths()
        self.file = Path('file')
        self.file.touch()

    def teardown(self):
        delete_directory(Path(Path.cwd() / '.cvs'))
        self.file.unlink()

    def test_not_create_commit_if_no_files_to_commit(self):
        add.add_command(self.file)
        commit.commit_command("first")
        with open(self.repository.master) as branch:
            first_commit_hash = branch.readline()
        commit.commit_command("second")
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
        add.add_command(self.file)
        repository_hash = dirhash(self.repository.path, 'sha1')
        commit.commit_command("first")
        with open(self.repository.master) as branch:
            first_commit_hash = branch.readline()
        with open(Path(self.repository.objects / first_commit_hash)) as first:
            first_commit = first.read()
        assert (first_commit ==
                f"tree {repository_hash}\n\nfirst")

    def test_correct_commit_connection(self):
        add.add_command(self.file)
        commit.commit_command("first")
        expected_parent_commit = self.repository.current_commit
        with open(self.file, 'w') as f:
            f.write("text")
        add.add_command(self.file)
        commit.commit_command("second")
        child_commit = self.repository.current_commit
        with open(Path(self.repository.objects / child_commit)) as child:
            actual_parent_commit = \
                child.readlines()[1].split()[1].split('\n')[0]
        assert expected_parent_commit == actual_parent_commit


    # def test_create_initial_commit(self):
    #     commit.commit_command()