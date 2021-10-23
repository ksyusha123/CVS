import click
import sys
from os.path import relpath
from pathlib import Path
from collections import deque
from enum import Enum

from repository import Repository
from commands.branch import get_current_position
from commands.add import calculate_hash


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
    _print_files_ready_for_commit(repository)
    _print_modified_files(repository)


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


def _print_files_ready_for_commit(repository):
    files_ready_for_commit = _get_files_ready_for_commit(repository)
    if len(files_ready_for_commit) == 0:
        click.echo("Nothing to commit")
    else:
        click.echo("Files ready for commit:")
        for file in files_ready_for_commit:
            click.echo(f"\t{file}")


def _print_modified_files(repository):
    modified_files = _get_modified_files(repository)
    if len(modified_files) == 0:
        click.echo("Working tree clean")
    else:
        click.echo("Files not staged for commit")
        for file in modified_files:
            click.echo(f"\t{file}")


def _get_untracked_files(repository):
    untracked_files = _bfs(repository.path, _get_subdirectories, _get_files,
                           _is_untracked, repository)
    return untracked_files


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
    indexed_files = _get_indexed_files_info(repository)
    return file not in indexed_files


def _get_files_ready_for_commit(repository):
    files_ready_for_commit = []
    indexed_files_info = _get_indexed_files_info(repository)
    tree = _get_commit_tree(repository, _get_current_commit(repository))
    files_from_commit = _get_info_from_commit_tree(repository, tree)
    for indexed_file_info in indexed_files_info:
        if indexed_file_info in files_from_commit:
            if (indexed_files_info[indexed_file_info] !=
                    files_from_commit[indexed_file_info]):
                files_ready_for_commit.append(indexed_file_info)
        else:
            files_ready_for_commit.append(indexed_file_info)
    return files_ready_for_commit


def _get_indexed_files_info(repository):
    with open(repository.index) as index:
        indexed_files_info = [tuple(line.split()) for line in index]
    return dict(indexed_files_info)


def _get_commit_tree(repository, commit):
    with open(Path(repository.objects / commit)) as commit_obj:
        tree = commit_obj.readline().split()[1]
    return tree


def _get_info_from_commit_tree(repository, tree):
    files_from_commit = _bfs(tree, _get_subtrees, _get_blobs,
                             lambda *args: True, repository)
    return dict(files_from_commit)


def _get_subtrees(repository, tree):
    subtrees = set()
    with open(Path(repository.objects / tree)) as tree_obj:
        for line in tree_obj:
            filetype, hash, name = line.split()
            if filetype == 'tree':
                subtrees.add(hash)
    return subtrees


def _get_blobs(repository, tree):
    blobs = set()
    with open(Path(repository.objects / tree)) as tree_obj:
        for line in tree_obj:
            filetype, hash, name = line.split()
            if filetype == 'blob':
                blobs.add((name, hash))
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


def _get_modified_files(repository):
    modified_files = []
    working_directory_tracked_files = _bfs(repository.path,
                                           _get_subdirectories, _get_files,
                                           _is_tracked, repository)
    indexed_files_info = _get_indexed_files_info(repository)
    for file in working_directory_tracked_files:
        hash = calculate_hash(repository, file)
        if hash != indexed_files_info[file]:
            modified_files.append(file)
    return modified_files


def _is_tracked(repository, file):
    return not _is_untracked(repository, file)


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

# status()
