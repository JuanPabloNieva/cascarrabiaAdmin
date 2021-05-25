from flask import Blueprint, render_template, redirect, url_for, request, abort, flash, json, session, jsonify
from config import PROD_ACCESS_TOKEN
from mercadopago import SDK

sdk = SDK(PROD_ACCESS_TOKEN)

pay = Blueprint('pay', __name__, url_prefix='/api', template_folder='templates')

@pay.route('/pay', methods={'POST','GET'})
def create_preference_data():
    arreglo = json.loads(request.data)
    if len(arreglo) == 0:
        abort(500)

    preference_data = {
        "items": []
    }
    for a in arreglo:
        preference_data['items'].append({'title': a['nombre'], "quantity": a['cantidad'], "unit_price": a['precio']})
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    return jsonify(data=preference), 200