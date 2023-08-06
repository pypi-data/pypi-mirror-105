import click
import pydoni
import pydoni.opsys
from cli_reference.common import Verbose


@click.option('-r', '--root', type=click.Path(exists=True), required=True, multiple=True,
              help='Top-level directory to scan.')
@click.option('--recursive', is_flag=True, default=False,
              help='Scan `root` recursively and iterate down the directory tree.')
@click.option('--true-remove', is_flag=True, default=False,
              help='Delete directories that contain only empty directories.')
@click.option('--count-hidden-files/--no-count-hidden-files', is_flag=True, default=True,
              help='Count hidden files in evaluating whether directory is empty.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print messages to console.')

@click.command()
def delete_empty_subdirs(root, recursive, true_remove, count_hidden_files, verbose):
    """
    Scan a directory and delete any empty bottom-level directories.
    """
    args, result = pydoni.pydonicli_declare_args(locals()), dict()
    pydoni.pydonicli_register({'command_name': pydoni.what_is_my_name(with_modname=True), 'args': args})

    dirs = list(root)
    vb = Verbose(verbose)

    removed_dirs = []
    for root in dirs:
        removed = pydoni.opsys.delete_empty_dirs(root=root,
                                                 recursive=recursive,
                                                 true_remove=true_remove,
                                                 count_hidden_files=count_hidden_files)
        removed_dirs += removed

    if verbose:
        if len(removed_dirs):
            for dir in removed_dirs:
                vb.info('Removed: ' + dir)
        else:
            vb.info('No empty directories found', level='warn')

    result['removed_dirs'] = removed_dirs
    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})
