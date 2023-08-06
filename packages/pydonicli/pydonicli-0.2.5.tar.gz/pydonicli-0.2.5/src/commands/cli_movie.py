import click
from commands.movie.refresh_imdb_table import refresh_imdb_table


@click.group(name='movie')
def cli_movie():
    """Doni movie-based CLI tools."""
    pass


cli_movie.add_command(refresh_imdb_table)
