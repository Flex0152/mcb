import pyperclip
from time import sleep
from datetime import datetime
import pygetwindow as gw
from rich import print as rprint
from model import Content, Window
from sqlalchemy.orm import Session
import sqlalchemy as sa
from model import engine

import tkinter as tk


def create_window(window_name, session_name):
    """if we have a new window, build a new window object otherwise
    give the window object from the database"""
    stmt = sa.Select(Window).where(Window.windowName == window_name[-1].strip())
    window = session_name.scalar(stmt)
    if not window:
        window = Window(window_name[-1].strip())
    return window

def add_content(txt, window, session_name):
    """Add the content with the windowname to the database"""
    content = Content(txt)
    window.contents.append(content)
    session_name.add(window)
    session_name.commit()

def get_clipboard() -> str | None:
    """get clipboard with error handling"""
    try:
        return pyperclip.paste()
    except pyperclip.PyperclipException:
        return None

def format_output(value: str) -> None:
    """Simple formated output"""
    print("+"*40)
    print()
    print(value + "\n")

class ClipboardMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Zwischenablage-Monitor")

        self.old_value = None

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Kopieren", command=self.copy_text)

        # Search Field
        search_label = tk.Label(self, text="Suche")
        search_label.grid()
        search_widget = tk.Entry(self)
        search_widget.grid()

        # Text-Widget
        self.text_widget = tk.Text(self)
        self.text_widget.grid() #.pack(fill=tk.BOTH, expand=True)
        self.bind("<Button-3>", self.show_menu)

        # Scrollbar
        # scrollbar = tk.Scrollbar(self)
        # scrollbar.grid() #.pack(side=tk.RIGHT, fill=tk.Y)
        # self.text_widget.config(yscrollcommand=scrollbar.set)
        # scrollbar.config(command=self.text_widget.yview)

        # Button to remove text field content
        clear_button = tk.Button(self, text="Löschen", command=self.clear_text)
        clear_button.grid() #.pack()

        # start refresh
        self.update_gui()

    # create context menu
    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def copy_text(self):
        # copy from text field itself
        selected_text = self.text_widget.selection_get()
        pyperclip.copy(selected_text)

    def update_gui(self):
        new_value = get_clipboard()
        if new_value != self.old_value and new_value is not None:
            with Session(engine) as session:
                # get window name with split at english dash
                window_name = str(gw.getActiveWindow().title).split("–")
                window = create_window(window_name, session)
                # add the content to database
                add_content(new_value, window, session)
            # create header of the gui, window name and Datetime
            window_content = f"{30 * "+"}\n" + \
                f"{datetime.strftime(datetime.now(), '%a %d %b %Y, %H:%M:%S')} \n" + \
                f"{window_name[-1].strip()} \n{30 * "-"}\n"
            # update text field with the new values
            self.text_widget.insert(tk.END, window_content)
            self.text_widget.insert(tk.END, new_value + "\n\n")
            self.old_value = new_value
        # repeat every 1000 ms
        self.after(1000, self.update_gui)

    def clear_text(self):
        self.text_widget.delete('1.0', tk.END)
    

if __name__ == '__main__':
    app = ClipboardMonitor()
    app.mainloop()