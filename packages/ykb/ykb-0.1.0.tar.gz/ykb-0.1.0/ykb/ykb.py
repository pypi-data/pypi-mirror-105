from subprocess import call
from datetime import datetime
import sys, tempfile, os
from pathlib import Path
import click
import shutil
import uuid
import re


HEADER_DELIM = '+++'

HEADER_FIELDS = """Created: {}
Updated: {}
"""

PLACEHOLDER = 'Your text goes here.'

TEMPLATE = '{}\n{}{}\n\n{}\n'.format(
   HEADER_DELIM,
   HEADER_FIELDS,
   HEADER_DELIM,
   PLACEHOLDER
)

def edit_note_with_editor(text, lineno=0):
    EDITOR = os.environ.get('EDITOR', 'vim')
    initial_message = str.encode(text)
    with tempfile.NamedTemporaryFile(suffix='.md') as tf:
        tf.write(initial_message)
        tf.flush()
        call([EDITOR, '+{}'.format(lineno), tf.name])
        tf.seek(0)
        edited_message = tf.read()
    return edited_message


def get_now_timestamp():
    now = datetime.now()
    timestamp = now.isoformat()[:19]
    return timestamp


def get_default_notebook_dir():
    home_dir = Path.home()
    p = home_dir / '.edda'
    return p


def get_default_note_dir():
    notebook_dir = get_default_notebook_dir()
    p = notebook_dir / 'notes'
    return p


def get_default_archive_dir():
    notebook_dir = get_default_notebook_dir()
    p = notebook_dir / 'archive'
    return p


def new_note():
    timestamp = get_now_timestamp()
    text = TEMPLATE.format(timestamp, timestamp)
    new_text = edit_note_with_editor(text, lineno=7)
    if text == new_text.decode():
        return None
    notedir = get_default_note_dir()
    if not notedir.exists():
        notedir.mkdir(parents=True, exist_ok=True)
    fname = str(uuid.uuid4()) + '.md'
    with open(notedir / fname, 'w') as outfile:
        outfile.write(new_text.decode())
    return fname


def get_note_files(uuid):
    if type(uuid) is str:
        notedir = get_default_note_dir()
        l = list(notedir.rglob(uuid + '*.md'))
        return l
    elif type(uuid) is list:
        notedir = get_default_note_dir()
        all_files = []
        for string in uuid:
            l = list(notedir.rglob(string + '*.md'))
            all_files.extend(l)
        return all_files
    else:
        print('Unsupported ID type')
        return None


def load_note(notefile):
    with open(notefile, 'rb') as infile:
        message = infile.read()
    return message.decode()


def update_timestamp(text):
    timestamp = get_now_timestamp()
    lines = text.decode().split('\n')
    #print(lines)
    if not lines[0].startswith(HEADER_DELIM):
        # TODO: this codepath was not tested yet
        HEADER.format(timestamp, timestamp)
        return HEADER + text
    else:
        new_lines = [lines[0]]
        in_header = True
        for line in lines[1:]:
            if line.startswith('Updated: ') and in_header:
                new_line = 'Updated: {}'.format(timestamp)
                new_lines.append(new_line)
            elif line.startswith(HEADER_DELIM) and in_header:
                in_header = False
                new_lines.append(line)
            else:
                new_lines.append(line)
        new_text = '\n'.join(new_lines)
        return new_text.encode()
    return text


def edit_note(noteid):
    notedir = get_default_note_dir()
    if not notedir.exists():
        print('Notes directory {} does not exists. Make a new note to create it.'.format(notedir))
        sys.exit(1)
    if noteid is None:
        # if noteid is not specified, looks for the latest updated note
        last_updated = find_last_updated_note()
        notefiles = [last_updated]
    else:
        notefiles = get_note_files(noteid)
    if len(notefiles) == 0:
        print('Note not found with ID {}.'.format(noteid))
        sys.exit(1)
    if len(notefiles) > 1:
        print('Too many notes matching the ID {}:'.format(noteid))
        for n in notefiles:
            print('  {}'.format(n.name))
        sys.exit(1)
    text = load_note(notefiles[0])
    new_text = edit_note_with_editor(text, lineno=7)
    if new_text.decode() != text:
        final_text = update_timestamp(new_text)
        with open(notefiles[0], 'w') as outfile:
            outfile.write(final_text.decode())
        return True, str(notefiles[0].name)
    else:
        return False, str(notefiles[0].name)


