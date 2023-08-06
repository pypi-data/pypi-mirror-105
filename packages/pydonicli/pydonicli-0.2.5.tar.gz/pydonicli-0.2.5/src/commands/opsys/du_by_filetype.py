import click
import pydoni
import pydoni.opsys
from cli_reference.common import Verbose


@click.option('-d', '--dpath', type=click.Path(exists=True), required=True,
              help='Full path to target directory.')
@click.option('-o', '--output-fpath', type=click.Path(), default=None,
              help='If specified, write program output to this file.')
@click.option('-r', '--recursive', is_flag=True, default=False,
              help='Scan recursively and iterate down the directory tree.')
@click.option('-h', '--human-readable', is_flag=True, default=False,
              help='Display filesize in output in human-readable format')
@click.option('-p', '--progress', is_flag=True, default=False,
              help='Display progress bar while scanning directory')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print messages to console.')

@click.command()
def du_by_filetype(dpath, output_fpath, recursive, human_readable, progress, verbose):
    """
    List the total filesize in a directory by file type.
    """
    args, result = pydoni.pydonicli_declare_args(locals()), dict()
    pydoni.pydonicli_register({'command_name': pydoni.what_is_my_name(with_modname=True), 'args': args})

    vb = Verbose(verbose)
    filesize_dct = pydoni.opsys.du_by_filetype(dpath=dpath,
                                               recursive=recursive,
                                               human_readable=human_readable,
                                               progress=progress,
                                               verbose=verbose)

    for ftype, fsize in filesize_dct.items():
        print(f'{ftype}: {fsize}')

    if isinstance(output_fpath, str):
        with open(output_fpath, 'a') as f:
            write_lst = []
            write_lst.append(f'Directory: "{dpath}"\n')

            for ftype, fsize in filesize_dct.items():
                write_lst.append(f'{ftype}: {fsize}\n')

            f.write(''.join(write_lst).strip())

    result['result'] = filesize_dct
    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})
