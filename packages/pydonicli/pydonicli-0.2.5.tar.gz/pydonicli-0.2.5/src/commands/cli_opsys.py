import click
from commands.opsys.delete_empty_subdirs import delete_empty_subdirs
from commands.opsys.du_by_filetype import du_by_filetype


@click.group(name='opsys')
def cli_opsys():
    """Doni opsys-based CLI tools."""
    pass


cli_opsys.add_command(delete_empty_subdirs)
cli_opsys.add_command(du_by_filetype)
