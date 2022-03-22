# Swap msgid and msgstr, saving original msgid in comments
# Restore original msgid from comments

This script can swap msgid and msgstr in your PO files and save the original msgid in comments.
By default:
- it expects Game.po filename
- it expects utf-8-sig encoding
- it will swap clear the msgstr after moving it to msgid
- it will quit on suspected errors
- it will add \_restored to the restored file name
- it will add \_swapped to the swapped file name

You can change these defaults in the script itself or via command line arguments.

## Usage

usage: swap-po.py [-h] [-encoding [ENCODING]] [-c] [-r|-s] [filename]

Swap msgid and msgstr or restore original msgid from a swapped PO file Adds X-Swapped-PO header to swapped files Auto-
detects swapped files via a header (X-Swapped-PO) Usage: swap-po.py filename Force restore swap-po.py -restore
filename swap-po.py -r filename Force swap swap-po.py -swap filename swap-po.py -s filename

positional arguments:
  filename              Task list to run from base.config.yaml

optional arguments:
  -h, --help            show this help message and exit
  -encoding [ENCODING], -e [ENCODING]
                        Encoding of the PO file (use None to try to detect the PO encoding automatically)
  -c, -clear_msgstr     Use -c or -clear to clear msgstr in a swapped PO
  -r, -restore          Use -r or -restore to force restore the original source in the translated PO
  -s, -swap             Use -s or -swap to force swap msgid and msgstr in a PO file
