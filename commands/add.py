import hashlib
from pathlib import Path
import click


class AddCommand:
    def __init__(self, file, repository):
        self.file = file
        self.repository = repository

    def add(self):
        if not self.repository.is_repository:
            print("Create a repository")
        else:
            hash = self._calculate_hash()
            self._create_blob(hash)
            self._add_to_index(hash)

    def _calculate_hash(self):
        with open(Path(self.repository.path/self.file)) as f:
            content = f.read()
            string_to_hash = f"blob {len(content)}\\0{content}"
            hash = hashlib.sha1(string_to_hash.encode()).hexdigest()
        return hash

    def _create_blob(self, hash):
        with open(Path(self.repository.objects/hash), 'wb') as obj, \
             open(Path(self.repository.path/self.file)) as f:
            for line in f:
                byte_string = f"{line}\n".encode()
                obj.write(byte_string)

    def _add_to_index(self, hash):
        is_indexed_old = False
        with open(self.repository.index) as index:
            index_read = index.read()
            filename_position_index = index_read.find(self.file)
            if filename_position_index != -1:
                is_indexed_old = True
                old_hash_position = \
                    filename_position_index + len(self.file) + 1
                index_read = index_read.replace(
                    index_read[old_hash_position:old_hash_position+40], hash)
        if is_indexed_old:
            with open(self.repository.index, 'w') as index:
                index.write(index_read)
        else:
            with open(self.repository.index, 'a') as index:
                index.write(f"{self.file} {hash}\n")
