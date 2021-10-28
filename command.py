from pathlib import Path
from abc import ABCMeta, abstractmethod

from repository import Repository


class Command:
    __metaclass__ = ABCMeta

    def __init__(self, message_if_error="Init a repository"):
        repository = Repository(Path.cwd())
        if not self.check(repository):
            print(message_if_error)
            return

    @abstractmethod
    def execute(self, *args):
        pass

    def check(self, repository):
        return repository.is_initialised

    @staticmethod
    def get_repo():
        repository = Repository(Path.cwd())
        repository.init_required_paths()
        return repository
