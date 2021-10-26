from pathlib import Path

from repository import Repository
from position_type import PositionType


def delete_directory(directory):
    for obj in directory.iterdir():
        if obj.is_dir():
            delete_directory(obj)
        else:
            obj.unlink()
    directory.rmdir()



