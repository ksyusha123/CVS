from pathlib import Path
import click
import zlib

from Repository import Repository


@click.command()
@click.argument('commit', required=True)
def reset(commit):
    repository = Repository(Path.cwd())
    if not repository.is_initialised:
        click.echo("Init a repository first")
    else:
        repository.init_required_paths()
        if not repository.has_commits():
            click.echo("No commits yet")
        else:
            repository.init_head()
            _replace_head(repository, commit)
            _update_index(repository, commit)
            _update_working_directory(repository)


def _replace_head(repository, commit):
    with open(repository.head) as head:
        previous_commit = head.readline()
    with open(repository.head, 'w') as head:
        with open(Path(repository.cvs/'ORIG_HEAD'), 'w') as orig_head:
            orig_head.write(previous_commit)
            head.write(commit)


def _update_index(repository, commit):
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
            obj_type, hash = obj_data[0], obj_data[1]
            if obj_type == 'blob':
                old_commit_index.append(line)
            else:
                _get_files(hash, old_commit_index, repository)


def _update_working_directory(repository):
    with open(repository.index) as index:
        for indexed_file in index:
            file_data = indexed_file.split()
            type, hash, name = file_data[0], file_data[1], file_data[2]
            with open(Path(repository.path/name), 'w') as current_file:
                with open(Path(repository.objects/hash), 'rb') as old_file:
                    current_file.write(
                        zlib.decompress(old_file.read()).decode())
