import click
import pydoni
import os
from cli_reference.common import Verbose


@click.option('-f', '--fpath', type=click.Path(exists=True), required=True, multiple=True,
              help='Video file(s) to convert to GIF.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print program messages to STDOUT.')
@click.option('-n', '--notify', is_flag=True, default=False,
              help='Fire macOS notification on program completion.')

@click.command()
def to_gif(fpath, verbose, notify):
    """
    Convert video file(s) to GIF.
    """
    args, result = pydoni.pydonicli_declare_args(locals()), dict()
    pydoni.pydonicli_register({'command_name': pydoni.what_is_my_name(with_modname=True), 'args': args})

    vb = Verbose(verbose)

    fpaths = list(fpath)
    for f in fpaths:
        vb.echo(f'Converting video file "{f}" to .gif...')
        pydoni.sh.FFmpeg().to_gif(f)
        if verbose:
            outfile = os.path.splitext(f)[0] + '.gif'
            vb.echo(f'Outputted .gif file "{outfile}"')

    if notify:
        pydoni.opsys.macos_notify(title='GIF Conversion Complete')

    result['videofile'] = f
    result['outfile'] = '<auto_generated>' if outfile is None else outfile

    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})
