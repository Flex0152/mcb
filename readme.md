# General
This is a small application for monitoring the Windows clipboard. The GUI in app.py creates a Tkinter text field. The text field updates with each new value from the clipboard.
The values are also stored in a database located in the same folder.
Additionally, there is a CLI with mcb.py. The CLI allows you to search the database.

## Note for Python 3.13
There is currently a bug in version 3.13 related to virtual environments and Tkinter. At the moment, the tcl folder from %ProgramFiles%\Python313\ must be copied directly into the venv\ folder.
Alternatively, you can use an older Python version.