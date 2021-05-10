from flask import Blueprint, render_template, redirect, url_for, request, abort, flash, json, session
from src.forms.categoryForm import CategoryForm
from config import *
from src.helpers.auth import check_auth
import requests
import json

cat = Blueprint('category', __name__, url_prefix='/categories', template_folder='templates')

@cat.route('/', methods=['GET',])
def index():
    if not check_auth(session):
        abort(401)

    categories = requests.get(API_GET_ALL_CATEGORIES)

    if categories.status_code == 200:
        return render_template('categories/index.html', categories=categories.json())
    return abort(categories.status_code)


@cat.route('/create', methods=['GET', 'POST'])
def create():
    if not check_auth(session):
        abort(401)

    form = CategoryForm()
    if form.validate_on_submit():
        category = {
            "nombre": str.upper(form.name.data).strip()
        }

        res = requests.post(API_POST_CATEGORY, data=json.dumps(category))
        flash('¡Se ha creado una nueva categoría!')
        return redirect(url_for('category.index'))

    return render_template('categories/create.html', form=form)

@cat.route('/<string:id>/edit', methods=['GET', 'POST'])
def edit(id):
    if not check_auth(session):
        abort(401)

    form = CategoryForm()

    req = requests.get(API_GET_CATEGORY.format(id))
    if req.status_code == 200 and form.validate_on_submit(): 
        category = {
            "nombre": str.upper(form.name.data).strip()
        }
        requests.patch(API_PUT_CATEGORY.format(id), json.dumps(category))
        flash('¡Se ha editado el producto con éxito!')
        return redirect(url_for('category.index'))
    form.name.data = req.json()['nombre']
    return render_template('categories/edit.html', form=form, category=id)

@cat.route('/<string:id>/delete', methods=['GET', 'DELETE'])
def delete(id):
    if not check_auth(session):
        abort(401)

    category = requests.get(API_GET_CATEGORY.format(id))
    jso = category.json()
    if category.status_code == 200:
        return render_template('categories/delete.html', category=category.json(), id=id)
    return flash('¡No existe la categoria indicada!', 'error')

@cat.route('/<string:id>/confirm_delete', methods=['GET', 'DELETE'])
def confirm_delete(id):
    if not check_auth(session):
        abort(401)

    category = requests.get(API_GET_CATEGORY.format(id))
    prod = requests.get(API_GET_ALL_PRODUCTS).json()
    if prod:
        products = [(str.upper(prod[p]['categoria'])) for p in prod]
    else: 
        products = []
    try:
        if not category.json()['nombre'] in products:
            requests.delete(API_DELETE_CATEGORY.format(id))
            flash('¡La eliminación ha sido exitosa!') 
        else:
            raise RuntimeError
    except:
        flash('¡No se puede borrar esta categoria porque hay productos que pertenecen a ella!', 'error')

    return redirect(url_for('category.index'))