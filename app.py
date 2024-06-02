import pyperclip
from time import sleep
import pygetwindow as gw
from pathlib import Path
from rich.panel import Panel
from rich import print
from model import Content, Window, Base
from sqlalchemy.orm import Session
import sqlalchemy as sa
from sqlalchemy import create_engine
from model import engine

# ready to remove !!!!
# def create_database_if_not_exists(database_name: str):
#     current_path = Path(__file__).parent
#     engine = create_engine(f"sqlite:///{current_path}/{database_name}")
#     if not Path(current_path / database_name).is_file():
#             Base.metadata.create_all(engine)
    
#     return engine

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

# ready to remove!!!
# engine = create_database_if_not_exists("tester.db")


def main():
    try:
        with Session(engine) as session:
            while(True):
                sleep(0.5)
                print(Panel(pyperclip.paste()))
                txt = pyperclip.waitForNewPaste()
                window_name = str(gw.getActiveWindow().title).split("-")
                
                window = create_window(window_name, session)
                add_content(txt, window, session)

    except KeyboardInterrupt:
        print("[*] Programm beendet!")
    except UnicodeDecodeError as e:
        print("[!] Im Versuch Inhalte zu schreiben ist ein Fehler aufgetreten.")


if __name__ == '__main__':
    main()
