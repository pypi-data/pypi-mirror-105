import atexit
import click
import logging
from datetime import datetime

import os
import sys
os.chdir(os.path.dirname(__file__))
sys.path.append(open(os.path.join('app_reference', 'pydoni_location.txt')).read())
import pydoni
from pydoni.db import Postgres


class NaturalOrderGroup(click.Group):
    """
    Control click command list order.
    Source: https://github.com/pallets/click/issues/513
    """
    def list_commands(self, ctx):
        return self.commands.keys()


def get_cl_commands():
    """
    Import all click commands under current directory as local variables.
    """
    from app import app
    from commands.cli_audio import cli_audio
    from commands.cli_data import cli_data
    from commands.cli_image import cli_image
    from commands.cli_imessage import cli_imessage
    from commands.cli_movie import cli_movie
    from commands.cli_notes import cli_notes
    from commands.cli_opsys import cli_opsys
    from commands.cli_photo import cli_photo
    from commands.cli_video import cli_video

    # Deactivated 2020-10-02 22:43:19
    # from commands.apple.make_meeting_entry import apple_make_meeting_entry

    # Retired until OMDB API key restored 2020-10-02 22:38:42
    # from commands.movie.refresh_movie_imdb_table import movie_refresh_imdb_table

    # Retired on 2020-10-10 23:01:03
    # from commands.photo.refresh_database import photo_refresh_database

    return locals()


def add_cl_commands(cl_commands):
    """
    Add them to `cli` variable. This will allow the `doni` commandline call
    visibility to all click commands housed under the current directory.
    """
    for cmd_name, cmd_obj in cl_commands.items():
        cli.add_command(cmd_obj)


def update_database_backend(schema_name, table_name, start_ts):
    """
    Update backend command run table. This table should be updated whenever a 'doni'
    command is run.
    """
    pg = Postgres()

    end_ts = datetime.utcnow()

    def get_pydoni_attr(attr_name):
        if hasattr(pydoni, attr_name):
            attr_value = getattr(pydoni, attr_name)
            return str(attr_value) if attr_value is not None else 'NULL'
        else:
            return 'NULL'

    e = get_pydoni_attr('pydonicli_e')
    args = get_pydoni_attr('pydonicli_args')
    result = get_pydoni_attr('pydonicli_result')
    command_name = get_pydoni_attr('pydonicli_command_name')

    elapsed_sec = datetime.timestamp(end_ts) - datetime.timestamp(start_ts)

    columns_values = [
        ('command_name', command_name),
        ('start_ts', start_ts),
        ('end_ts', end_ts),
        ('elapsed_sec', elapsed_sec),
        ('error_msg', e),
        ('args', args),
        ('result', result),
    ]

    if 'pg' in locals() or 'pg' in globals():
        pg.execute(pg.build_insert(schema=schema_name,
                                    table=table_name,
                                    columns=[col for col, val in columns_values],
                                    values=[val for col, val in columns_values],
                                    validate=True))
    else:
        pydoni_logger.warn(f'No connection to database backend established. No record inserted to {schema_name}.{table_name}')


@click.group(cls=NaturalOrderGroup)
@click.option('-v', '--verbose', count=True, help='Change logging level from WARN to INFO.')

def cli(verbose):
    """
    Command line interface to `pydoni` module.
    """
    global start_ts
    start_ts = datetime.utcnow()

    global pydoni_logger
    logging.basicConfig(level=logging.WARNING)
    pydoni_logger = logging.getLogger('pydoni')

    if verbose:
        pydoni_logger.setLevel(logging.INFO)
    else:
        pydoni_logger.setLevel(logging.WARN)


def main(args=None):
    add_cl_commands(get_cl_commands())
    try:
        cli()
    except Exception as e:
        error = e
        pydoni.pydonicli_e = str(error)

    atexit.register(update_database_backend, 'pydonicli', 'command_history', start_ts)

    if 'error' in locals():
        raise error
