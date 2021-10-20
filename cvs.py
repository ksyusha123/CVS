import click
from commands import log
from commands import reset
from commands import init
from commands import add
from commands import commit
from commands import branch
from commands import checkout
from commands import tag


@click.group(help="Control version system")
def cvs():
    pass


cvs.add_command(log.log)
cvs.add_command(init.init)
cvs.add_command(add.add)
cvs.add_command(commit.commit)
cvs.add_command(reset.reset)
cvs.add_command(branch.branch)
cvs.add_command(checkout.checkout)
cvs.add_command(tag.tag)
