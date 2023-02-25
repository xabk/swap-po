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

## Requirements

You'll need polib: `pip install polib`

## Usage

You can just drag the file onto the script and it will try to detect what it should do to the file, and use the default parameters to do it.

Alternatively, you can use command line to gain more control of the process:

`swap-po.py [-h] [-encoding [ENCODING]] [-c] [-r|-s] [filename]`

Swap msgid and msgstr or restore original msgid from a swapped PO file Adds X-Swapped-PO header to swapped files Auto-
detects swapped files via a header (X-Swapped-PO) Usage: swap-po.py filename Force restore swap-po.py -restore
filename swap-po.py -r filename Force swap swap-po.py -swap filename swap-po.py -s filename

positional arguments:

  `filename`              Task list to run from base.config.yaml

optional arguments:

  `-h`, `--help`            show this help message and exit
  
  `-encoding [ENCODING]`, `-e [ENCODING]`   Encoding of the PO file (use None to try to detect the PO encoding automatically)
                        
  `-c`, `-clear_msgstr`     Use -c or -clear to clear msgstr in a swapped PO
  
  `-r`, `-restore`          Use -r or -restore to force restore the original source in the translated PO
  
  `-s`, `-swap`             Use -s or -swap to force swap msgid and msgstr in a PO file
  
## Examples
  
By default, this:
```
#. Key:	1DFB985749BF3FF089CDEEAFF2FED5AF
#. SourceLocation:	/Game/AssetPacks/.../BP_MainMenu_Functions.BP_MainMenu_Functions_C:CreateBackRequest [Script Bytecode]
#. Debug ID:	#0046		Asset: BP_MainMenu_Functions
#: /Game/AssetPacks/.../BP_MainMenu_Functions.BP_MainMenu_Functions_C:CreateBackRequest [Script Bytecode] ### Key: ,001DFB985749BF003FF089CDEEAFF002FED005AF
msgctxt ",1DFB985749BF3FF089CDEEAFF2FED5AF"
msgid "You have unapplied changes.\r\n"
"Leave without applying?"
msgstr "Часть изменений не сохранена.\r\n"
"Выйти без сохранения?"
```

Becomes this:
```
#. Key:	1DFB985749BF3FF089CDEEAFF2FED5AF
#. SourceLocation:	/Game/AssetPacks/.../BP_MainMenu_Functions.BP_MainMenu_Functions_C:CreateBackRequest [Script Bytecode]
#. Debug ID:	#0046		Asset: BP_MainMenu_Functions
#. Original source block, please don't delete and don't change: ~~~/
#. You have unapplied changes.
#. Leave without applying?
#. /~~~ End of original source block
#: /Game/AssetPacks/.../BP_MainMenu_Functions.BP_MainMenu_Functions_C:CreateBackRequest [Script Bytecode] ### Key: ,001DFB985749BF003FF089CDEEAFF002FED005AF
msgctxt ",1DFB985749BF3FF089CDEEAFF2FED5AF"
msgid ""
"Часть изменений не сохранена.\r\n"
"Выйти без сохранения?"
msgstr ""
```

Let's say, we transalted this line to "Some translaton". Then it can be restored to this:
```
#. Key:	1DFB985749BF3FF089CDEEAFF2FED5AF
#. SourceLocation:	/Game/AssetPacks/.../BP_MainMenu_Functions.BP_MainMenu_Functions_C:CreateBackRequest [Script Bytecode]
#. Debug ID:	#0046		Asset: BP_MainMenu_Functions
#: /Game/AssetPacks/.../BP_MainMenu_Functions.BP_MainMenu_Functions_C:CreateBackRequest [Script Bytecode] ### Key: ,001DFB985749BF003FF089CDEEAFF002FED005AF
msgctxt ",1DFB985749BF3FF089CDEEAFF2FED5AF"
msgid ""
"You have unapplied changes.\r\n"
"Leave without applying?"
msgstr "Some translation"
```