def get_list_data(lines):
    # In case of possibly corrupted notes,
    # fills the fields with clearly suspicious data.
    # Dates will appear at beginning or end of a sorted list.
    data = {
        'updated': '9999-99-99T99:99:99',
        'created': '9999-99-99T99:99:99',
        'summary': 'NONE'
    }
    # consumes lines until the beginning line of the header
    for l in lines:
        if l.startswith(HEADER_DELIM):
            break
    # consumes lines within the header
    for l in lines:
        if l.startswith(HEADER_DELIM):
            break
        if l.startswith('Created: '):
            data['created'] = l[8:-1].strip()   # exclude the newline
            continue
        if l.startswith('Updated: '):
            data['updated'] = l[8:-1].strip()  # exclude the newline
            continue
    # consumes lines in the body of the notes
    for l in lines:
        if len(l) > 2:
            data['summary'] = l[:-1]   # exclude the newline
            break
    return data


def format_line_for_list(line, width=80):
    if len(line) <= width:
        l = line
    else:
        pos = line[:width-2].rfind(' ')
        l = line[:pos] + '...'
    return l


def format_note_for_list(note, width=80):
    text = note[1]['summary']
    # TODO: find better way to caclulate length of a styled string
    datetime = note[1]['created'][:-3]
    noteid = note[0].name[:8]
    datetime_s = click.style(datetime, fg='yellow')
    noteid_s = click.style(noteid, fg='green')
    info = '{} {} '.format(datetime, noteid)
    info_s = '{} {} '.format(datetime_s, noteid_s)
    l = format_line_for_list(text, width=width - len(info))
    return info_s + l


def list_notes(width=80):
    notedir = get_default_note_dir()
    note_files = list(notedir.rglob('*.md'))
    notes = []
    for notefile in note_files:
        with open(notefile, 'r') as f:
            data = get_list_data(f)
        notes.append((notefile, data))
    notes = sorted(notes, key = lambda val: val[1]['created'])
    for note in notes:
        line = format_note_for_list(note, width=width)
        click.echo(line)


def find_tags(notefile, tags):
    data = {}
    pat = re.compile(r"@(\w+)")
    with open(notefile, 'r') as f:
        before_header = True
        in_header = False
        after_header = False
        for line in f:
            if line.startswith(HEADER_DELIM) and before_header:
                before_header = False
                in_header = True
                continue
            if line.startswith(HEADER_DELIM) and in_header:
                in_header = False
                after_header = True
                continue
            if after_header and len(line) > 2:
                tags_in_line = pat.findall(line)
                for t in tags_in_line:
                    if t in tags:
                        tags[t] += 1
                    else:
                        tags[t] = 1
                continue
    return tags


def list_tags():
    notedir = get_default_note_dir()
    note_files = list(notedir.rglob('*.md'))
    tags = {}
    for note in note_files:
        tags = find_tags(note, tags)
    maxlen = max([len(x) for x in tags])
    # trick to use different orders for frequency and tag name
    tags_sorted = sorted(((v,k) for k,v in tags.items()), key=lambda tup: (-tup[0],tup[1].lower()), reverse=True)
    for tag in reversed(tags_sorted):
        print('{:{maxlen}} {:4}'.format(tag[1], tag[0], maxlen=maxlen))


def get_note_header_fields(f):
    header = {}
    # consumes lines until the beginning line of the header
    for l in f:
        if l.startswith(HEADER_DELIM):
            break
    # consumes lines within the header
    for l in f:
        if l.startswith(HEADER_DELIM):
            break
        pos = l.find(':')
        if pos == -1:
            return None
        key = l[:pos].strip()
        value = l[pos+1:].strip()
        header[key] = value
    return header


