import click
import os
import pydoni
import pydoni.image
from cli_reference.common import Verbose


@click.option('-f', '--fpath', type=click.Path(exists=True), required=True, multiple=True,
              help='Path to audiofile(s) to compress.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print messages to console.')

@click.command()
def ocr(fpath, verbose):
    """
    OCR an image using pytesseract.
    """
    pydoni.pydonicli_register({'command_name': pydoni.what_is_my_name(with_modname=True), 'args': args})
    args, result = pydoni.pydonicli_declare_args(locals()), dict()
    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})

    vb = Verbose(verbose)

    fpaths = list(fpath)
    for fpath in fpaths:
        vb.info(f'Applying OCR to file "{fpath}"...')
        text = pydoni.image.ocr_image(fpath)

        with open(os.path.splitext(fpath)[0] + '.txt', 'w') as f:
            f.write(text)

        vb.info("Successfully OCR'd file")

    result['ocr_files'] = fpaths
    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})
