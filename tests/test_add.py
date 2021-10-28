import pytest
from pathlib import Path
from os.path import relpath

from commands.add import AddCommand
from commands.add import calculate_hash
from commands.init import InitCommand
from repository import Repository
from helper import delete_directory


class TestAdd:

    def setup(self):
        InitCommand().execute()
        self.repository = Repository(Path.cwd())
        self.repository.init_required_paths()
        self.file = Path('file')
        self.file.touch()

    def teardown(self):
        delete_directory(Path(Path.cwd() / '.cvs'))
        self.file.unlink()

    def test_add_file(self):
        AddCommand().execute(self.file.name)
        with open(self.repository.index) as index:
            indexed_file = index.readline().split()
        assert indexed_file[0] == self.file.name

    def test_add_files_in_directory(self):
        Path('directory').mkdir(parents=True, exist_ok=True)
        file1 = Path(Path.cwd() / 'directory' / 'file1')
        file2 = Path(Path.cwd() / 'directory' / 'file2')
        file1.touch()
        file2.touch()
        AddCommand().execute('directory')
        with open(self.repository.index) as index:
            assert relpath(file1, Path.cwd()) == index.readline().split()[0]
            assert relpath(file2, Path.cwd()) == index.readline().split()[0]
        delete_directory(Path('directory'))

    def test_file_not_found(self, capfd):
        AddCommand().execute('non_existing')
        out, err = capfd.readouterr()
        add_message = out.split('\n')[1]
        assert add_message == "File not found. Check path name"

    def test_add_modified_file(self):
        AddCommand().execute(self.file.name)
        with open(self.file, 'w') as f:
            f.write('some text')
        AddCommand().execute(self.file.name)
        modified_file_hash = calculate_hash(self.repository, self.file)
        with open(self.repository.index) as index:
            file_hash = index.readline().split()[1]
        assert file_hash == modified_file_hash
