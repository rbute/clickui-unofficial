import os

import click

from distutils.util import strtobool
from clickui.const import CLICKUI_ENV
from clickui.core import CommandView


def make_ui(cmd: click.Command):
    if strtobool(os.getenv(CLICKUI_ENV, True)):
        return CommandView(cmd)
    else:
        return cmd
