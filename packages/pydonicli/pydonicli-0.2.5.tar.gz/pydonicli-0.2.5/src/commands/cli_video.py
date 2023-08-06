import click
from commands.video.to_gif import to_gif


@click.group(name='video')
def cli_video():
    """Doni video-based CLI tools."""
    pass


cli_video.add_command(to_gif)
