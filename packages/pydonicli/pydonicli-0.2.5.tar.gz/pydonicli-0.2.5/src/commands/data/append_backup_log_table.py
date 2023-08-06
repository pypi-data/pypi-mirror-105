import click
import os
import pydoni
import pydoni.db
from datetime import datetime
from cli_reference.common import Verbose


@click.option('--table-schema', type=str, default='pydonicli',
              help='Postgres directory backup table schema name.')
@click.option('--table-name', type=str, default='directory_backup',
              help='Postgres directory backup table name.')
@click.option('--source', type=str,
              help='Source directory path.')
@click.option('--source-size-bytes', type=int, default=None,
              help='Size of source directory in bytes.')
@click.option('--target', type=str,
              help='Target directory path.')
@click.option('--target-size-before-bytes', default=None, type=int,
              help='Size of target directory before backup in bytes.')
@click.option('--target-size-after-bytes', default=None, type=int,
              help='Size of target directory after backup in bytes.')
@click.option('--start-ts', type=int, default=None,
              help='UNIX timestamp of backup start time.')
@click.option('--end-ts', type=int, default=None,
              help='UNIX timestamp of backup end time.')
@click.option('--is-completed', type=bool, default=True,
              help='Boolean flag to indicate whether backup was completed successfully.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print program messages to console.')

@click.command()
def append_backup_log_table(table_schema,
                            table_name,
                            source,
                            source_size_bytes,
                            target,
                            target_size_before_bytes,
                            target_size_after_bytes,
                            start_ts,
                            end_ts,
                            is_completed,
                            verbose):
    """
    Append a record to directory backup Postgres table. To be used if a backup is carried
    out without the use of the `doni data backup` command which handles the table insert
    automatically, but when the backup would still like to be logged in the log table.
    """
    pydoni.pydonicli_register({'command_name': pydoni.what_is_my_name(with_modname=True), 'args': args})
    args, result = pydoni.pydonicli_declare_args(locals()), dict()
    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})

    vb = Verbose(verbose)
    pg = pydoni.db.Postgres()

    sql_value_dct = {
        'source': source,
        'source_size_bytes': source_size_bytes,
        'target': target,
        'target_size_before_bytes': target_size_before_bytes,
        'target_size_after_bytes': target_size_after_bytes,
        'start_ts': datetime.fromtimestamp(start_ts),
        'end_ts': datetime.fromtimestamp(end_ts),
        'is_completed': is_completed,
    }

    vb.info(f'table_schema: {table_schema}')
    vb.info(f'table_name: {table_name}')
    for k, v in sql_value_dct.items():
        vb.info(f'{k}: {v}')

    insert_sql = pg.build_insert(
        schema=table_schema,
        table=table_name,
        columns=[k for k, v in sql_value_dct.items()],
        values=[v for k, v in sql_value_dct.items()]
    )

    pg.execute(insert_sql)

    vb.info(f'Appended record to {table_schema}.{table_name}')
    result['insert_sql'] = insert_sql

    vb.program_complete('Append to backup log table complete')
    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})
