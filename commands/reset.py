from pathlib import Path


class ResetCommand:
    def __init__(self, repository, commit):
        self.repository = repository
        self.commit = commit

    def reset(self):
        self._replace_head()
        self._update_index()
        self._update_working_directory()

    def _replace_head(self):
        with open(self.repository.head) as head:
            previous_commit = head.readline()
        with open(self.repository.head, 'w') as head:
            with open(Path(self.repository.cvs/'ORIG_HEAD'), 'w') as orig_head:
                orig_head.write(previous_commit)
                head.write(self.commit)

    def _update_index(self):
        old_commit_index = []
        with open(Path(self.repository.objects / self.commit)) as commit_obj:
            self._get_files(commit_obj.readline().split()[1], old_commit_index)
        with open(self.repository.index, 'w') as index:
            index.writelines(old_commit_index)

    def _get_files(self, tree, old_commit_index):
        with open(Path(self.repository.objects / tree)) as tree_file:
            for line in tree_file:
                obj_data = line.split()
                obj_type, hash = obj_data[0], obj_data[1]
                if obj_type == 'blob':
                    old_commit_index.append(line)
                else:
                    self._get_files(hash, old_commit_index)

    def _update_working_directory(self):
        with open(self.repository.index) as index:
            for indexed_file in index:
                file_data = indexed_file.split()
                type, hash, name = file_data[0], file_data[1], file_data[2]
                with open(Path(self.repository.path/name), 'w') as \
                        current_file:
                    with open(Path(self.repository.objects/hash)) as \
                            old_file:
                        current_file.writelines(old_file.readlines())
