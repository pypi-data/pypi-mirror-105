import click
import os
import pydoni
import pydoni.sh
from cli_reference.common import Verbose


@click.option('-f', '--fpath', type=click.Path(exists=True), required=True, multiple=True,
              help='Path to M4A file(s) to convert to MP3.')
@click.option('-o', '--outfile', type=click.Path(), required=False, default=None,
              help='Desired path to output mp3 file(s). Must be either the same length as `file`, or None. If None, same file basename is used for each item in `file`.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print program messages to STDOUT.')
@click.option('-n', '--notify', is_flag=True, default=False,
              help='Fire macOS notification on program completion.')

@click.command()
def m4a_to_mp3(fpath, outfile, verbose, notify):
    """
    Convert .m4a file(s) to .mp3.
    """
    pydoni.pydonicli_register({'command_name': pydoni.what_is_my_name(with_modname=True), 'args': args})
    args, result = pydoni.pydonicli_declare_args(locals()), dict()
    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})

    vb = Verbose(verbose)

    fpaths = list(fpath)
    if outfile is None:
        outfiles = [os.path.splitext(f)[0] + '.mp3' for f in fpaths]
    else:
        outfiles = pydoni.ensurelist(outfile)

    assert len(fpaths) == len(outfiles)

    for fpath, outfile in zip(fpaths, outfiles):
        vb.info(f'Converting .m4a file "{fpath}" to .mp3: %s...')
        pydoni.sh.FFmpeg().compress(file, outfile=outfile)
        vb.info(f'Outputted .mp3 file "{outfile}"')

    if notify:
        pydoni.opsys.macos_notify(title='Audiofile Compression Complete!')

    result = {'fpaths': fpaths, 'outfiles': outfiles}
    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})
