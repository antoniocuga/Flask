from wtforms import Form, TextField
from wtforms.validators import Required, URL


class AddFeed(Form):
    feed_url = TextField('Feed URL', validators=[
        Required('Campo requerido'),
        URL('URL incorrecta')
    ])
