from pathlib import Path
import json


def init(directory):
    if not directory.is_repository:
        try:
            Path(directory.path/'.cvs').mkdir()
        except OSError:
            print("Can't create a repository")

        directory.is_repository = True

        with open(directory.head, 'w') as head:
            pass
        Path(directory.cvs/'objects').mkdir()
        with open(directory.index, 'w') as index:
            pass
    else:
        print("Repository exists")
