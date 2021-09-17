from pathlib import Path
import json


def init(directory):
    if not directory.is_repository:
        try:
            Path(directory.path/'.cvs').mkdir()
        except OSError:
            print("Can't create a repository")

        directory.is_repository = True
        directory.cvs = Path(directory.path/'.cvs')

        Path(directory.cvs/'HEAD').mkdir()
        Path(directory.cvs/'objects').mkdir()
    else:
        print("Repository exists")
