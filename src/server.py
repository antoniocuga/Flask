from flask import Flask, g, render_template, url_for, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import feedparser

import settings
import models
import forms

app = Flask(
    __name__,
    static_folder=settings.STATIC_PATH,
    static_url_path=settings.STATIC_URL_PATH
)
db_engine = create_engine(
    settings.DATABASE_DSN,
    echo=settings.DEBUG
)


@app.before_request
def before_request():
    g.db = sessionmaker(
        bind=db_engine
    )()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    feeds = g.db.query(
        models.Feed.id,
        models.Feed.title,
        models.Feed.unread,
        models.Feed.last_update_at
    ).order_by(
        models.Feed.title
    ).all()

    return render_template(
        'index.html',
        feeds=feeds,
    )


@app.route('/feed/<int:id>')
def feed(id):
    feed = g.db.query(
        models.Feed.id,
        models.Feed.title,
        models.Feed.url
    ).filter(
        models.Feed.id == id
    ).first()

    entries = g.db.query(
        models.Entry.id,
        models.Entry.title,
        models.Entry.status,
        models.Entry.create_at
    ).filter(
        models.Entry.feed_id == feed.id
    ).order_by(
        models.Entry.create_at
    ).all()

    return render_template(
        'feed.html',
        feed=feed,
        entries=entries
    )


@app.route('/read/<int:id>')
def read(id):
    entry = g.db.query(
        models.Entry
    ).filter(
        models.Entry.id == id
    ).first()

    feed = g.db.query(
        models.Feed
    ).filter(
        models.Feed.id == entry.feed_id
    ).first()

    entry.status = 'read'
    g.db.add(entry)

    feed.unread -= 1
    g.db.add(feed)

    try:
        g.db.commit()
    except:
        g.db.rollback()
    else:
        return render_template('entry.html', entry=entry, feed=feed)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = forms.AddFeed(request.form)
    if request.method == 'POST' and form.validate():
        feed_data = feedparser.parse(form.feed_url.data)
        feed = models.Feed()
        feed.title = feed_data['feed']['title']
        feed.url = feed_data['feed']['link']
        feed.unread = len(feed_data['items'])
        feed.feed_url = form.feed_url.data
        g.db.add(feed)

        try:
            g.db.commit()
        except:
            g.db.rollback()
            raise
        else:
            return redirect(url_for('index'))
    return render_template('add_feed.html', form=form)


if __name__ == '__main__':
    app.run(
        debug=settings.DEBUG,
    )
