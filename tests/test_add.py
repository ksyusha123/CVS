import pytest
from pathlib import Path
from os.path import relpath

from commands import add
from commands import init
from repository import Repository
from helper import delete_directory


class TestAdd:

    def setup(self):
        init.init_command()
        self.repository = Repository(Path.cwd())
        self.repository.init_required_paths()
        self.file = Path('file')
        self.file.touch()

    def teardown(self):
        delete_directory(Path(Path.cwd() / '.cvs'))
        self.file.unlink()

    def test_add_file(self):
        add.add_command(self.file.name)
        with open(self.repository.index) as index:
            indexed_file = index.readline().split()
        assert indexed_file[0] == self.file.name

    def test_add_files_in_directory(self):
        Path('directory').mkdir(parents=True, exist_ok=True)
        file1 = Path(Path.cwd() / 'directory' / 'file1')
        file2 = Path(Path.cwd() / 'directory' / 'file2')
        file1.touch()
        file2.touch()
        add.add_command('directory')
        with open(self.repository.index) as index:
            assert relpath(file1, Path.cwd()) == index.readline().split()[0]
            assert relpath(file2, Path.cwd()) == index.readline().split()[0]
        delete_directory(Path('directory'))

    def test_file_not_found(self, capfd):
        add.add_command('non_existing')
        out, err = capfd.readouterr()
        add_message = out.split('\n')[1]
        assert add_message == "File not found. Check path name"

    def test_add_modified_file(self):
        add.add_command(self.file.name)
        with open(self.file, 'w') as f:
            f.write('some text')
        add.add_command(self.file.name)
        modified_file_hash = add.calculate_hash(self.repository, self.file)
        with open(self.repository.index) as index:
            file_hash = index.readline().split()[1]
        assert file_hash == modified_file_hash

    # @pytest.mark.parametrize(("content", "expected"),
    #                          [("", "fef5d3bff5779d32d22f11c494250c4160063220"),
    #                           ("some_text",
    #                            "899a8f3e79b59c5bcb8c0267000f90efc6d05fe2")])
    # def test_calculate_hash(self, content, expected):
    #     with open(self.file, 'w') as f:
    #         f.write(content)
    #     assert expected == add.calculate_hash(self.repository, self.file)

