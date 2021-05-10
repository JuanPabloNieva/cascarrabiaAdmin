from flask import abort, session, Flask, Blueprint, url_for, render_template, redirect, flash
from src.helpers.firebase import auth as aut
from src.forms.adminForm import AdminForm
from src.helpers.auth import check_auth

auth = Blueprint('auth', __name__, url_prefix='')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = AdminForm()

    if form.validate_on_submit():
        try:
            admin = aut.sign_in_with_email_and_password(form.data['email'], form.data['password'])
        except:
            flash('¡Contraseña o email inválido!')
            return redirect(url_for('auth.login'))
        session['user'] = admin['email']

        flash('¡Se inició sesión correctamente!')
        return redirect(url_for('product.index'))

    return render_template('authentication/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = AdminForm()

    if form.validate_on_submit():
        admin = aut.create_user_with_email_and_password(form.data['email'], form.data['password'])

        return redirect(url_for('auth.login'))

    return render_template('authentication/registrar.html', form=form)


@auth.route('/logout')
def logout():
    if not check_auth(session):
        abort(401)

    try:
        del session['user']
        session.clear()
    except:
        flash('El usuario ha cerrado sesión', 'error')
    return redirect(url_for('auth.login'))