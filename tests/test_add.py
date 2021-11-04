from unittest.mock import patch
from pathlib import Path
from os.path import relpath

from commands.add import AddCommand
from commands.init import InitCommand
from repository import Repository
from helper import delete_directory
from test_command_base import TestCommand


class TestAdd(TestCommand):

    def setUp(self):
        InitCommand().execute()
        self.repository = Repository(Path.cwd())
        self.repository.init_required_paths()
        self.file = Path('file')
        self.file.touch()

    def tearDown(self):
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

    def test_add_directory_with_subdirectories(self):
        directory = Path('directory')
        directory.mkdir(parents=True, exist_ok=True)
        file1 = Path(directory / 'file1')
        file1.touch()
        subdirectory = Path(directory / 'subdirectory')
        subdirectory.mkdir(parents=True, exist_ok=True)
        file2 = Path(subdirectory / 'file2')
        file2.touch()
        AddCommand().execute('directory')
        with open(self.repository.index) as index:
            assert {'directory\\file1', 'directory\\subdirectory\\file2'} == \
                   {index.readline().split()[0], index.readline().split()[0]}
        delete_directory(directory)

    @patch('click.echo')
    def test_file_not_found(self, mock_click_echo):
        AddCommand().execute('non_existing')
        mock_click_echo.assert_called_once_with(
            "File not found. Check path name")

    def test_add_modified_file(self):
        AddCommand().execute(self.file.name)
        with open(self.file, 'w') as f:
            f.write('some text')
        AddCommand().execute(self.file.name)
        modified_file_hash = AddCommand.calculate_hash(self.repository,
                                                       self.file)
        with open(self.repository.index) as index:
            file_hash = index.readline().split()[1]
        assert file_hash == modified_file_hash
