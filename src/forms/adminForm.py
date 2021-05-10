from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import email, length, DataRequired


class AdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('El email es obligatorio'), length(
        1, 50, 'El email debe contener entre 1 y 50 caracteres'), email('Email inválido')])

    password = PasswordField('Contraseña', validators=[DataRequired(
        'La contraseña es obligatoria'), length(5, -1, 'La contraseña debe tener como mínimo 5 caracteres')])
