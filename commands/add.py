import sys
import hashlib
from pathlib import Path
import click
import zlib
from os.path import relpath
from os.path import getsize
from multiprocessing import Pool

from repository import Repository


@click.command(help="Indexes files")
@click.argument('obj_name')
def add(obj_name):
    add_command(obj_name)


def add_command(obj_name):
    repository = Repository(Path.cwd())
    if not repository.is_initialised:
        click.echo("Init a repository first")
        return
    if not Path(repository.path / obj_name).exists():
        click.echo("File not found. Check path name")
        return
    repository.init_required_paths()
    _add(repository, obj_name)


def _add(repository, obj_name):
    if Path(obj_name).is_dir():
        _add_directory(repository, Path(obj_name))
    else:
        _add_file(repository, Path(obj_name))


def _add_directory(repository, directory):
    if directory.name == '.cvs':
        return
    for obj in directory.iterdir():
        if obj.is_file():
            _add_file(repository, relpath(obj, repository.path))
        else:
            _add_directory(repository, obj)


def _add_file(repository, file):
    hash = calculate_hash(repository, file)
    if not Path(repository.objects / hash).exists():
        _create_blob(hash, repository, file)
    _add_to_index(hash, repository, file)


def calculate_hash(repository, file):
    content_size = getsize(file)
    string_to_hash = f"blob {content_size}\\0"
    sha1 = hashlib.sha1(string_to_hash.encode())
    with open(Path(repository.path/file), 'rb') as f:
        while True:
            content = f.read()
            if not content:
                break
            sha1.update(content)
        hash = sha1.hexdigest()
    return hash


def _create_blob(hash, repository, file):
    with open(Path(repository.objects/hash), 'wb') as obj:
        compressed_content = _compress_file(repository, file)
        obj.write(compressed_content)


def _compress_file(repository, file):
    file_parts = _split_file(repository, file)
    with Pool() as pool:
        compressed_file_parts = pool.map(_compress_content, file_parts)
    return b'--new-part--'.join(compressed_file_parts)


def _compress_content(content):
    compress_obj = zlib.compressobj(level=9)
    compressed_content = compress_obj.compress(content)
    return compressed_content


def _split_file(repository, file):
    parts = []
    with open(Path(repository.path / file), 'rb') as f:
        while True:
            content = f.read(1048576)
            if not content:
                break
            parts.append(content)
    return parts


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
