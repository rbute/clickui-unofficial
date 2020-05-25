import os
import unittest

import click
import click.testing as ct

from clickui import make_ui

os.environ['CLICKUI'] = 'False'


@make_ui
@click.command('Sample Command')
@click.argument('sample_arg2')
@click.argument('sample_arg')
@click.option('--sample_option', '-s', '--samopts')
@click.option('-f', is_flag=True)
def sample_command(sample_arg, sample_arg2, sample_option, f):
    click.echo(f'sample_arg: {sample_arg}')
    click.echo(f'sample_arg2: {sample_arg2}')
    click.echo(f'sample_option: {sample_option}')
    click.echo(f'f: {f}')


class MyTestCase(unittest.TestCase):
    def test_something(self):
        runner = ct.CliRunner()
        res: ct.Result = runner.invoke(sample_command, ['world', 'oops', '--sample_option'])
        self.assertEqual(0, res.exit_code)


if __name__ == '__main__':
    unittest.main()