def find_all_headers():
    notedir = get_default_note_dir()
    note_files = list(notedir.rglob('*.md'))
    headers = {}
    for note in note_files:
        with open(note, 'r') as f:
            header = get_note_header_fields(f)
            if header is None:
                print('Header format error in note ID {}.'.format(note))
                return None
            headers[note] = header
    return headers


def find_last_updated_note():
    headers = find_all_headers()
    updates = []
    for h in headers:
        if 'Updated' not in headers[h]:
            print('"Updated" field not found in {}'.format(h))
        else:
            updates.append((h, headers[h]['Updated']))
    #print(updates)
    min_val = max(updates, key=lambda x: x[1])
    #print(min_val)
    return min_val[0]


def search_lines(lines, string, ignore_case=False):
    # In case of possibly corrupted notes,
    # fills the fields with clearly suspicious data.
    # Dates will appear at beginning or end of a sorted list.
    data = {
        'created': '9999-99-99T99:99:99',
        'result': []
    }
    # consumes lines until the beginning line of the header
    for l in lines:
        if l.startswith(HEADER_DELIM):
            break
    # consumes lines within the header
    for l in lines:
        if l.startswith(HEADER_DELIM):
            break
        if l.startswith('Created: '):
            data['created'] = l[8:-1].strip()   # exclude the newline
            continue
    # consumes lines in the body of the notes
    search_string = string.lower() if ignore_case else string
    for l in lines:
        search_line = l.lower() if ignore_case else l
        if search_string in search_line:
            data['result'].append(l[:-1])
    return data


def format_line_for_search(line, width=80, target=None, color=False, ignore_case=False):
    if target is None:
        l = format_line_for_list(line)
    else:
        # TODO: truncate long lines around the position of the target string
        pos = line.find(target)
        if color:
            # splits the original string while keeping the "separators"
            parts = re.split('(' + target + ')', line, flags=re.IGNORECASE)
            for i, item in enumerate(parts):
                # surround odd separators with color
                if i % 2 != 0:
                    parts[i] = click.style(parts[i], fg='red')
            l = ''.join(parts)
        else:
            l = line
    return l


def format_note_for_search(note, width=80, target=None, color=False):
    if len(note[1]['result']) == 0:
        return None
    else:
        lines = []
        for i, line in enumerate(note[1]['result']):
            formatted_line = format_line_for_search(line, target=target, color=color)
            datetime = click.style(note[1]['created'][:-3], fg='yellow')
            noteid = click.style(note[0].name[:8], fg='green')
            lines.append('{} {} {}'.format(datetime, noteid, formatted_line))
    return '\n'.join(lines)


def list_search_result(string, ignore_case=True):
    notedir = get_default_note_dir()
    note_files = list(notedir.rglob('*.md'))
    notes = []
    for notefile in note_files:
        with open(notefile, 'r') as f:
            # TODO: optimization: the search function could return a regex splitted string as a result;
            # in this way the result does not require another regex splitting in the formatting.
            # A "negative" search result should correspond to a string with only 1 part (no splitting).
            # But maybe it is not an optimizatino: if regex splitting takes much longer than the current search method,
            # it would be applied to aal the lines, while now it is only applied to "positive" lines.
            # Some profiling is necessary to evaluate this optimization.
            result = search_lines(f, string, ignore_case=ignore_case)
        notes.append((notefile, result))
    #notes = sorted(notes, key = lambda val: val[1]['created'])
    for note in notes:
        formatted_note = format_note_for_search(note, target=string, color=True)
        if formatted_note is not None:
            click.echo(formatted_note)


def extract_body(lines):
    # consumes lines until the beginning line of the header
    for l in lines:
        if l.startswith(HEADER_DELIM):
            break
    # consumes lines within the header
    for l in lines:
        if l.startswith(HEADER_DELIM):
            break
    # consumes lines in the body of the notes
    body = []
    for l in lines:
        body.append(l)
    return body


