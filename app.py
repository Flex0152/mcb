import pyperclip
from time import sleep
import pygetwindow as gw
from rich import print as rprint
from model import Content, Window
from sqlalchemy.orm import Session
import sqlalchemy as sa
from model import engine


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


def main():
    try:
        with Session(engine) as session:
            while True:
                
                try:
                    sleep(0.5)
                    rprint(pyperclip.paste())
                    print()
                    txt = pyperclip.waitForNewPaste()
                    if txt == "":
                        txt = "Inhalt nicht zu erfassen!"
                # Wird das Notebook gesperrt, ist kein Zugriff auf die Zwischenablage möglich. -> Ausnahme wird abgefangen und ignoriert.
                except pyperclip.PyperclipWindowsException:
                    continue

                window_name = str(gw.getActiveWindow().title).split("-")
                window = create_window(window_name, session)
                
                add_content(txt, window, session)

    except KeyboardInterrupt:
        rprint("[*] Programm beendet!")
    except UnicodeDecodeError as e:
        rprint("[!] Im Versuch Inhalte zu schreiben ist ein Fehler aufgetreten.")
    

if __name__ == '__main__':
    main()
