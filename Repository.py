from pathlib import Path


class Repository:
    def __init__(self, path):
        self.path = path
        self.cvs = Path()
        self.objects = Path()
        self.index = Path()
        self.head = Path()
        self.master = Path()
        self.refs = Path()
        self.heads = Path()

    @property
    def is_initialised(self):
        return Path(self.path / '.cvs').exists()

    def has_commits(self):
        return Path(self.master).exists()

    def init_required_paths(self):
        self.cvs = Path(self.path / '.cvs')
        self.objects = Path(self.cvs / 'objects')
        self.index = Path(self.cvs / 'index')
        self.head = Path(self.cvs / 'HEAD')
        self.refs = Path(self.cvs / 'refs')
        self.heads = Path(self.refs / 'heads')
        self.master = Path(self.heads / 'master')
        Path(self.cvs).mkdir(parents=True, exist_ok=True)
        Path(self.objects).mkdir(parents=True, exist_ok=True)
        Path(self.refs).mkdir(parents=True, exist_ok=True)
        Path(self.heads).mkdir(parents=True, exist_ok=True)

    def create_master(self):
        with open(self.master, 'w') as master:
            pass