def show_notes(noteid):
    prefix = 'Note ID: {}'
    note_files = get_note_files(noteid)
    for notefile in note_files:
        with open(notefile, 'r') as f:
            result = extract_body(f)
        click.echo(prefix.format(click.style(notefile.name[:-3], fg='green')))
        to_print = ''.join(result)
        click.echo(to_print)


def move_notes(dst, notes, force_yes=False):
    """Moves the list of notes to dst.

    It's a generic function.
    It can be used for archiving/unarchiving, and moving notes between
    different notebooks.
    The list of notes includes the path.
    """
    n_moved = 0
    for src_file in notes:
        answer = 'y'
        if not force_yes:
            # TODO: request should include the title of the note
            answer = input('Archive {} (y/N/q)? '.format(str(src_file.name)[:8]))
        if answer in 'qQ':
            break
        if answer in 'yY':
            shutil.move(str(src_file), str(dst))
            #print('Moving {} to {}'.format(src_file, dst))
            n_moved += 1
    print('Moved {} notes to {}'.format(n_moved, dst))


def cmd_archive(notes, nb=None, force_yes=False):
    # TODO: handle different notebooks
    dst = get_default_archive_dir()
    if not dst.exists():
        dst.mkdir(parents=True, exist_ok=True)
    move_notes(dst, notes, force_yes=force_yes)


@click.group()
def cli():
    pass


@click.command(name='new', help='Add a new note')
def cmd_new_func():
    new_note_file = new_note()
    if new_note_file is not None:
        click.echo('Created note ID {}.'.format(new_note_file[:8]))
    else:
        click.echo('New note not created.')


@click.command(name='list', help='List notes')
def cmd_list_func():
    terminal_width, _ = click.get_terminal_size()
    list_notes(width=terminal_width)


@click.command(name='tags', help='List all tags appearing in the notes')
def cmd_tags_func():
    list_tags()


@click.command(name='show', help='Show one or more notes with matching ID')
@click.argument('noteid')
def cmd_show_func(noteid):
    show_notes(noteid)


@click.command(name='edit', help='Edit an existing note in the editor')
@click.argument('noteid', required=False)
def cmd_edit_func(noteid):
    (updated, note_file) = edit_note(noteid)
    if updated:
        click.echo('Updated note ID {}.'.format(note_file[:8]))
    else:
        click.echo('Note ID {} not changed.'.format(note_file[:8]))


@click.command(name='archive', help='Archive one or more notes')
@click.argument('noteid')
@click.option('--force-yes', '-y', is_flag=True, default=False, help='do not ask for confirmation')
def cmd_archive_func(noteid, force_yes):
    notefiles = get_note_files(noteid)
    cmd_archive(notefiles, force_yes=force_yes)


@click.command(name='search', help='Search string in notes')
@click.argument('string')
@click.option('--no-case', '-i', is_flag=True, default=False, help='perform case insensitive search')
def cmd_search_func(string, no_case):
    list_search_result(string, ignore_case=no_case)


@click.command(name='delete', help='Delete the ID note')
@click.argument('noteid')
def cmd_delete_func(noteid):
    note_files = get_note_files(noteid)
    n = len(note_files) 
    if n == 0:
        click.echo('No matching with note ID "{}".'.format(noteid))
    elif n == 1:
        os.remove(note_files[0])
        click.echo('Removed note {}.'.format(note_files[0]))
    else:
        click.echo('Too many matching notes ({}).'.format(n))


def main():
    cli.add_command(cmd_new_func)
    cli.add_command(cmd_list_func)
    cli.add_command(cmd_tags_func)
    cli.add_command(cmd_show_func)
    cli.add_command(cmd_edit_func)
    cli.add_command(cmd_archive_func)
    cli.add_command(cmd_search_func)
    cli.add_command(cmd_delete_func)
    cli()


if __name__ == '__main__':
    main()

