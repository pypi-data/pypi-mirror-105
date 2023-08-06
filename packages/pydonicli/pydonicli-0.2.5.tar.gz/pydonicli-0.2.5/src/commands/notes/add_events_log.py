import click
import re
import pydoni
import pydoni.vb
from datetime import datetime


def get_entry(tabsize):
    """
    Prompt user for moments entry.
    """

    def capitalize_entry_line(line):
        """
        Capitalize first letter of each sentence in entry line.
        """
        sentence_delim_regex =  '|'.join([x + ' ' for x in [r'\.', r'\?', '!']])
        delims_found = re.findall(sentence_delim_regex, line)
        sentences = re.split(sentence_delim_regex, line)
        sentences = [pydoni.cap_nth_char(x, n=0) for x in sentences]
        line = ''.join([x + y for x, y in zip(sentences, delims_found + [''])])
        return line

    def add_entry_line_timestamp(line):
        """
        Add timestamp to beginning of line.
        """
        return str(datetime.now().strftime('%Y-%m-%d')) + ' ' + line

    def add_entry_line_bullet(line, bullet_char='-'):
        """
        Add bullet to beginning of line.
        """
        return re.sub(r'^(\s*)(.*)', r'\1%s \2' % bullet_char, line)

    entry = []
    while True:
        line = pydoni.get_input("Entry line (enter '' to terminate)")
        if line == '':
            break
        else:
            indent = line.count('\t')
            line = line.strip()
            line = capitalize_entry_line(line)
            line = add_entry_line_timestamp(line)
            line = add_entry_line_bullet(line, bullet_char='-')
            line = '    ' * indent + line
            entry.append(line)

    return entry


@click.option('--events-log-file', type=click.Path(exists=True), required=True,
              help='Filepath of "Events Log.txt".')

@click.command()
def add_events_log(events_log_file):
    """
    Prompt for input and append to "Events Log.txt" file.
    """
    args, result = pydoni.pydonicli_declare_args(locals()), dict()
    pydoni.pydonicli_register({'command_name': pydoni.what_is_my_name(with_modname=True), 'args': args})

    try:
        with open(events_log_file, 'r') as f:
            events_log = f.readlines()

        entry = get_entry(tabsize=4)

        # If file doesn't end with an empty line, append one to beginning of entry
        if not events_log[-1].endswith('\n'):
            entry = [''] + entry

        with open(events_log_file, 'a') as f:
            for line in entry:
                f.write(line + '\n')

        pydoni.vb.program_complete('Events log updated')
        result['lines_entered'] = len(entry)

    except Exception as e:
        # If there's an error, print the entry to the screen so it is not lost
        if 'entry' in locals():
            pydoni.vb.echo('Encountered a problem (traceback below). Entry is saved here for convenience:\n', error=True)

            for line in entry: print(line)
            print('')

        result['lines_entered'] = 0

        import traceback; traceback.print_exc()
        pydoni.pydonicli_register({'e': str(e)})

    pydoni.pydonicli_register({k: v for k, v in locals().items() if k in ['result']})
