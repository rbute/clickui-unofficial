import os

import click

from clickui.const import CLICKUI_ENV
from clickui.core import CommandView
from distutils.util import strtobool

def make_ui(cmd: click.Command):
    CommandView(cmd)
    # do_mk_ui = bool(strtobool(os.getenv(CLICKUI_ENV, 'True')))
    # if do_mk_ui:
    #     return CmdGUI(cmd)
    # else:
    #     return cmd
