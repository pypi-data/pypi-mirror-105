import click
import os
import pydoni
import pydoni.sh
import pydoni.vb
from tqdm import tqdm
from colorama import Fore
from datetime import datetime
from cli_reference.common import Verbose


def find_directories(root, ignore, recursive):
    """
    Scan root directory (recursively) for git directories.
    """
    dnames = [root]

    if recursive:
        excl = ['.app', '.git', '.Rproj', '.archive', 'from-github']
        dnames = dnames + pydoni.listdirs(path=root, recursive=True, full_names=True)
        dnames = [x for x in dnames if not any([y in x for y in excl])]

    if ignore:
        dnames = [d for d in dnames if not any([d.startswith(ig) for ig in ignore])]

    return dnames


def scan_directories(dnames, verbose, color):
    """
    Scan directories to find out if each one contains a .git directory.
    """
    vb.info('Scanning {} total directories'.format(str(len(dnames))))

    if verbose:
        pbar = tqdm(dnames, unit='dir')
        if color:
            cmap = pydoni.extract_colorpalette('Greens', n=len(dnames), mode='ansi')
            current_color = None

    to_commit = []
    g = pydoni.sh.Git()
    for i, dname in enumerate(dnames):
        if verbose:
            if color:
                if current_color != cmap[i]:
                    pbar.bar_format = "{l_bar}%s{bar}%s{r_bar}" % (cmap[i], Fore.RESET)
                    current_color = cmap[i]

        if g.is_git_repo(dir=dname):
            if g.status(dir=dname) is False:
                to_commit.append(dname)

        if verbose:
            pbar.update(1)

    if verbose:
        pbar.close()

    return to_commit


def write_output(to_commit, outfile, root, recursive, verbose, color):
    """
    Print output to console or write to output file.
    """

    if outfile is None:
        vb.info('')
        vb.info('Requires commit:')
        for dname in to_commit:
            vb.info(dname, indent=1)

    else:
        assert isinstance(outfile, str)
        outfile = os.path.expanduser(outfile)

        with open(outfile, 'w') as f:
            indent = ' ' * 2

            f.write('Git Sync Program Log\n')
            f.write('{}Run at: {}\n'.format(indent, pydoni.systime()))
            f.write('{}Root dir: {}\n'.format(indent, root))
            f.write('{}Recursive: {}\n'.format(indent, str(recursive)))
            f.write('\nRequires commit:\n')

            for dname in to_commit:
                f.write(indent + dname + '\n')


@click.option('--root', type=click.Path(exists=True), required=True,
    help='Top-level directory to scan.')
@click.option('--outfile', type=click.Path(exists=False), default=None,
    help='Path to output file, if None then write to STDOUT.')
@click.option('--ignore', type=click.Path(exists=True), required=False, multiple=True,
    help='Directory paths to recursively ignore.')
@click.option('-r', '--recursive', is_flag=True, default=False,
    help='Scan `root` dir recursively for git directories.')
@click.option('-v', '--verbose', is_flag=True, default=False,
    help='Print messages to console.')
@click.option('-c', '--color', is_flag=True, default=False,
    help='Print colored progress bar. Requires that `verbose` is True.')

@click.command()
def git_sync(root, outfile, ignore, recursive, verbose, color):
    """
    Scan a directory for git repositories with outstanding changes.
    """
    pydoni.pydonicli_register({'command_name': pydoni.what_is_my_name(with_modname=True)})
    args = pydoni.pydonicli_declare_args(locals())
    result = dict(repositories_need_commit=None)

    os.chdir(root)

    global vb
    vb = Verbose(verbose, timestamp=True)

    ignore = list(ignore)
    dnames = find_directories(root, ignore, recursive)
    to_commit = scan_directories(dnames, verbose, color)

    if len(to_commit):
        write_output(to_commit, outfile, root, recursive, verbose, color)
    else:
        vb.info('No repositories need commit!')

    vb.info('')
    vb.program_complete('Git Sync complete!')

    result['repositories_need_commit'] = to_commit
    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['args', 'result']})
