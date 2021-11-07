from pathlib import Path
import click
from os.path import relpath


from command import Command
from file_manager import compress_file, calculate_hash


@click.command(help="Indexes files")
@click.argument('obj_name')
def add(obj_name):
    AddCommand().execute(obj_name)


class AddCommand(Command):

    def execute(self, obj_name):
        repository = self.get_repo()
        if not Path(repository.path / obj_name).exists():
            click.echo("File not found. Check path name")
            return
        self._add(repository, obj_name)

    def _add(self, repository, obj_name):
        if Path(obj_name).is_dir():
            self._add_directory(repository, Path(obj_name))
        else:
            self._add_file(repository, Path(obj_name))
        click.echo(f"Add {obj_name}")

    def _add_directory(self, repository, directory):
        if directory.name == '.cvs':
            return
        for obj in directory.iterdir():
            if obj.is_file():
                self._add_file(repository, relpath(obj, repository.path))
            else:
                self._add_directory(repository, obj)

    def _add_file(self, repository, file):
        file_hash = calculate_hash(repository, file)
        if not Path(repository.objects / file_hash).exists():
            self._create_blob(file_hash, repository, file)
        self._add_to_index(file_hash, repository, file)

    @staticmethod
    def _add_to_index(file_hash, repository, file):
        is_indexed_old = False
        with open(repository.index) as index:
            index_read = index.read()
            filename_position_index = index_read.find(str(file))
            if filename_position_index != -1:
                is_indexed_old = True
                old_hash_position = \
                    filename_position_index + len(str(file)) + 1
                index_read = index_read.replace(
                    index_read[old_hash_position:old_hash_position + 40],
                    file_hash)
        if is_indexed_old:
            with open(repository.index, 'w') as index:
                index.write(index_read)
        else:
            with open(repository.index, 'a') as index:
                index.write(f"{file} {file_hash}\n")

    @staticmethod
    def _create_blob(file_hash, repository, file):
        with open(Path(repository.objects / file_hash), 'wb') as obj:
            compressed_content = compress_file(repository, file)
            obj.write(compressed_content)
