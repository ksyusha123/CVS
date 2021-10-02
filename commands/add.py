import hashlib
from pathlib import Path
import click
from Repository import Repository


@click.command()
@click.argument('file')
def add(file):
    repository = Repository(Path.cwd())
    if not repository.is_initialised:
        click.echo("Init a repository first")
    else:
        repository.init_required_paths()
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
        for line in f:
            byte_string = f"{line}\n".encode()
            obj.write(byte_string)


def _add_to_index(hash, repository, file):
    is_indexed_old = False
    with open(repository.index) as index:
        index_read = index.read()
        filename_position_index = index_read.find(file)
        if filename_position_index != -1:
            is_indexed_old = True
            old_hash_position = \
                filename_position_index + len(file) + 1
            index_read = index_read.replace(
                index_read[old_hash_position:old_hash_position+40], hash)
    if is_indexed_old:
        with open(repository.index, 'w') as index:
            index.write(index_read)
    else:
        with open(repository.index, 'a') as index:
            index.write(f"{file} {hash}\n")
