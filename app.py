import pyperclip
from time import sleep
import pygetwindow as gw
from rich import print as rprint
from model import Content, Window
from sqlalchemy.orm import Session
import sqlalchemy as sa
from model import engine

from icecream import ic


def create_window(window_name, session_name):
    stmt = sa.Select(Window).where(Window.windowName == window_name[-1].strip())
    window = session_name.scalar(stmt)
    if not window:
        window = Window(window_name[-1].strip())
    return window

def add_content(txt, window, session_name):
    content = Content(txt)
    window.contents.append(content)
    session_name.add(window)
    session_name.commit()

def get_clipboard() -> str | None:
    try:
        return pyperclip.paste()
    except pyperclip.PyperclipException:
        return None

def format_output(value: str) -> None:
    print("+"*40)
    print()
    print(value + "\n")


def main():
    # initial
    old_value = get_clipboard()
    try:
        with Session(engine) as session:
            while True:
                sleep(1)
                # get clipboard every second
                new_value = get_clipboard()
                # if the new value not equal to the old value
                # and if new value not None
                if old_value != new_value and new_value != None:
                    format_output(new_value)
                    window_name = str(gw.getActiveWindow().title).split("-")
                    window = create_window(window_name, session)
                    # add the content to database
                    add_content(new_value, window, session)
                    # assign the new value to the old_value variable        
                    old_value = new_value
    except KeyboardInterrupt:
        rprint("[*] Programm beendet!")
    except UnicodeDecodeError as e:
        rprint("[!] Im Versuch Inhalte zu schreiben ist ein Fehler aufgetreten.")
    

if __name__ == '__main__':
    main()
