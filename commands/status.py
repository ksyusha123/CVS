import click
from os.path import relpath
from pathlib import Path
from collections import deque

from commands.add import AddCommand
from command import Command


@click.command(help="Prints information about files in repository")
def status():
    StatusCommand().execute()


class StatusCommand(Command):

    def execute(self):
        repository = self.get_repo()
        click.echo()
        _print_current_position(repository)
        _print_untracked_files(repository)
        _print_files_ready_for_commit(repository)
        _print_modified_files(repository)


def bfs(root, get_children, get_values, must_be_in_answer, *args):
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


def _get_commit_tree(repository, commit):
    with open(Path(repository.objects / commit)) as commit_obj:
        tree = commit_obj.readline().split()[1]
    return tree


def _get_subtrees(repository, tree):
    subtrees = set()
    with open(Path(repository.objects / tree)) as tree_obj:
        for line in tree_obj:
            filetype, file_hash, name = line.split()
            if filetype == 'tree':
                subtrees.add(file_hash)
    return subtrees


def _get_blobs(repository, tree):
    blobs = set()
    with open(Path(repository.objects / tree)) as tree_obj:
        for line in tree_obj:
            filetype, file_hash, name = line.split()
            if filetype == 'blob':
                blobs.add((name, file_hash))
    return blobs


def _get_info_from_commit_tree(repository, tree):
    files_from_commit = bfs(tree, _get_subtrees, _get_blobs,
                            lambda *args: True, repository)
    return dict(files_from_commit)


def get_files_ready_for_commit(repository):
    if not repository.has_commits():
        return repository.indexed_files_info.keys()
    files_ready_for_commit = []
    indexed_files_info = repository.indexed_files_info
    tree = _get_commit_tree(repository, repository.current_commit)
    files_from_commit = _get_info_from_commit_tree(repository, tree)
    for indexed_file_info in indexed_files_info:
        if indexed_file_info in files_from_commit:
            if (indexed_files_info[indexed_file_info] !=
                    files_from_commit[indexed_file_info]):
                files_ready_for_commit.append(indexed_file_info)
        else:
            files_ready_for_commit.append(indexed_file_info)
    return files_ready_for_commit


def _print_current_position(repository):
    current_position, position_type = repository.current_position_with_type
    click.echo(f"On {position_type.name} {current_position}\n")


def _get_subdirectories(repository, directory):
    subdirectories = set()
    for obj in directory.iterdir():
        if obj.is_dir() and obj != repository.cvs:
            subdirectories.add(obj)
    return subdirectories


def _get_files(repository, directory):
    files = set()
    for obj in directory.iterdir():
        if obj.is_file():
            files.add(relpath(obj, repository.path))
    return files


def _is_untracked(repository, file):
    indexed_files = repository.indexed_files_info
    return file not in indexed_files


def _get_untracked_files(repository):
    untracked_files = bfs(repository.path, _get_subdirectories,
                          _get_files,
                          _is_untracked, repository)
    return untracked_files


def _is_tracked(repository, file):
    return not _is_untracked(repository, file)


def _get_modified_files(repository):
    modified_files = []
    working_directory_tracked_files = bfs(repository.path,
                                          _get_subdirectories,
                                          _get_files,
                                          _is_tracked, repository)
    indexed_files_info = repository.indexed_files_info
    for file in working_directory_tracked_files:
        file_hash = AddCommand.calculate_hash(repository, file)
        if file_hash != indexed_files_info[file]:
            modified_files.append(file)
    return modified_files


def _print_files(repository, get_files, message_if_no_files,
                 message):
    files = get_files(repository)
    if len(files) == 0:
        click.echo(message_if_no_files)
    else:
        click.echo(message)
        for file in files:
            click.echo(f"\t{file}")
    click.echo()


def _print_modified_files(repository):
    _print_files(repository, _get_modified_files,
                 "Working tree clean",
                 "Files not staged for commit:")


def _print_files_ready_for_commit(repository):
    _print_files(repository, get_files_ready_for_commit,
                 "Nothing to commit",
                 "Files ready for commit:")


def _print_untracked_files(repository):
    _print_files(repository, _get_untracked_files,
                 "No untracked files",
                 "Untracked files:")
