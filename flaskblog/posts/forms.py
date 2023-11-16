from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired


class PostForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    # passing the render_kw which is like adding the keywords of html elements
    content = TextAreaField(
        "Content", validators=[InputRequired()], render_kw={"rows": "10"}
    )
    submit = SubmitField("Post")
