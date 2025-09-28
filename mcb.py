'''
Zum laden der Elemente in die Zwischenablage.
'''
import sqlalchemy as sa
import sqlalchemy.orm as so
from model import Content, Window
from model import engine
from rich.panel import Panel
from rich import print as rprint
from typer import Typer


app = Typer()

def get_all_rows():
    """Ruft alle Zeilen der Content Tabelle ab."""
    with so.Session(engine) as session:
        result = session.scalars(sa.Select(Content)).all()
    return result

def get_content_by_name(name: str) -> list:
    """Ruft den Content der name enthält ab. Gibt den gefundenen
    Content als Liste zurück"""
    with so.Session(engine) as session:
        contents = session \
            .scalars(sa.Select(Content) \
            .filter(Content.content.like(f"%{name}%"))).all()
        
        result = [{"content":content.content, "created":f"{content.created}"} 
                  for content in contents]
        return result 

def get_content_by_windowname(name: str):
    """Ruft den Content des angegebenen Fensters ab."""
    with so.Session(engine) as session:
        contents = (
        session.query(Content)
        .join(Content.windows)
        .filter(Window.windowName.like(f"%{name}%"))
        .all()
        )
        
        result = [{"content":content.content, "created":f"{content.created}"} 
                  for content in contents]
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
    elif windowname != "":
        results = get_content_by_windowname(windowname)

    if len(results) > 0:
        for item in results:
            content = item['content']
            created = item['created']
            rprint(Panel(f"Erstellt am: \t{created}\nContent: \t{content}"))
    else:
        rprint(Panel(":-1: Keine Ergebnisse"))


if __name__ == '__main__':    
    app()
