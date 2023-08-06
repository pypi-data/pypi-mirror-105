import click
import os
import pydoni
import re
from .common import Extension, Convention, MediaFile
from pydoni.vb import echo
from tqdm import tqdm


def parse_media_type(file_ext, EXT):
    """
    Given a file extension, get the type of media
    One of 'photo', 'video' or 'remove'

    file_ext {str}: file extension to parse
    EXT {Extension}: Extension object
    type of media {str}
    """
    for attr_name in [x for x in dir(EXT) if not x.startswith('__')]:
        if file_ext in getattr(EXT, attr_name):
            return attr_name

    raise Exception(f'Invalid extension: {file_ext}')


@click.option('-f', '--fpath', required=True, type=click.Path(exists=True), multiple=True,
              help='Path or paths to file(s) to rename.')
@click.option('--initials', default='AKS', type=str,
              help='2 or 3 letter initials string.')
@click.option('--tz-adjust', default=0, type=int,
              help='Execute `pydoni.opsys.macos_notify()` on program completion.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print output to console.')
@click.option('-n', '--notify', is_flag=True, default=False,
              help='Fire macOS notification on program completion.')

@click.command()
def rename_mediafile(fpath, initials, tz_adjust, verbose, notify):
    """
    Rename a photo or video file according to a specified file naming convention.

    fpath {str} or {list}: filename or list of filenames to rename
    initials {str}: 2 or 3 letter initials string
    notify {bool}: execute `pydoni.opsys.macos_notify()` on program completion
    tz_adjust {int}: adjust file creation times by a set number of hours
    verbose {bool}: print messages and progress bar to console
    """
    args, result = pydoni.pydonicli_declare_args(locals()), dict()
    pydoni.pydonicli_register({'command_name': pydoni.what_is_my_name(with_modname=True), 'args': args})

    assert len(initials) in [2, 3], 'Parameter `initials` must be a string of length 2 or 3'

    logger = pydoni.logger_setup(pydoni.what_is_my_name(), pydoni.modloglev)
    logger.logvars(locals())

    mediafiles = list(fpath)
    assert isinstance(mediafiles, list), 'Variable `mediafiles` is not of type list'
    assert len(mediafiles), 'No mediafiles to rename!'
    assert isinstance(mediafiles[0], str), \
        f'First element of variable `mediafiles` is of type {type(mediafiles[0]).__name__}, expected string'

    CONV = Convention()
    EXT = Extension()

    mediafiles = [os.path.abspath(x) for x in mediafiles \
        if not re.match(CONV.photo, os.path.basename(x)) \
        and not re.match(CONV.video, os.path.basename(x))]

    msg = f'Renaming {len(mediafiles)} media files'
    logger.info(msg)
    if verbose:
        pydoni.vb.verbose_header(msg)
        pbar = tqdm(total=len(mediafiles), unit='mediafile')

    if not len(mediafiles):
        if verbose:
            echo('No files to rename!', fg='green')

    for mfile in mediafiles:
        if verbose:
            pbar.set_postfix(mediafile=pydoni.vb.stabilize_postfix(mfile, max_len=15))

        mf = MediaFile(mfile)
        newfname = mf.build_fname(initials=initials, tz_adjust=tz_adjust)
        newfname = os.path.join(os.path.dirname(mfile), os.path.basename(newfname))

        if os.path.basename(mfile) != os.path.basename(newfname):
            os.rename(mfile, newfname)
            result[os.path.basename(mfile)] = os.path.basename(newfname)
            if verbose:
                tqdm.write('{}: {} -> {}'.format(
                    click.style('Renamed', fg='green'),
                    os.path.basename(mfile),
                    os.path.basename(newfname)))
        else:
            result[os.path.basename(mfile)] = '<not renamed, new filename identical>'
            if verbose:
                tqdm.write('{}: {}'.format(
                    click.style('Not renamed', fg='red'),
                    os.path.basename(mfile)))

        if verbose:
            pbar.update(1)

    if verbose:
        pbar.close()
        echo(f'Renamed media files: {len(mediafiles)}', indent=2)

    if verbose or notify:
        pydoni.opsys.macos_notify(title='Mediafile Rename', message='Completed successfully!')

    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})
