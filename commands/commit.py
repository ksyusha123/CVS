import click
import os
import hashlib
from pathlib import Path
from checksumdir import dirhash


class CommitCommand:
    def __init__(self, repository, message):
        self.repository = repository
        self.message = message

    def commit(self):
        repository_hash = dirhash(self.repository.path, 'sha1')
        self._make_graph(self.repository.path, repository_hash)
        commit_hash = self._create_commit_object(repository_hash)
        self._direct_head(commit_hash)
        # self._clear_index()

    def _make_graph(self, current_directory, current_dir_hash):
        with open(Path(self.repository.objects / current_dir_hash), 'w')\
                as tree_file:
            for obj in current_directory.iterdir():
                if obj == Path(current_directory/'.cvs'):
                    continue
                if obj.is_dir():
                    obj_hash = dirhash(current_directory, 'sha1')
                    self._make_graph(obj, obj_hash)
                    tree_file.write(f"tree {obj_hash} {obj.name}\n")
                else:
                    info_from_index = self._get_info_from_index(obj)
                    if info_from_index:
                        tree_file.write(
                            f"blob {info_from_index[1]} "
                            f"{info_from_index[0]}\n")

    def _get_info_from_index(self, file):
        with open(self.repository.index) as index:
            for line in index:
                index_file_info = line.split()
                if file == Path(self.repository.path/index_file_info[0]):
                    return index_file_info

    def _create_commit_object(self, root_hash):
        parent = self._find_parent_commit()
        with open(Path(self.repository.objects/'tmp'), 'w') as commit:
            commit.write(f"tree {root_hash}\n")
            if parent is not None:
                commit.write(f"parent {parent}\n")
            commit.write(f"{self.message}")
        commit_hash = self._calculate_hash(Path(self.repository.objects/'tmp'))
        os.rename(Path(self.repository.objects/'tmp'),
                  Path(self.repository.objects/commit_hash))
        return commit_hash

    def _find_parent_commit(self):
        parent = None
        if self.repository.head.exists():
            with open(self.repository.head) as head:
                parent = head.readline()
        return parent

    @staticmethod
    def _calculate_hash(file_path):
        with open(file_path, 'rb') as binary_file:
            hash = hashlib.sha1(binary_file.read()).hexdigest()
        return hash

    def _direct_head(self, commit_hash):
        with open(self.repository.head, 'w') as head:
            head.write(commit_hash)

    # def _clear_index(self):
    #     with open(self.repository.index, 'w') as index:
    #         pass
