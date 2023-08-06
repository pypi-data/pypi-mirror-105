import click
from commands.photo.instagram_hashtags import instagram_hashtags
from commands.photo.rename_mediafile import rename_mediafile
from commands.photo.split_batch_exported_timelapse import split_batch_exported_timelapse
from commands.photo.website_extract_image_titles import website_extract_image_titles
from commands.photo.workflow.workflow import workflow


@click.group(name='photo')
def cli_photo():
    """Doni photo-based CLI tools."""
    pass


cli_photo.add_command(instagram_hashtags)
cli_photo.add_command(rename_mediafile)
cli_photo.add_command(website_extract_image_titles)
cli_photo.add_command(workflow)
