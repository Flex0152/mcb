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


def get_all_rows():
    """Hilfsfunktion für convert_to_DataFrame.
    Ruft alle Zeilen der Content Tabelle ab."""
    with so.Session(engine) as session:
        result = session.scalars(sa.Select(Content)).all()
    return result

def convert_to_DataFrame() -> pd.DataFrame:
    """Erstellt im ersten Schritt eine Liste mit Dictonarys. Diese Liste 
    wird in ein DataFrame konvertiert und zurückgegeben"""
    erg = []
    results = get_all_rows()
    for row in results:
        tmp = {
            "ID" : row.id,
            "Content" : row.content.strip()
        }
        erg.append(tmp)
    return pd.DataFrame(erg)

@app.command()
def load_content_by_id(id: int):
    """Ruft den Content der angegebenen ID ab. Gibt den gefundenen 
    Content über Std Out in einem rich Panel aus"""
    with so.Session(engine) as session:
        stmt = sa.Select(Content).where(Content.id == id)
        result = session.scalar(stmt)
    print(Panel(result.content))


if __name__ == '__main__':
    app()
