import sys
from pathlib import Path
import click
import zlib

from repository import Repository


@click.command(help='Replaces HEAD and current branch to given commit')
@click.option('--soft', 'option', is_flag=True, default=True,
              flag_value='soft',
              help='Is default option')
@click.option('--hard', 'option', is_flag=True,
              flag_value='hard',
              help='Updates index and working directory')
@click.option('--mixed', 'option', is_flag=True,
              flag_value='mixed',
              help='Updates index')
@click.argument('commit', required=True)
def reset(commit, option):
    repository = Repository(Path.cwd())
    if not repository.is_initialised:
        click.echo("Init a repository first")
        sys.exit()
    repository.init_required_paths()
    if not repository.has_commits():
        click.echo("No commits yet")
        sys.exit()
    _replace_current_branch(repository, commit)
    if option == 'mixed' or option == 'hard':
        update_index(repository, commit)
        if option == 'hard':
            update_working_directory(repository)


def _replace_current_branch(repository, commit):
    with open(repository.head) as head:
        current_branch = head.readline()
        with open(Path(repository.cvs / current_branch)) as current:
            previous_commit = current.readline()
            with open(Path(repository.cvs / 'ORIG_HEAD'), 'w') as orig_head:
                orig_head.write(previous_commit)
        with open(Path(repository.cvs / current_branch), 'w') as current:
            current.write(commit)


def update_index(repository, commit):
    old_commit_index = []
    with open(Path(repository.objects / commit)) as commit_obj:
        _get_files(
            commit_obj.readline().split()[1], old_commit_index, repository)
    with open(repository.index, 'w') as index:
        index.writelines(old_commit_index)


def _get_files(tree, old_commit_index, repository):
    with open(Path(repository.objects / tree)) as tree_file:
        for line in tree_file:
            obj_data = line.split()
            obj_type, hash, name = obj_data[0], obj_data[1], obj_data[2]
            if obj_type == 'blob':
                old_commit_index.append(f"{name} {hash}\n")
            else:
                _get_files(hash, old_commit_index, repository)


def update_working_directory(repository):
    with open(repository.index) as index:
        for indexed_file in index:
            file_data = indexed_file.split()
            name, hash = file_data[0], file_data[1]
            with open(Path(repository.path/name), 'w') as current_file:
                with open(Path(repository.objects/hash), 'rb') as old_file:
                    current_file.write(
                        zlib.decompress(old_file.read()).decode())
