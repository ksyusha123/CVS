import sys
import hashlib
from pathlib import Path
import click
import zlib
from os.path import relpath

from repository import Repository


@click.command(help="Indexes files")
@click.argument('obj_name')
def add(obj_name):
    repository = Repository(Path.cwd())
    if not repository.is_initialised:
        click.echo("Init a repository first")
        sys.exit()
    if not Path(repository.path / obj_name).exists():
        click.echo("File Not Found")
        sys.exit()
    repository.init_required_paths()
    _add(repository, obj_name)


def _add(repository, obj_name):
    if Path(obj_name).is_dir():
        _add_directory(repository, Path(obj_name))
    else:
        _add_file(repository, Path(obj_name))


def _add_directory(repository, directory):
    for obj in directory.iterdir():
        if obj.is_file():
            _add_file(repository, relpath(obj, repository.path))
        else:
            _add_directory(repository, obj)


def _add_file(repository, file):
    hash = _calculate_hash(repository, file)
    _create_blob(hash, repository, file)
    _add_to_index(hash, repository, file)


def _calculate_hash(repository, file):
    with open(Path(repository.path/file)) as f:
        content = f.read()
        string_to_hash = f"blob {len(content)}\\0{content}"
        hash = hashlib.sha1(string_to_hash.encode()).hexdigest()
    return hash


def _create_blob(hash, repository, file):
    with open(Path(repository.objects/hash), 'wb') as obj, \
         open(Path(repository.path/file)) as f:
        compressed_content = zlib.compress(f.read().encode())
        obj.write(compressed_content)


def _add_to_index(hash, repository, file):
    is_indexed_old = False
    with open(repository.index) as index:
        index_read = index.read()
        filename_position_index = index_read.find(str(file))
        if filename_position_index != -1:
            is_indexed_old = True
            old_hash_position = \
                filename_position_index + len(str(file)) + 1
            index_read = index_read.replace(
                index_read[old_hash_position:old_hash_position+40], hash)
    if is_indexed_old:
        with open(repository.index, 'w') as index:
            index.write(index_read)
    else:
        with open(repository.index, 'a') as index:
            index.write(f"{file} {hash}\n")
