from . import client
from database import Employees
from flask import jsonify, g
from ..utils import get_api_user



@client.route('/v1/employees', methods = ['POST','GET'])
@get_api_user
def employees():
    if request.method == 'POST':
        api_secret = request.form.get('secret')
        if api_secret:
            if g.user.verify_secret(api_secret):
                return jsonify('Success')

        return jsonify('failed'), 401

    workers = [{
    'first_name': x.first_name,
    'last_name': x.last_name,
    'email': x.email,
    } for x in Employees.query.all()]
    return jsonify(workers)

