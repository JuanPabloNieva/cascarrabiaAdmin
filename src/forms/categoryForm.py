from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CategoryForm(FlaskForm):
    name = StringField('nombre', validators=[DataRequired('El nombre es obligatorio'), Length(
        1, 50, 'El nombre debe tener entre 1 y 50 caracteres')])
    