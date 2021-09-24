from pathlib import Path


class Directory:
    def __init__(self, path):
        self.is_repository = False
        self.path = path
        self.cvs = Path(path/'.cvs')
        self.objects = Path(self.cvs/'objects')
        self.index = Path(self.cvs/'index')
        self.head = Path(self.cvs/'HEAD')
