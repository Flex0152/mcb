# General
This is a small application for monitoring the Windows clipboard. The GUI in app.py creates a Tkinter TreeView. The Treeview updates with each new value from the clipboard.
The values are also stored in a database located in the same folder. The database can be searched using the search field by text content or by category.
Additionally, there is a CLI with mcb.py. The CLI allows you to search the database.

![alt text](https://github.com/Flex0152/mcb/blob/master/png/main.png)

## Note for Python 3.13
There is currently a bug in version 3.13 related to virtual environments and Tkinter. At the moment, the tcl folder from %ProgramFiles%\Python313\ must be copied directly into the venv\ folder.
Alternatively, you can use an older Python version.

## todo
The entries should be markable as a text block. A separate Treeview will display all entries that have been marked as a text block.