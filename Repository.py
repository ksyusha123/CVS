from pathlib import Path


class Repository:
    def __init__(self, path):
        self.path = path
        self.cvs = Path()
        self.objects = Path()
        self.index = Path()
        self.head = Path()

    @property
    def is_initialised(self):
        return Path(self.path/'.cvs').exists()

    def init_paths(self):
        self.cvs = Path(self.path / '.cvs')
        self.objects = Path(self.cvs / 'objects')
        self.index = Path(self.cvs / 'index')
        self.head = Path(self.cvs / 'HEAD')

