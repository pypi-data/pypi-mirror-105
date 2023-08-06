import click
from commands.notes.add_events_log import add_events_log
from commands.notes.book_table_to_md import book_table_to_md
from commands.notes.ph_refresh import ph_refresh


@click.group(name='notes')
def cli_notes():
    """Doni notes-based CLI tools."""
    pass


cli_notes.add_command(add_events_log)
cli_notes.add_command(book_table_to_md)
cli_notes.add_command(ph_refresh)
