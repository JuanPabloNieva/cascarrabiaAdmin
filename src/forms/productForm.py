from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, FloatField, SelectField, FileField
from wtforms.validators import DataRequired, Length


class ProductForm(FlaskForm):
    name = StringField('Nombre', validators=[
                       DataRequired('El nombre es obligatorio')])
    price = FloatField('Precio', validators=[
                       DataRequired('El precio es obligatorio')])
    description = StringField('Descripcion', validators=[
                              Length(-1, 100, 'La descripcion no puede tener una longitud mayor a 100 caracteres.')])
    category = SelectField('Categoria', validators=[
                           DataRequired('La categoría es obligatoria')], choices=[])
    image = FileField('Imagen', validators=[FileRequired('La imagen es obligatoria'), FileAllowed(
        ['jpg', 'png', 'jpeg'], 'Solo se aceptan formatos JPG, PNG y JPEG')])
