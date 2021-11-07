import click
import os
import hashlib
from pathlib import Path

from command import Command


@click.command(help="Commits changes")
@click.option('-m', '--message', 'message',
              required=True, help='Commit message')
def commit(message):
    CommitCommand().execute(message)


class CommitCommand(Command):

    def execute(self, message):
        repository = self.get_repo()
        if len(repository.files_ready_for_commit) == 0:
            click.echo("No files added")
            return
        root_hash = self._make_graph(repository.path, repository)
        commit_hash = self._create_commit_object(
            root_hash, repository, message)
        self._direct_current_branch(commit_hash, repository)

    def _make_graph(self, current_directory, repository):
        tree_file_content = ""
        for obj in current_directory.iterdir():
            if obj == repository.cvs:
                continue
            if obj.is_dir():
                obj_hash = self._make_graph(obj, repository)
                tree_file_content += f"tree {obj_hash} {obj.name}\n"
            else:
                info_from_index = self._get_info_from_index(obj, repository)
                if info_from_index:
                    tree_file_content += f"blob {info_from_index[1]} " \
                                         f"{info_from_index[0]}\n"
        graph_hash = hashlib.sha1(tree_file_content.encode()).hexdigest()
        with open(Path(repository.objects / graph_hash), 'w') as graph:
            graph.write(tree_file_content)
        return graph_hash


    @staticmethod
    def _get_info_from_index(file, repository):
        with open(repository.index) as index:
            for line in index:
                index_file_info = line.split()
                if file == Path(repository.path / index_file_info[0]):
                    return index_file_info

    def _create_commit_object(self, root_hash, repository, message):
        parent = self._find_parent_commit(repository)
        with open(Path(repository.objects / 'tmp'), 'w') as commit_obj:
            commit_obj.write(f"tree {root_hash}\n")
            if parent is not None:
                commit_obj.write(f"parent {parent}\n")
            commit_obj.write(f"\n{message}")
        commit_hash = self._calculate_hash(Path(repository.objects / 'tmp'))
        os.rename(Path(repository.objects / 'tmp'),
                  Path(repository.objects / commit_hash))
        return commit_hash

    @staticmethod
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

    @staticmethod
    def _calculate_hash(file_path):
        with open(file_path, 'rb') as binary_file:
            file_hash = hashlib.sha1(binary_file.read()).hexdigest()
        return file_hash

    @staticmethod
    def _direct_current_branch(commit_hash, repository):
        if not repository.has_commits():
            repository.create_master()
        with open(repository.head) as head:
            current_branch = head.readline()
            with open(Path(repository.cvs / current_branch), 'w') as current:
                current.write(commit_hash)


