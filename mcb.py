'''
Zum laden der Elemente in die Zwischenablage.
'''
import sqlalchemy as sa
import sqlalchemy.orm as so
from model import Content
from app import engine
import pandas as pd


def get_all_rows():
    with so.Session(engine) as session:
        result = session.scalars(sa.Select(Content)).all()
    return result

def convert_to_DataFrame():
    erg = []
    results = get_all_rows()
    for row in results:
        tmp = {
            "ID" : row.id,
            "Content" : row.content.strip()
        }
        erg.append(tmp)
    return pd.DataFrame(erg)

def load_content_by_id(id: int):
    with so.Session(engine) as session:
        stmt = sa.Select(Content).where(Content.id == id)
        result = session.scalar(stmt)
    print(result.content)


if __name__ == '__main__':
    print(convert_to_DataFrame())