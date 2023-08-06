import click
import os
import pydoni
import pydoni.db
from datetime import datetime
from cli_reference.common import Verbose


def define_template():
    """Define markdown template."""
    template = """
    # {author}: {title}

    *This note was refreshed on {refreshed_on} at {refreshed_at}.*

    **Type**: {book_type}

    **My Rating**: {my_rating}

    **Date Begun**: {date_begun}

    **Date Completed**: {date_completed}

    ### MY COMMENTS
    {my_comments}

    ### MY NOTES
    {my_notes}
    """
    return '\n'.join([x.strip() for x in template.split('\n')])


def generate_notes_string(row, template):
    """Transform books dataframe row into a string."""
    title = row['title']
    if row['subtitle'] is not None:
        title = title + ': ' + row['subtitle']

    now = datetime.now()
    refreshed_on = now.strftime('%B %d, %Y')
    refreshed_at = now.strftime('%-I:%M:%S %p')

    author = row['author']
    book_type = row['book_type']
    my_rating = row['rating'] if row['rating'] is not None else 'Not Yet Rated'
    date_begun = row['date_begun'].strftime('%B %d, %Y')
    if row['date_completed'] is not None:
        date_completed = row['date_completed'].strftime('%B %d, %Y')
    else:
        date_completed = 'Not Yet Completed'

    my_comments = row['comments']
    my_comments = '(No comments)' if my_comments is None else my_comments

    my_notes = row['notes_md']
    my_notes = '(No notes)' if my_notes is None else my_notes

    return template.format(**locals()).strip()


def build_outfile(row):
    """Build output Markdown filename."""
    title = row['title']
    if row['subtitle'] is not None:
        title = title + ': ' + row['subtitle']

    author = row['author']
    outfile = '{author} - {title}.md'.format(**locals())

    return outfile.replace('/', '_').replace(':', '_')


@click.option('-o', '--output-dpath', type=click.Path(exists=True), required=True,
              help='Directory to write output Markdown files to.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print messages to console.')

@click.command()
def book_table_to_md(output_dpath, verbose):
    """
    Convert Postgres "notes"."books" table to Markdown.
    """
    args, result = pydoni.pydonicli_declare_args(locals()), dict()
    pydoni.pydonicli_register({'command_name': pydoni.what_is_my_name(with_modname=True), 'args': args})

    vb = Verbose(verbose)
    pg = pydoni.db.Postgres()

    df_books = pg.read_table('notes', 'books')
    template = define_template()

    if not os.path.isdir(output_dpath):
        os.makedirs(output_dpath)

    for idx, row in df_books.iterrows():
        notes_string = generate_notes_string(row, template)
        outfile = build_outfile(row)
        with open(os.path.join(output_dpath, outfile), 'w') as f:
            f.write(notes_string)

    vb.program_complete()

    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})
