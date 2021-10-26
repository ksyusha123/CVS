import sys
from pathlib import Path


from repository import Repository


class Command:
    def __init__(self):
        self.repository = Repository(Path.cwd())
        if not self.repository.is_initialised:
            sys.exit()
        self.repository.init_required_paths()
