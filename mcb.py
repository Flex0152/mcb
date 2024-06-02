'''
Zum laden der Elemente in die Zwischenablage.
'''
import sqlalchemy as sa
import sqlalchemy.orm as so
from model import Content
from app import engine
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


@app.command()
def get_content_by_name(name: str) -> None:
    """Ruft den Content der name enthält ab. Gibt den gefundenen
    Content über Std Out in einem rich Panel aus"""
    with so.Session(engine) as session:
        result = session \
            .scalars(sa.Select(Content) \
            .filter(Content.content.like(f"%{name}%"))).all()
        for item in result:
            print(Panel(item.content))

@app.command()
def get_content_by_id(id: int) -> None:
    """Ruft den Content der angegebenen ID ab. Gibt den gefundenen 
    Content über Std Out in einem rich Panel aus"""
    with so.Session(engine) as session:
        stmt = sa.Select(Content).where(Content.id == id)
        result = session.scalar(stmt)
    print(Panel(result.content))


if __name__ == '__main__':
    app()
