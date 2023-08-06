import click
from commands.audio.compress_file import compress_file
from commands.audio.join_files import join_files
from commands.audio.m4a_to_mp3 import m4a_to_mp3
from commands.audio.text_to_speech import text_to_speech


@click.group(name='audio')
def cli_audio():
    """Doni audio-based CLI tools."""
    pass

cli_audio.add_command(compress_file)
cli_audio.add_command(join_files)
cli_audio.add_command(m4a_to_mp3)
cli_audio.add_command(text_to_speech)
