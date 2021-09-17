import hashlib
import pickle
import os
from pathlib import Path
import click
import json


def add(file, directory):
    if not directory.is_repository:
        print("Create a repository")
    else:
        hash = _calculate_hash(file, directory)
        _create_blob(file, directory, hash)
        _add_to_index(file, hash, directory)


def _calculate_hash(file, directory):
    with open(Path(directory.path/file), 'rb') as binary_file:
        hash = hashlib.sha1(binary_file.read()).hexdigest()
    return hash


def _create_blob(file, directory, hash):
    with open(Path(directory.cvs/'objects'/hash), 'wb') as obj, \
         open(Path(directory.path/file)) as f:
        content = f.read()
        pickle.dump(f"blob {len(content)}\\0{content}", obj)


def _add_to_index(filename, hash, directory):
    is_indexed_old = False
    with open(Path(directory.cvs/'index')) as index:
        index_read = index.read()
        filename_position_index = index_read.find(filename)
        if filename_position_index != -1:
            is_indexed_old = True
            old_hash_position = filename_position_index + len(filename) + 1
            index_read = index_read.replace(index_read[
                               old_hash_position:old_hash_position+40], hash)
    if is_indexed_old:
        with open(Path(directory.cvs/'index'), 'w') as index:
            index.write(index_read)
    else:
        with open(Path(directory.cvs/'index'), 'a') as index:
            index.write(f"{filename} {hash}\n")
