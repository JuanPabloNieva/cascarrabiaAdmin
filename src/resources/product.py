from flask import Blueprint, render_template, redirect, url_for, request, abort, flash, json
from src.forms.productForm import ProductForm
from src.forms.productEditForm import ProductEditForm
from src.helpers.firebase import generate_url_image
from config import *

import requests
import json

prod = Blueprint('product', __name__, url_prefix='/products',
                 template_folder='templates')

# Guardar ruta de consulta en variable de entorno
url_get = "https://testapi-d2ef9-default-rtdb.firebaseio.com/products.json"
url_post = "https://testapi-d2ef9-default-rtdb.firebaseio.com/products.json"
url_categorias_get = "https://testapi-d2ef9-default-rtdb.firebaseio.com/categorias.json"


@prod.route('', methods={'GET', })
def index():
    req = requests.get(API_GET_ALL_PRODUCTS)

    if req.status_code == 200:
        products = req.json()
        return render_template('product/index.html', products=products)

    return abort(400)


@prod.route('/create', methods={'GET', 'POST'})
def create():
    categories = requests.get(API_GET_ALL_CATEGORIES).json()
    form = ProductForm()
    if categories:
        form.category.choices = [(categories[c]['nombre']) for c in categories]
    else:
        form.category.choices = []

    if form.validate_on_submit():
        url_img = generate_url_image(form.data['image'])

        product = {
            'nombre': (form.data['name']).strip(),
            'precio': form.data['price'],
            'categoria': form.data['category'],
            'url_imagen': url_img,
            'descripcion': (form.data['description']).strip()
        }

        try:
            req = requests.post(API_POST_PRODUCT, data=json.dumps(product))
            flash('¡Se ha creado un nuevo producto!')
        except():
            abort(500)

        return redirect(url_for('product.index'))
    return render_template('product/create.html', form=form)


@prod.route('/<string:id>/edit', methods=['GET', 'POST'])
def edit(id):
    product = requests.get(API_GET_PRODUCT.format(id))
    categories = requests.get(API_GET_ALL_CATEGORIES).json()
    form = ProductEditForm()
    if categories:
        form.category.choices = [(categories[c]['nombre']) for c in categories]
    else:
        form.category.choices = []

    if form.validate_on_submit():
        if form.data['image'].filename != '':
            url_img = generate_url_image(form.data['image'])
        else:
            url_img = product.json()['url_imagen']

        product = {
            'nombre': (form.data['name']).strip(),
            'precio': form.data['price'],
            'categoria': form.data['category'],
            'url_imagen': url_img,
            'descripcion': (form.data['description']).strip()
        }

        try:
            req = requests.put(API_PUT_PRODUCT.format(id), data=json.dumps(product))
            flash('¡Se ha editado el producto con éxito!')
        except():
            abort(500)
        return redirect(url_for('product.index'))

    form.name.data = product.json()['nombre']
    form.description.data = product.json()['descripcion']
    form.price.data = product.json()['precio']
    form.category.data = product.json()['categoria']
    return render_template('product/edit.html', form=form, product=id)


@prod.route('/<string:id>/delete', methods=['GET', 'DELETE'])
def delete(id):
    product = requests.get(API_GET_PRODUCT.format(id))

    if product.status_code == 200:
        return render_template('product/delete.html', product=product.json(), id=id)
    return flash('¡No existe el producto indicada!', 'error')


@prod.route('/<string:id>/confirm_delete', methods=['GET', 'DELETE'])
def confirm_delete(id):
    product = requests.get(API_GET_PRODUCT.format(id))

    if product.status_code == 200:
        requests.delete(API_DELETE_PRODUCT.format(id))
        flash('¡La eliminación ha sido exitosa!')
        return redirect(url_for('product.index'))
    return flash('¡No existe el producto indicada!', 'error')


@prod.route('/<string:id>/details', methods=['GET', ])
def details(id):
    product = requests.get(API_GET_PRODUCT.format(id)).json()

    return render_template('product/detail.html', product=product)
