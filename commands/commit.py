import sys
import click
import os
import hashlib
from pathlib import Path
from checksumdir import dirhash

from repository import Repository


@click.command()
@click.option('-m', '--message', 'message',
              required=True, help='Commit message')
def commit(message):
    repository = Repository(Path.cwd())
    if not repository.is_initialised:
        click.echo("Init a repository first")
        sys.exit()
    repository.init_required_paths()
    repository_hash = dirhash(repository.path, 'sha1')
    _make_graph(repository.path, repository_hash, repository)
    commit_hash = _create_commit_object(
        repository_hash, repository, message)
    _direct_current_branch(commit_hash, repository)


def _make_graph(current_directory, current_dir_hash, repository):
    with open(Path(repository.objects / current_dir_hash), 'w')\
            as tree_file:
        for obj in current_directory.iterdir():
            if obj == repository.cvs:
                continue
            if obj.is_dir():
                obj_hash = dirhash(current_directory, 'sha1')
                _make_graph(obj, obj_hash, repository)
                tree_file.write(f"tree {obj_hash} {obj.name}\n")
            else:
                info_from_index = _get_info_from_index(obj, repository)
                if info_from_index:
                    tree_file.write(
                        f"blob {info_from_index[1]} "
                        f"{info_from_index[0]}\n")


def _get_info_from_index(file, repository):
    with open(repository.index) as index:
        for line in index:
            index_file_info = line.split()
            if file == Path(repository.path/index_file_info[0]):
                return index_file_info


def _create_commit_object(root_hash, repository, message):
    parent = _find_parent_commit(repository)
    with open(Path(repository.objects/'tmp'), 'w') as commit:
        commit.write(f"tree {root_hash}\n")
        if parent is not None:
            commit.write(f"parent {parent}\n")
        commit.write(f"\n{message}")
    commit_hash = _calculate_hash(Path(repository.objects/'tmp'))
    os.rename(Path(repository.objects/'tmp'),
              Path(repository.objects/commit_hash))
    return commit_hash


def _find_parent_commit(repository):
    parent = None
    if repository.has_commits():
        with open(repository.head) as head:
            current_branch = head.readline()
            with open(repository.cvs / current_branch) as current:
                current_commit = current.readline()
                if current_commit != "":
                    parent = current_commit
    return parent


def _calculate_hash(file_path):
    with open(file_path, 'rb') as binary_file:
        hash = hashlib.sha1(binary_file.read()).hexdigest()
    return hash


def _direct_current_branch(commit_hash, repository):
    if not repository.has_commits():
        repository.create_master()
    with open(repository.head) as head:
        current_branch = head.readline()
        with open(Path(repository.cvs / current_branch), 'w') as current:
            current.write(commit_hash)
