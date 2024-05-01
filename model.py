from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy import Column, create_engine, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path
from datetime import datetime


class Base(DeclarativeBase):
    pass

class Content(Base):
    __tablename__ = 'tblContent'

    id: Mapped[int] = Column(Integer, primary_key=True)
    created: Mapped[datetime] = Column(DateTime, default=datetime.now())
    content: Mapped[str]
    windows = relationship('Window', secondary='tblContent2Window', back_populates='contents')

    def __init__(self, content):
        self.content = content

    def __repr__(self) -> str:
        return f"<Content: {self.content}>"

class Window(Base):
    __tablename__ = 'tblWindow'

    id: Mapped[int] = Column(Integer, primary_key=True)
    windowName: Mapped[str] = Column(String, unique=True)
    contents = relationship('Content', secondary='tblContent2Window', back_populates='windows')

    def __init__(self, windowName):
        self.windowName = windowName

    def __repr__(self) -> str:
        return f"<{self.windowName}>"

class Content2Window(Base):
    __tablename__ = "tblContent2Window"
    id: Mapped[int] = Column(Integer, primary_key=True)
    contentID: Mapped[int] = Column(Integer, ForeignKey('tblContent.id'))
    windowID: Mapped[int] = Column(Integer, ForeignKey('tblWindow.id'))

current_path = Path(__file__).parent
engine = create_engine(f"sqlite:///{current_path}/texts.db")


if __name__ == '__main__':
    Base.metadata.create_all(engine)
