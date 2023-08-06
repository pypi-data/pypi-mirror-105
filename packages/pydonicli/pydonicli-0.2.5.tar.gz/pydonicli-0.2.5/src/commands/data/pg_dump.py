import click
import os
import pydoni
import pydoni.db
import pydoni.vb
import termtables as tt
from datetime import datetime
from cli_reference.common import Verbose


@click.option('--backup-dir', type=click.Path(exists=True), required=True,
              help='Path to directory to save database dump to.')
@click.option('--pg-dbname', type=str, default=None,
              help='Name of local Postgres database to dump.')
@click.option('--pg-user', type=str, default=None,
              help='Username for local Postgres')
@click.option('--sep', type=str, default='\x08',
              help='Separator for local CSV dump. Requires that `csvdump` is True.')
@click.option('--pgdump', is_flag=True, default=False,
              help='Dump database using `pgdump` utility.')
@click.option('--csvdump', is_flag=True, default=False,
              help='Dump database as CSV files.')
@click.option('--max-dir-size', type=float, default=None, required=False,
              help='Maximum backup directory size in GB. If specified, after the dump is complete, then check if the total directory size of `backup_dir` is above this limit. If so, begin by removing the oldest backups and re-checking until the size is under the specified GB limit.')
@click.option('--dry-run', is_flag=True, default=False,
              help='Do not execute dump but still run through program.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print messages to console.')

@click.command()
def pg_dump(backup_dir, pg_dbname, pg_user, sep, pgdump, csvdump, max_dir_size, dry_run, verbose):
    """
    Dump a local Postgres database. Looks for ~/.pgpass by default.
    """
    args, result = pydoni.pydonicli_declare_args(locals()), dict()
    pydoni.pydonicli_register({'command_name': pydoni.what_is_my_name(with_modname=True), 'args': args})

    global vb
    vb = Verbose(verbose)

    if dry_run:
        vb.info('DRY RUN: Not executing any code', level='warn')

    # Either `pgdump` or `csvdump` must be true
    assert pgdump is True or csvdump is True

    pg = pydoni.db.Postgres(pg_user=pg_user, pg_dbname=pg_dbname)

    # Define subfolder to dump files to within dump directory
    subdir = pydoni.systime(stripchars=True) + '_' + pg.dbname
    backup_subdir = os.path.join(backup_dir, subdir)
    os.mkdir(backup_subdir)

    vb.info('Database: ' + pg.dbname)
    vb.info('Destination folder: ' + backup_subdir)

    # Dump database based on user's preference
    # May dump using pg_dump, export tables to CSV, or both

    dumped_files = []

    if pgdump:
        vb.info('Executing `pg_dump`')
        if not dry_run:
            dumped_dbfile = pg.dump(backup_dir=backup_subdir)
            dumped_files += [dumped_dbfile]

    if csvdump:
        # Dump each file to textfile
        vb.info('Executing CSV dump to tables')
        if not dry_run:
            dumped_csvfiles = pg.dump_tables(backup_dir=backup_subdir, sep=sep, coerce_csv=False)
            dumped_files += dumped_csvfiles

    result['backup_directory'] = backup_subdir
    result['dumped_files'] = {}
    for f in dumped_files:
        result['dumped_files'][os.path.basename(f)] = dict(
            filesize=os.stat(f).st_size,
            filesize_readable=pydoni.human_filesize(os.stat(f).st_size),
            created=datetime.fromtimestamp(os.path.getctime(f)).strftime('%Y-%m-%d %H:%M:%S.%f'),
            rows=pydoni.file_len(f))

    if verbose:
        vb.line_break()
        tt_list = [[os.path.basename(file),
                    infodict['created'],
                    pydoni.human_filesize(infodict['filesize']),
                    str(infodict['rows'])
                   ] for file, infodict in result['dumped_files'].items()]

        if len(tt_list):
            if verbose:
                print(tt.to_string(
                    tt_list,
                    header=[click.style(x, bold=True) for x in ['File', 'Created', 'Size', 'Rows']],
                    style=tt.styles.ascii_thin_double,
                    padding=(0, 1),
                    alignment='ccrr'))
        else:
            vb.info('No database files were dumped!', level='warn')

    if dry_run:
        os.rmdir(backup_subdir)

    max_dir_size_enforced = False
    removed_old_backup_dirs = []
    if max_dir_size:
        # Check size of `backup_dir` and clear any backup directories until the total size
        # is less than max_dir_size (upper GB limit)
        from collections import OrderedDict
        from shutil import rmtree
        from pathlib import Path

        subdirs = sorted([x for x in Path(backup_dir).iterdir() if os.path.isdir(x)], key=os.path.getmtime)
        subdirs_size = zip(subdirs, [pydoni.dirsize(x) / 1000000000 for x in subdirs])
        total_size = sum([y for x, y in subdirs_size])

        if total_size > max_dir_size:
            vb.info('Enforcing maximum directory size: %s GB' % str(max_dir_size), level='warn')
            max_dir_size_enforced = True

        while total_size > max_dir_size:
            dir_to_remove = str(subdirs[0])
            rmtree(dir_to_remove)
            removed_old_backup_dirs.append(dir_to_remove)

            subdirs = sorted([x for x in Path(backup_dir).iterdir() if os.path.isdir(x)], key=os.path.getmtime)

            subdirs_size = zip(subdirs, [pydoni.dirsize(x) / 1000000000 for x in subdirs])
            total_size = sum([y for x, y in subdirs_size])

            vb.info('Removed: ' + os.path.basename(dir_to_remove), level='warn')

    vb.program_complete('Postgres dump complete!')

    result['max_dir_size_enforced'] = max_dir_size_enforced
    result['removed_old_backup_dirs'] = [os.path.basename(x) for x in removed_old_backup_dirs]
    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})
