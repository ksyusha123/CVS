from pathlib import Path


class LogCommand:
    def __init__(self, repository):
        self.repository = repository

    def log(self):
        if not self.repository.head.exists():
            print("No commits yet")
        else:
            with open(self.repository.head) as head:
                commit = head.readline()
                self._print_commits_tree(commit)

    def _print_commits_tree(self, commit):
        while True:
            with open(Path(self.repository.objects / commit)) as commit_obj:
                lines = commit_obj.readlines()
                print(f"{commit} {lines[-1]}")
                if len(lines) == 4:
                    commit = lines[1].split()[1]
                else:
                    break
