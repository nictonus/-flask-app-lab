from msilib.schema import PublishComponent
from wsgiref.validate import validator

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectMultipleField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField, DateTimeLocalField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, Length
from datetime import datetime as dt

# Список категорій, що використовується у випадаючому меню
CATEGORIES = [('tech', 'Tech'), ('science', 'Science'), ('lifestyle', 'Lifestyle')]

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(message="Обов'язкове поле"), Length(min=3, max=100)])
    content = TextAreaField("Content", render_kw={"rows": 5,  "cols": 40}, validators=[DataRequired()])
    tags = SelectMultipleField("Tags", coerce=int)  # Поле для вибору кількох тегів
    is_active = BooleanField("Active Post")
    publish_date = DateTimeLocalField('Publish Date', format="%Y-%m-%dT%H:%M", default=dt.now())
    category = SelectField("Category",
                           choices=CATEGORIES, validators=[DataRequired()])
    author_id = SelectField("Author", choices=[], coerce=int)
    submit = SubmitField("Submit")


