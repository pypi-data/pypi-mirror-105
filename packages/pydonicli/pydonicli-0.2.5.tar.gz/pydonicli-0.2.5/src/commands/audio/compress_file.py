import click
import os
import pydoni
from cli_reference.common import Verbose


@click.option('-f', '--fpath', type=click.Path(exists=True), required=True, multiple=True,
              help='Path to audiofile(s) to compress.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print program messages to STDOUT.')
@click.option('-n', '--notify', is_flag=True, default=False,
              help='Fire macOS notification on program completion.')

@click.command()
def compress_file(fpath, verbose, notify):
    """
    Compress one or more audiofiles.
    """
    pydoni.pydonicli_register({'command_name': pydoni.what_is_my_name(with_modname=True), 'args': args})
    args, result = pydoni.pydonicli_declare_args(locals()), dict()
    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})

    vb = Verbose(verbose)

    fpaths = list(fpath)
    for fpath in fpaths:
        vb.info(f'Compressing file "{fpath}"...')
        pydoni.sh.FFmpeg().compress(fpath)
        vb.info('Successfully compressed file')

    if notify:
        pydoni.opsys.macos_notify(title='M4A to MP3 Conversion Complete!')

    result['compressed_files'] = fpaths
    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})
