import click
import sys
from os.path import relpath
from pathlib import Path
from collections import deque
from enum import Enum

from repository import Repository
from commands.branch import get_current_position


@click.command(help="Prints information about files in repository")
def status():
    repository = Repository(Path.cwd())
    # repository = Repository(Path("C:\\Users\\Пользователь\\OneDrive\\Рабочий "
    #                              "стол\\домашки\\CVS\\test"))
    if not repository.is_initialised:
        click.echo("Init a repository first")
        sys.exit()
    repository.init_required_paths()
    click.echo()
    _print_current_position(repository)
    _print_untracked_files(repository)


def _print_current_position(repository):
    current_position = get_current_position(repository)
    position_type = _get_type_of_position(current_position)
    if (position_type == PositionType.branch or
        position_type == PositionType.tag):
        position_name = current_position.split('\\')[-1]
        click.echo(f"On {position_type.name} {position_name}\n")
    else:
        click.echo(f"On commit {current_position.name}\n")


def _print_untracked_files(repository):
    untracked_files = _get_untracked_files(repository)
    if len(untracked_files) == 0:
        click.echo("Nothing added to commit")
    else:
        click.echo("Untracked files:")
        for file in untracked_files:
            click.echo(f"\t{file}")


def _get_untracked_files(repository):
    untracked_files = _bfs(repository.path, _get_subdirectories, _get_files,
                           _is_untracked, repository)
    return untracked_files
    # untracked_files = set()
    # queue = deque()
    # queue.append(repository.path)
    # while len(queue) != 0:
    #     current_directory = queue.popleft()
    #     subdirectories, files = \
    #         _get_subdirectories_and_files(repository, current_directory)
    #     for file in files:
    #         if _is_untracked(repository, file):
    #             untracked_files.add(file)
    #     for subdirectory in subdirectories:
    #         queue.append(subdirectory)
    # return untracked_files


def _get_subdirectories(repository, directory):
    subdirectories = set()
    for obj in directory.iterdir():
        if obj.is_dir():
            subdirectories.add(obj)
    subdirectories.remove(repository.cvs)
    return subdirectories


def _get_files(repository, directory):
    files = set()
    for obj in directory.iterdir():
        if obj.is_file():
            files.add(relpath(obj, repository.path))
    return files


def _is_untracked(repository, file):
    is_untracked = True
    indexed_files = _get_indexed_files(repository)
    if file in indexed_files:
        is_untracked = False
    return is_untracked


# def _get_files_ready_for_commit(repository):
#     indexed_files = _get_indexed_files(repository)
#     for file in indexed_files:



def _get_indexed_files(repository):
    with open(repository.index) as index:
        indexed_files = [line.split()[0] for line in index]
    return indexed_files


def _get_commit_tree(repository, commit):
    with open(Path(repository.objects / commit)) as commit_obj:
        tree = commit_obj.readline().split()[1]
    return tree


def _get_info_from_commit_tree(repository, tree):
    files_from_commit = _bfs(tree, _get_subtrees, _get_blobs, lambda x: True,
                             repository)
    return files_from_commit


def _get_subtrees(repository, tree):
    subtrees = set()
    with open(Path(repository.objects / tree)) as tree_obj:
        for line in tree_obj:
            filetype, hash = line.split()
            if filetype == 'tree':
                subtrees.add(hash)
    return subtrees


def _get_blobs(repository, tree):
    blobs = set()
    with open(Path(repository.objects / tree)) as tree_obj:
        for line in tree_obj:
            filetype, hash = line.split()
            if filetype == 'blob':
                blobs.add(hash)
    return blobs


def _get_current_commit(repository):
    with open(repository.head) as head:
        position = head.readline()
        position_type = _get_type_of_position(position)
        if (position_type == PositionType.branch or
                position_type == PositionType.tag):
            with open(Path(repository.cvs / position)) as current_position:
                current_commit = current_position.readline()
        else:
            current_commit = position
    return current_commit


def _get_type_of_position(position):
    if "heads" in position:
        return PositionType.branch
    if "tags" in position:
        return PositionType.tag
    else:
        return PositionType.commit


def _bfs(root, get_children, get_values, must_be_in_answer, *args):
    answer = set()
    queue = deque()
    queue.append(root)
    while len(queue) != 0:
        current = queue.popleft()
        children = get_children(*args, current)
        values = get_values(*args, current)
        for value in values:
            if must_be_in_answer(*args, value):
                answer.add(value)
        for child in children:
            queue.append(child)
    return answer


class PositionType(Enum):
    branch = 0,
    tag = 1,
    commit = 2
