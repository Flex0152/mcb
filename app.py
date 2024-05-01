import pyperclip
from time import sleep
import pygetwindow as gw

from model import Content, Window, engine
from sqlalchemy.orm import Session
import sqlalchemy as sa


try:
    while(True):
        sleep(0.5)
        print(pyperclip.paste())
        txt = pyperclip.waitForNewPaste()
        win = str(gw.getActiveWindow().title).split("-")
        
        with Session(engine) as session:
            stmt = sa.Select(Window).where(Window.windowName == win[-1].strip())
            window = session.scalar(stmt)
            if not window:
                window = Window(win[-1].strip())
            
            content = Content(txt)
            window.contents.append(content)

            session.add(window)
            session.add(content)
            session.commit()

except KeyboardInterrupt:
    print("[*] Programm beendet!")
except UnicodeDecodeError as e:
    print("[!] Im Versuch Inhalte zu schreiben ist ein Fehler aufgetreten.")