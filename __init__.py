from flask import Blueprint
from flask import jsonify, request
from app import app
from app.managers import CryptoManager

api = Blueprint('api', __name__)


@api.route('/')
def hello():
    return 'Hello, World from API! change runtime'


@api.route('/cryptos', methods=['GET', 'POST'])
def cryptos_data():
    if request.method == 'GET':
        ret = CryptoManager.get_all_cryptocurrencies()
        return jsonify(ret)
    elif request.method == 'POST':
        if request.is_json:
            json_data = request.get_json()
            cm = CryptoManager(refreshed_data=json_data)
            cm.data_sync()

            response = {'status': 'success', 'message': 'Data Processed'}
            return jsonify(response)
        else:
            response = {'status': 'error', 'message': 'Invalid request'}
            return jsonify(response), 400


app.register_blueprint(api)

