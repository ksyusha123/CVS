from pathlib import Path


class Directory:
    def __init__(self, path):
        self.is_repository = False
        self.path = path
        self.cvs = Path()
