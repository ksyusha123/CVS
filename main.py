from commands.add import AddCommand
from commands.init import init
from commands.commit import CommitCommand
from commands.log import LogCommand
from commands.reset import ResetCommand
from Repository import Repository

from pathlib import Path
import click


@click.command()
@click.argument('directory')
def main(directory):
    directory = Repository(Path(directory))
    if Path(directory.path/'.cvs').exists():
        directory.cvs = Path(directory.path/'.cvs')
        directory.is_repository = True
    while True:
        command = input().split()
        if command[0] == 'init':
            init(directory)
        elif command[0] == 'commit':
            CommitCommand(directory, command[1]).commit()
        elif command[0] == 'log':
            LogCommand(directory).log()
        elif command[0] == 'reset':
            ResetCommand(directory, command[1]).reset()
        else:
            AddCommand(command[1], directory).add()


if __name__ == '__main__':
    main('test')
