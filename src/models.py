from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, \
    Unicode, UnicodeText, Enum, ForeignKey
from sqlalchemy.orm import relationship

Entity = declarative_base()


class Feed(Entity):
    __tablename__ = 'feeds'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False)
    url = Column(UnicodeText, nullable=False)
    feed_url = Column(UnicodeText, nullable=False)
    unread = Column(Integer, default='0')
    create_at = Column(DateTime, default=datetime.now)
    last_update_at = Column(DateTime)

    entries = relationship('Entry', backref='feed')


class Entry(Entity):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False)
    body = Column(UnicodeText, nullable=False)
    status = Column(Enum('unread', 'read'), default='unread')
    create_at = Column(DateTime, nullable=False)

    feed_id = Column(Integer, ForeignKey('feeds.id'))


if __name__ == '__main__':

    from sqlalchemy import create_engine

    import settings

    engine = create_engine(
        settings.DATABASE_DSN,
        echo=settings.DEBUG
    )
    Entity.metadata.create_all(engine)
