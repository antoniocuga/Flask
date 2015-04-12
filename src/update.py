from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import feedparser

from datetime import datetime
from time import mktime

import settings
import models
import import_sunat


db_engine = create_engine(
    settings.DATABASE_DSN,
    echo=settings.DEBUG
)


def main():
    db = sessionmaker(bind=db_engine)()

    feeds = db.query(
        models.Feed
    ).all()

    for feed in feeds:
        feed_data = feedparser.parse(feed.feed_url)
        new_count = 0
        for entry in feed_data['items']:
            if db.query(
                models.Entry
            ).filter(
                models.Entry.title == entry['title']
            ).count() == 0:
                _entry = models.Entry()
                _entry.title = entry['title']
                _entry.body = entry['description']
                _entry.create_at = datetime.fromtimestamp(
                    mktime(entry.updated_parsed)
                )
                _entry.feed_id = feed.id
                db.add(_entry)
                new_count += 1
        feed.unread += new_count
        db.add(feed)
        try:
            db.commit()
        except:
            db.rollback()

if __name__ == '__main__':
    main()
