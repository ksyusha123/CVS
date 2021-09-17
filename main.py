from commands.add import add
from commands.init import init
from Directory import Directory

from pathlib import Path
import click


# @click.command()
# @click.argument('directory')
def main(directory):
    directory = Directory(Path(directory))
    if Path(directory.path/'.cvs').exists():
        directory.cvs = Path(directory.path/'.cvs')
        directory.is_repository = True
    while True:
        command = input()
        if command == 'init':
            init(directory)
        else:
            add(command.split()[1], directory)


if __name__ == '__main__':
    main('test')
