from pathlib import Path

from position_type import PositionType


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
        return current_position

    @property
    def current_position_with_type(self):
        cur_pos = self.current_position
        return cur_pos.split('\\')[-1], self._get_type_of_position(cur_pos)

    @property
    def current_commit(self):
        position = self.current_position
        position_type = self._get_type_of_position(position)
        if (position_type == PositionType.branch or
                position_type == PositionType.tag):
            with open(Path(self.cvs / position)) as current_position:
                current_commit = current_position.readline()
        else:
            current_commit = position
        return current_commit

    @staticmethod
    def _get_type_of_position(position):
        if "heads" in position:
            return PositionType.branch
        if "tags" in position:
            return PositionType.tag
        else:
            return PositionType.commit
