from libraries.polib import POEntry
import polib
import argparse
from pathlib import Path
import re

ENC = "utf-8-sig"  # Default encoding for PO files

SRC_START = "Original source block, please don't delete and don't change: ~~~/"
SRC_END = "/~~~ End of original source block"
DEF_FN = 'Game.po'  # Default PO file name
BREAK_ON_SUSPECTED_ERRORS = False
CLR_MSGSTR = True
WRAP = 0


def swap(pofile: polib.POFile, clear_msgstr: bool = CLR_MSGSTR):
    for entry in pofile:
        if not entry.msgstr:
            print('ERROR: No translation, can\'t use empty strings as msgid')
            print(f'Entry (line {entry.linenum}): {entry.msgid}')
            return 101
        if SRC_START in entry.comment.splitlines(
            False
        ) or SRC_END in entry.comment.splitlines(False):
            print(
                'ERROR: Unexpected prefix in comments. '
                'Is this actually a swapped file?'
            )
            print(f'Entry: {entry.msgid}')
            if BREAK_ON_SUSPECTED_ERRORS:
                return 102

        # Save original msgid to comments
        entry.comment = (
            entry.comment
            + '\n'
            + SRC_START
            + '\n'
            + '\n'.join(entry.msgid.splitlines(False))
            + '\n'
            + SRC_END
        )

        # Swap or clear msgstr if needed
        if clear_msgstr:
            entry.msgid, entry.msgstr = entry.msgstr, ''
        else:
            entry.msgid, entry.msgstr = entry.msgstr, entry.msgid

        # print(f'Entry msgid:   {entry.msgid}')
        # print(f'Entry msgstr:  {entry.msgstr}')
        # print(f'Entry comment: {entry.comment}')

    return 0


def restore(pofile: polib.POFile):
    for entry in pofile:
        # entry = POEntry(entry)
        if SRC_START not in entry.comment.splitlines(
            False
        ) or SRC_END not in entry.comment.splitlines(False):
            print(
                'ERROR: No original source block in entry. File damaged?'
                'Or is this actually an original file?'
            )
            print(f'Entry (line {entry.linenum}): {entry.msgid}')
            print(f'Comment: {entry.msgid}')
            if BREAK_ON_SUSPECTED_ERRORS:
                return 201
            continue

        # Restore the original msgid
        in_source_block = False
        msgid = []
        comment = []
        for line in entry.comment.splitlines(False):
            if line == SRC_START:
                in_source_block = True
                continue
            if line == SRC_END:
                in_source_block = False
                continue
            if in_source_block:
                msgid.append(line)
                continue
            comment.append(line)

        entry.comment = '\n'.join(comment)

        line_ending = '\n'
        if '\r\n' in entry.msgid:
            line_ending = '\r\n'

        entry.msgid = line_ending.join(msgid)

        msgstr = entry.msgstr

        # print(f'Entry msgid:   {entry.msgid}')
        # print(f'Entry msgstr:  {entry.msgstr}')
        # print(f'Entry comment: {entry.comment}')

    return 0


def main():
    parser = argparse.ArgumentParser(
        description='''
    Swap msgid and msgstr or restore original msgid from a swapped PO file
    Adds X-Swapped-PO header to swapped files
    Auto-detects swapped files via a header (X-Swapped-PO)
    Usage: swap-po.py filename
    
    Force restore
    swap-po.py -restore filename
    swap-po.py -r filename
    
    Force swap
    swap-po.py -swap filename
    swap-po.py -s filename
    '''
    )

    parser.add_argument(
        'filename',
        type=str,
        nargs='?',
        default=DEF_FN,
        help='Task list to run from base.config.yaml',
    )

    parser.add_argument(
        'encoding',
        type=str,
        nargs='?',
        default=ENC,
        help='Encoding of the PO file '
        '(use None to try to detect the PO encoding automatically)',
    )

    parser.add_argument(
        '-c',
        '-clear_msgstr',
        dest='clear',
        action='store_true',
        default=CLR_MSGSTR,
        help='Use -r or -restore to restore the original source in the translated PO',
    )

    parser.add_argument(
        '-r',
        '-restore',
        dest='restore',
        action='store_true',
        help='Use -r or -restore to restore the original source in the translated PO',
    )

    parser.add_argument(
        '-s',
        '-swap',
        dest='swap',
        action='store_true',
        help='Use -s or -swap to force swap msgid and msgstr in a PO file',
    )

    args = parser.parse_args()

    if not args.filename:
        print('Specify the filename in script parameters.')
        parser.print_help()
        return 1

    if not Path(args.filename).is_file():
        print('Specified PO file not found or is not a file.')
        return 2

    pofile = polib.pofile(args.filename, encoding=args.encoding, wrapwidth=WRAP)

    if len(pofile) == 0:
        print('Something wrong with the PO file. No entries loaded.')
        return 3

    fn_tuple = args.filename.rpartition('.')
    if not fn_tuple[0]:
        print('The file should have an extension?.. Probably, PO? :)')
        return 4

    if args.swap and args.restore:
        print('Specify one of -restore or -swap arguments only.')
        return 5

    task = '(No detection. Script arguments provided.'
    new_fn = ''

    if not (args.swap or args.restore):
        if 'X-Swapped-PO' in pofile.metadata.keys():
            print('Detected swapped PO. Restoring the original source.')
            task = 'restore'
        else:
            print('Detected original PO. Swapping msgid and msgstr.')
            task = 'swap'

    print(f'{args}. Detected task for file: {task}')

    if task == 'restore' or args.restore:
        new_fn = fn_tuple[0] + '_restored.po'
        result = restore(pofile)
        pofile.metadata.pop('X-Swapped-PO', None)
    elif task == 'swap' or args.swap:
        new_fn = fn_tuple[0] + '_swapped.po'
        result = swap(pofile)
        pofile.metadata.update({'X-Swapped-PO': 'Swapped'})

    if not new_fn:
        print('Could not create new file name from the original file name.')
        print(f'Original file name: {args.filename}')
        return 6

    if not result:
        pofile.save(new_fn)

    return result


if __name__ == '__main__':
    main()
