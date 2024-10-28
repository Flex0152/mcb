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

def get_content_by_name(name: str) -> list:
    """Ruft den Content der name enthält ab. Gibt den gefundenen
    Content als Liste zurück"""
    with so.Session(engine) as session:
        result = session \
            .scalars(sa.Select(Content) \
            .filter(Content.content.like(f"%{name}%"))).all()
        return result if len(result) != 0 else None

def get_content_by_windowname(name: str):
    """Ruft den Content des angegebenen Fensters ab."""
    with so.Session(engine) as session:
        contents = (
        session.query(Content.content)
        .join(Content.windows)
        .filter(Window.windowName == name)
        .all()
        )
        for content in contents:
            print(content.content)
        result = [content.content for content in contents]
        return result

def get_content_by_id(id: int):
    """Ruft den Content der angegebenen ID ab. Gibt den gefundenen 
    Content über Std Out in einem rich Panel aus"""
    with so.Session(engine) as session:
        stmt = sa.Select(Content).where(Content.id == id)
        result = session.scalar(stmt)
    return result


@app.command()
def show(suchbegriff: str = "", windowname: str = "") -> None:
    """Ausgabe der gesuchten Werte. Reagiert Suchbegriff oder Fenstername"""

    if suchbegriff != "":
        results = get_content_by_name(suchbegriff)
        # if len(results) > 0:
        #     for item in results:
        #         print(Panel(item.content))
        # else:
        #     print(Panel(":-1: Keine Ergebnisse"))

    if windowname != "":
        results = get_content_by_windowname(windowname)
    if len(results) > 0:
        for item in results:
            print(Panel(item))
    else:
        print(Panel(":-1: Keine Ergebnisse"))


if __name__ == '__main__':    
    app()
