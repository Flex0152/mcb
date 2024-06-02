'''
Zum laden der Elemente in die Zwischenablage.
'''
import sqlalchemy as sa
import sqlalchemy.orm as so
from model import Content, Window
# from app import engine
from model import engine
import pandas as pd
from rich.panel import Panel
from rich import print
from typer import Typer


app = Typer()

def convert_to_DataFrame(result: list) -> pd.DataFrame:
    """Erstellt im ersten Schritt eine Liste mit Dictonarys. Diese Liste 
    wird in ein DataFrame konvertiert und zurückgegeben"""
    erg = []
    results = result # get_all_rows()
    for row in results:
        tmp = {
            "ID" : row.id,
            "Content" : row.content.strip()
        }
        erg.append(tmp)
    return pd.DataFrame(erg)

def get_all_rows():
    """Ruft alle Zeilen der Content Tabelle ab."""
    with so.Session(engine) as session:
        result = session.scalars(sa.Select(Content)).all()
    return result

def get_content_by_name(name: str):
    """Ruft den Content der name enthält ab. Gibt den gefundenen
    Content über Std Out in einem rich Panel aus"""
    with so.Session(engine) as session:
        result = session \
            .scalars(sa.Select(Content) \
            .filter(Content.content.like(f"%{name}%"))).all()
        return result

def get_content_by_id(id: int):
    """Ruft den Content der angegebenen ID ab. Gibt den gefundenen 
    Content über Std Out in einem rich Panel aus"""
    with so.Session(engine) as session:
        stmt = sa.Select(Content).where(Content.id == id)
        result = session.scalar(stmt)
    return result

def get_content_by_windowName(name: str):
    """Ruft den Content des angegebenen Fensters ab. 
    Bei uneingeutigen Namen, wird das zuerst gefundene Fenster verwendet."""
    with so.Session(engine) as session:
        result = session.scalar(sa.Select(Window).where(Window.windowName.like(f"%{name}%")))
        if result != None:
            return result.contents
        else:
            return result
        

@app.command()
def show(id: int = 0, suchbegriff: str = "", windowName: str = "") -> None:
    """Ausgabe der gesuchten Werte. Reagiert auf id, Suchbegriff oder Fenstername"""
    if id != 0:
        result = get_content_by_id(id)
        print(Panel(result.content) if result != None else Panel(":-1: Keine Ergebnisse"))
    if suchbegriff != "":
        result = get_content_by_name(suchbegriff)
        if len(result) != 0:
            for item in result:
                print(Panel(item.content))
        else:
            print(Panel(":-1: Keine Ergebnisse"))
    if windowName != "":
        results = get_content_by_windowName(windowName)
        if results != None:
            for item in results:
                print(Panel(item.content))
        else:
            print(Panel(":-1: Keine Ergebnisse"))


if __name__ == '__main__':
    app()
