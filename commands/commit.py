from pathlib import Path
import click
from checksumdir import dirhash


class CommitCommand:
    def __init__(self, repository, message):
        self.repository = repository
        self.message = message

    def commit(self):
        repository_hash = dirhash(self.repository.path, 'sha1')
        self._make_graph(self.repository.path, repository_hash)

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
                if file.name == index_file_info[0]:
                    return index_file_info
