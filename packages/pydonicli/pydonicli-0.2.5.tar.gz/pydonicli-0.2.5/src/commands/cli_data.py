import click
from commands.data.backup import backup
from commands.data.pg_dump import pg_dump
from commands.data.append_backup_log_table import append_backup_log_table


@click.group(name='data')
def cli_data():
    """Doni data-based CLI tools."""
    pass


cli_data.add_command(backup)
cli_data.add_command(pg_dump)
cli_data.add_command(append_backup_log_table)
