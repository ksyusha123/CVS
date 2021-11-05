from pathlib import Path

from position_type import PositionType
from position import Position


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
        self.tags = Path()

    @property
    def is_initialised(self):
        return Path(self.path / '.cvs').exists()

    @property
    def branches(self):
        branches = set()
        for branch in self.heads.iterdir():
            branches.add(branch.name)
        return branches

    @property
    def all_tags(self):
        tags = set()
        for tag in self.tags.iterdir():
            tags.add(tag.name)
        return tags

    def has_commits(self):
        return Path(self.master).exists()

    def init_required_paths(self):
        self.cvs = Path(self.path / '.cvs')
        self.objects = Path(self.cvs / 'objects')
        self.index = Path(self.cvs / 'index')
        self.head = Path(self.cvs / 'HEAD')
        self.refs = Path(self.cvs / 'refs')
        self.tags = Path(self.refs / 'tags')
        self.heads = Path(self.refs / 'heads')
        self.master = Path(self.heads / 'master')
        Path(self.cvs).mkdir(parents=True, exist_ok=True)
        Path(self.objects).mkdir(parents=True, exist_ok=True)
        Path(self.refs).mkdir(parents=True, exist_ok=True)
        Path(self.heads).mkdir(parents=True, exist_ok=True)
        Path(self.tags).mkdir(parents=True, exist_ok=True)

    def create_master(self):
        self.master.touch()

    @property
    def current_position(self):
        with open(self.head) as head:
            current_position = head.readline()
        return Position(current_position)

    @property
    def current_commit(self):
        position = self.current_position
        if (position.type == PositionType.branch or
                position.type == PositionType.tag):
            with open(Path(self.cvs / position.path)) as current_position:
                current_commit = current_position.readline()
        else:
            current_commit = position.path
        return current_commit

    @property
    def indexed_files_info(self):
        indexed_files_info = {}
        with open(self.index) as index:
            for line in index:
                indexed_data = line.split()
                indexed_files_info[indexed_data[0]] = indexed_data[1]
        return indexed_files_info

    def get_commit_hash_of(self, commit):
        if '~' in commit:
            return self._get_commit_from_end(self, int(commit.split('~')[1]))
        if not Path(self.objects / commit).exists():
            return None
        return commit

    @staticmethod
    def _get_commit_from_end(repository, number):
        current_commit = repository.current_commit
        for i in range(number):
            with open(Path(repository.objects / current_commit)) as commit:
                lines = commit.readlines()
                if len(lines) < 4:
                    return None
                current_commit = lines[1].split()[1]
        return current_commit
