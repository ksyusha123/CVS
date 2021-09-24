from commands.add import AddCommand
from commands.init import init
from commands.commit import CommitCommand
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
        elif command == 'commit':
            CommitCommand(directory, 's').commit()
        else:
            AddCommand(command.split()[1], directory).add()


if __name__ == '__main__':
    main('test')
