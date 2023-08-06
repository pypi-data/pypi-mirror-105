import click
import os
from gtts import gTTS
from datetime import datetime
from cli_reference.common import Verbose


@click.option('-t', '--text', type=str,
              help='Text string to convert to speech. If specified, must not specify --file.')
@click.option('-f', '--fpath', type=click.Path(exists=True), multiple=True,
              help='Path to M4A file(s) to convert to MP3.')
@click.option('-o', '--outfile', type=click.Path(), required=False, multiple=True, default=None,
              help='Desired path to output mp3 file(s). Must be either the same length as `file`, or None. If None, same file basename is used for each item in `file`.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print program messages to STDOUT.')
@click.option('-n', '--notify', is_flag=True, default=False,
              help='Fire macOS notification on program completion.')

@click.command()
def text_to_speech(text, fpath, outfile, verbose, notify):
    """
    Convert raw text, either as commandline input or file input, to speech using gTTS.
    """
    vb = Verbose(verbose)

    fpaths = list(fpath) if fpath is not None else []
    outfiles = list(outfile) if outfile is not None else []

    now_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    default_outfile = os.path.expanduser(os.path.join('~', 'Desktop', f'text_to_speech_commandline_output_{now_str}.mp3'))

    if text is not None:
        # --text
        if len(fpaths): raise Exception('Must pass either --text or --file, not both!')
        if len(outfiles) > 1: raise Exception('Passed --text but length of --outfile does not match!')

        output = gTTS(text=text, lang='en', slow=False)
        outfile_cl = os.path.expanduser(outfiles[0]) if len(outfiles) else default_outfile
        output.save(outfile_cl)
        vb.info(f'Audiofile saved {outfile_cl}')

    elif len(fpaths):
        # --fpath

        if len(fpaths) != len(outfiles):
            raise Exception('Passed --fpath but length of --outfile does not match!')

        for i, f in enumerate(fpaths):
            with open(f, 'r') as g:
                ftext = g.read().replace('\n', '')

            output = gTTS(text=ftext, lang='en', slow=False)
            outfile_f = os.path.expanduser(outfiles[i]) if len(outfiles) else default_outfile

            output.save(outfile_f)
            vb.info(f'Audiofile saved {outfile_f}')

    else:
        raise Exception('Must pass either --text or --file!')

    if notify:
        import pydoni.opsys
        pydoni.opsys.macos_notify(title='Text to Speech Complete')
