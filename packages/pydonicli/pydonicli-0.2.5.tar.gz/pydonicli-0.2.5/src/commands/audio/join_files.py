import click
import os
import pydoni
import pydoni.audio
import pydoni.opsys
from cli_reference.common import Verbose

@click.option('-f', '--fpath', type=click.Path(exists=True), required=True, multiple=True,
              help='Path to audiofiles to concatenate.')
@click.option('-o', '--outfile', type=click.Path(), required=False, default=None,
              help='Desired path to output audiofile.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print program messages to STDOUT.')
@click.option('-n', '--notify', is_flag=True, default=False,
              help='Fire macOS notification on program completion.')

@click.command()
def join_files(fpath, outfile, verbose, notify):
    """
    Concatenate multiple audio files with FFmpeg.
    """
    pydoni.pydonicli_register({'command_name': pydoni.what_is_my_name(with_modname=True), 'args': args})
    args, result = pydoni.pydonicli_declare_args(locals()), dict()
    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})

    assert len(fpath) > 1, 'Must pass more than one file to join!'
    vb = Verbose(verbose)

    fpaths = pydoni.naturalsort(fpath)
    vb.info(f'Joining {len(fpaths)} audiofiles...')

    if outfile is None:
        outfile = pydoni.append_filename_suffix(fpaths[0], '-JOINED')

    pydoni.audio.join_audiofiles(audiofiles=fpaths, targetfile=outfile, method='ffmpeg')
    vb.info(f'Output audiofile created "{outfile}"')

    if notify:
        pydoni.opsys.macos_notify(title='Audiofile Join Complete!')

    outfile_size = os.stat(outfile).st_size
    result = {'joined_files': fpaths, 'outfile': outfile, 'outfile_size': outfile_size}
    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})
