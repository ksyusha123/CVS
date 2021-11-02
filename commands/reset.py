from pathlib import Path
import click
import zlib
from multiprocessing import Pool

from command import Command
from position_type import PositionType


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
    ResetCommand().execute(commit, option)


class ResetCommand(Command):

    def execute(self, commit, option):
        repository = self.get_repo()
        if not repository.has_commits():
            click.echo("No commits yet")
            return
        commit = _get_commit_hash(repository, commit)
        if commit is None:
            click.echo("There is no such commit")
            return
        replace_head_with_branch(repository, commit)
        if option == 'mixed' or option == 'hard':
            update_index(repository, commit)
            if option == 'hard':
                update_working_directory(repository)


def replace_head_with_branch(repository, commit):
    with open(Path(repository.cvs / 'ORIG_HEAD'), 'w') as orig_head:
        orig_head.write(repository.current_commit)
    current_position = repository.current_position_with_type
    if current_position[1] == PositionType.branch:
        with open(Path(repository.cvs / current_position[0]), 'w') as current:
            current.write(commit)
    else:
        with open(repository.head, 'w') as head:
            head.write(commit)


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
            old_file = Path(repository.objects / hash)
            current_file = Path(repository.path / name)
            current_file.write_bytes(_decompress_file(repository, old_file))


def _decompress_file(repository, file):
    file_parts = _split_bytes_file(repository, file)
    with Pool() as pool:
        decompressed_file_parts = pool.map(_decompress_content, file_parts)
    return b''.join(decompressed_file_parts)


def _decompress_content(content):
    decompress_obj = zlib.decompressobj()
    decompressed_content = decompress_obj.decompress(content)
    return decompressed_content


def _split_bytes_file(repository, file):
    parts = []
    with open(Path(repository.path / file), 'rb') as f:
        content = f.read()
        split_content = content.split(b'--new-part--')
        parts += split_content
    return parts


def _get_commit_hash(repository, commit):
    if '~' in commit:
        return get_commit_from_end(repository, int(commit.split('~')[1]))
    if not Path(repository.objects / commit).exists():
        return None
    return commit


def get_commit_from_end(repository, number):
    current_commit = repository.current_commit
    for i in range(number):
        with open(Path(repository.objects / current_commit)) as commit:
            lines = commit.readlines()
            if len(lines) < 4:
                return None
            current_commit = lines[1].split()[1]
    return current_commit
