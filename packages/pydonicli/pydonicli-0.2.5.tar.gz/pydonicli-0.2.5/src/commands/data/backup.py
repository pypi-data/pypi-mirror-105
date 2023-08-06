import click
import pydoni
import shutil
import time
import subprocess
from cli_reference.common import Verbose
from datetime import datetime
from os import makedirs
from os.path import basename, isfile, isdir, dirname, getmtime
from send2trash import send2trash


ignore_files = [
    'The Office S09E16 Moving On.mkv',
    'The Office S09E20 Paper Airplanes.mkv',
]


def is_file_changed(sourcefile, targetfile):
    """
    Detect whether a target file has been changed from its corresponding source file
    by determining whether the source and target file change datetimes are different
    by more than a threshold value (i.e. 1%).
    """

    def pct_change(num1, num2):
        """
        Return the pecentage change from `num1` -> `num2` on a scale from 0-100.
        """
        return abs(100.0 * (num2*1.0 - num1*1.0) / num1*1.0)

    mtime_source = getmtime(sourcefile)
    mtime_target = getmtime(targetfile)

    return pct_change(mtime_source, mtime_target) > 1.0


@click.option('--source', type=click.Path(exists=True), required=True,
              help='Absolute path to source directory.')
@click.option('--target', type=click.Path(exists=True), required=True,
              help='Absolute path to target directory.')
@click.option('--update-log-table', is_flag=True, default=False,
              help='Add an entry to Postgres table pydonicli.directory_backup')
@click.option('--use-rsync', is_flag=True, default=False,
              help='Use the `rsync` executable instead of python to back up source to target.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print messages to console.')
@click.option('--debug', is_flag=True, default=False,
              help='Print debug messages to console.')
@click.option('--dry-run', is_flag=True, default=False,
              help='Do not execute copy, replace or delete on any files.')

