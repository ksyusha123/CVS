import pytest
from pathlib import Path

from commands.init import InitCommand
from repository import Repository


def test_init():
    InitCommand().execute()
    repository = Repository(Path.cwd())
    assert repository.is_initialised


# @pytest.mark.xfail(raises=SystemExit)
# def test_not_create_cvs_if_initialised():
#     repository = Repository(Path.cwd())
#     init_command()
