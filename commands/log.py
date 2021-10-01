from pathlib import Path
import click

from Repository import Repository


@click.command()
def log():
    repository = Repository(Path.cwd())
    if not repository.is_initialised:
        click.echo("Init a repository first")
    else:
        repository.init_paths()
        if not repository.head.exists():
            click.echo("No commits yet")
        else:
            with open(repository.head) as head:
                commit = head.readline()
                _print_commits_tree(commit, repository)


def _print_commits_tree(commit, repository):
    while True:
        with open(Path(repository.objects / commit)) as commit_obj:
            lines = commit_obj.readlines()
            print(f"{commit} {lines[-1]}")
            if len(lines) == 4:
                commit = lines[1].split()[1]
            else:
                break