@click.command()
def backup(source, target, update_log_table, use_rsync, verbose, debug, dry_run):
    """
    Back up a source directory to a target directory.

    Author: Andoni Sooklaris
    Date: 2019-01-29
    Updated:
        - 2019-10-10
        - 2020-03-18
        - 2020-05-10
        - 2020-10-11: Integrated with PG table pydoni.directory_backup
        - YYYY-MM-DD: Simplified code logic substantially

    This function will accept a source and target directories, most often
    on separate external hard drives, and copy all files from the source
    to the target that are either:

        (1) Not in the target directory
        (2) Are in the target directory, but have been updated

    Files in the target that have been deleted in the source will also
    be deleted.
    """
    args, result = pydoni.pydonicli_declare_args(locals()), dict()
    pydoni.pydonicli_register({'command_name': pydoni.what_is_my_name(with_modname=True), 'args': args})

    start_ts = time.time()

    vb = Verbose(verbose)
    ws = '  '

    if update_log_table:
        from pydoni import dirsize
        from pydoni.db import Postgres

        vb.debug('Attempting to initialize directory backup record in Postgres log table')

        start_ts_utc = datetime.utcnow()
        pg = Postgres()
        directory_backup_table_schema = 'pydonicli'
        directory_backup_table_name = 'directory_backup'

        insert_dict = {
            'source': source,
            'source_size_bytes': dirsize(source),
            'target': target,
            'target_size_before_bytes': dirsize(target),
            'target_size_after_bytes': None,
            'start_ts': start_ts_utc,
            'is_completed': False
        }

        insert_sql = pg.build_insert(schema=directory_backup_table_schema,
                                     table=directory_backup_table_name,
                                     columns=list(insert_dict.keys()),
                                     values=list(insert_dict.values()),
                                     validate=True)
        if not dry_run:
            pg.execute(insert_sql)

        directory_backup_id = pg.read_sql(f"""
        select directory_backup_id
        from {directory_backup_table_schema}.{directory_backup_table_name}
        order by gen_ts desc
        limit 1""").squeeze()

        vb.debug(f'{ws}Successful. Directory Backup ID: {directory_backup_id}')


    assert source != target, 'Source and target directories must be different'
    if basename(source) != basename(target):
        if not click.confirm('Source and target directory basenames are not the same. Are you sure you would like to proceed?'):
            exit()

    if use_rsync:
        cmd_lst = ['rsync', '--delete-before', '-a', '-h', '-u']
        if verbose:
            cmd_lst = cmd_lst + ['-v', '--progress']

        cmd_lst = cmd_lst + [f'"{source}"'] + [f'"{target}"']
        cmd = ' '.join(cmd_lst)

        subprocess.call(cmd, shell=True)

        # progress_flag = ' --progress' if verbose else ''
        # backup_cmd = f'rsync -avhu{progress_flag} --delete-before "{source}" "{target}"'
        # subprocess.call(backup_cmd, shell=True)

    else:
        vb.info(f'Listing files at source: {source}')
        files_source = pydoni.listfiles(path=source, recursive=True, full_names=True)
        vb.debug('Found files at source: ' + str(len(files_source)))
        files_source = [x for x in files_source if x not in ignore_files]
        vb.debug(f'Found files at source after filtering out manually ignored files: {len(files_source)}')

        vb.info(f'Listing files at target: {target}')
        files_target = pydoni.listfiles(path=target, recursive=True, full_names=True)
        vb.debug('Found files at target: ' + str(len(files_target)))
        files_target = [x for x in files_target if x not in ignore_files]
        vb.debug(f'Found files at target after filtering out manually ignored files: {len(files_target)}')

        # Scan source files and for each determine whether to do nothing, copy to target,
        # or replace at target
        copied_files = []
        replaced_files = []
        vb.info('Scanning for new, updated or deleted files at source')
        vb.pbar_init(total=len(files_source), unit='file')

        for sourcefile in files_source:
            vb.pbar_write(f'Sourcefile: {sourcefile}', refer_debug=True)
            vb.pbar.set_postfix({'file': basename(sourcefile)})

            targetfile = sourcefile.replace(source, target)
            vb.pbar_write(f'{ws}Expected mirrored targetfile: {targetfile}', refer_debug=True)

            if not isfile(targetfile):
                # Copy file to target. Create parent directory at target if not exists
                vb.pbar_write(f'{ws}(Copy) attempting to copy file "{sourcefile}" to "{targetfile}"', refer_debug=True)

                targetdpath = dirname(targetfile)
                if not isdir(targetdpath):
                    vb.pbar_write(f'{ws}{ws}Parent directory of targetfile does not exist, creating it at: ' + targetdpath, refer_debug=True)
                    if not dry_run:
                        makedirs(targetdpath)

                    vb.pbar_write(f'{ws}{ws}Successful', refer_debug=True)

                if not dry_run:
                    shutil.copy2(sourcefile, targetfile)

                vb.pbar_write(f'{ws}Successful', refer_debug=True)
                copied_files.append(sourcefile)

            elif isfile(targetfile) and is_file_changed(sourcefile, targetfile):
                # Replace file at target (same action as copy, but parent directory must exist)
                vb.pbar_write(f'(Replace) attempting to copy file "{sourcefile}" to "{targetfile}"', refer_debug=True)
                if not dry_run:
                    shutil.copy2(sourcefile, targetfile)

                vb.pbar_write(f'Successful', refer_debug=True)
                replaced_files.append(sourcefile)

            else:
                vb.pbar_write(f'{ws}Targetfile already exists and is unchanged', refer_debug=True)

            vb.pbar_update(1)

        vb.pbar_close()

        # Scam target files and for each determine whether that file has been since
        # deleted from source
        deleted_files = []
        vb.info('Scanning for files at target since deleted from source')
        vb.pbar_init(total=len(files_target))
        for targetfile in files_target:
            sourcefile = targetfile.replace(target, source)
            vb.pbar.set_postfix({'file': basename(targetfile)})

            if not isfile(sourcefile) and not isdir(sourcefile):
                vb.pbar_write(f'(Delete) attempting to delete "{targetfile}"', refer_debug=True)
                if not dry_run:
                    send2trash(targetfile)

                vb.pbar_write(f'{ws}Successful', refer_debug=True)
                deleted_files.append(targetfile)

            vb.pbar_update(1)

        vb.pbar_close()

        # Record number of files copied, replaced and deleted
        vb.info(f'Copied {len(copied_files)} files')
        vb.info(f'Replaced {len(replaced_files)} files')
        vb.info(f'Deleted {len(deleted_files)} files')
        vb.info(f'Unchanged {len(files_source) - len(copied_files) - len(replaced_files) - len(deleted_files)} files')
        result = dict(copied=len(copied_files),
                    replaced=len(replaced_files),
                    deleted=len(deleted_files),
                    unchanged=len(files_source) - len(copied_files) - len(replaced_files) - len(deleted_files))

    if update_log_table:
        vb.debug('Attempting to update log table with results')

        update_dict = {
            'target_size_after_bytes': dirsize(target),
            'end_ts': datetime.utcnow(),
            'is_completed': True
        }

        update_sql = pg.build_update(schema=directory_backup_table_schema,
                                     table=directory_backup_table_name,
                                     pkey_name='directory_backup_id',
                                     pkey_value=directory_backup_id,
                                     columns=list(update_dict.keys()),
                                     values=list(update_dict.values()),
                                     validate=True)

        if not dry_run:
            pg.execute(update_sql)

        vb.debug(f'{ws}Successful')

    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})
    vb.program_complete('Backup complete', start_ts=start_ts)
