from flask import render_template, flash


def not_found_error(e):
    kwargs = {
        "error_name": "404 Not Found Error",
        "error_description": "La url a la que quiere acceder no existe",
    }
    return render_template("error.html", **kwargs), 404


def unauthorized_error(e):
    kwargs = {
        "error_name": "401 Unauthorized Error",
        "error_description": "No está autorizado para acceder a la url",
    }
    return render_template("error.html", **kwargs), 401

def method_not_allowed(e):
    kwargs = {
        "error_name": "405 Method Not Allowed",
        "error_description": "Método no permitido"
    }
    return render_template("error.html", **kwargs), 405

def internal_server_error(e):
    kwargs = {
        "error_name": "500 Internal Server Error",
        "error_description": "Ha ocurrido un problema en el servidor"
    }
    return render_template("error.html", **kwargs), 500

def load_errors(errors):
    for error_message in errors:
        flash(error_message, category="error")