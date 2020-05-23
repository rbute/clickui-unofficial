import click

from clickui.core import CommandView


def make_ui(cmd: click.Command):
    CommandView(cmd)
