import click
from commands.image.ocr import ocr


@click.group(name='image')
def cli_image():
    """Doni image-based CLI tools."""
    pass


cli_image.add_command(ocr)
