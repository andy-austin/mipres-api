import requests
from flask import jsonify, request, current_app
from flask.views import MethodView
from flask_jwt_extended import create_access_token

SWAGGER_AUTHENTICATION_SCHEMA = {
    '/login': {
        'post': {
            'operationId': 'login',
            'parameters': [
                {
                    'name': 'body',
                    'description': 'Authentication model',
                    'in': 'body',
                    'required': True,
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'nit': {'type': 'string'},
                            'token_pres': {'type': 'string'},
                            'token_prov': {'type': 'string'}
                        }
                    }
                }
            ],
            'responses': {
                '200': {'description': 'Successful login'},
                '400': {'description': 'Missing parameter'},
                '401': {'description': 'Bad credentials'},
            },
            'tags': ['Authentication']
        }
    }
}


class AuthenticationView(MethodView):
    @staticmethod
    def post():
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        nit = request.json.get('nit', None)
        token_pres = request.json.get('token_pres', None)
        token_prov = request.json.get('token_prov', None)

        if not nit or not token_pres or not token_prov:
            return jsonify({"msg": "Missing parameter"}), 400

        token_pre = AuthenticationView.generate_token(nit, token_pres)
        token_pro = AuthenticationView.generate_token(nit, token_prov)

        if 'Message' in token_pre or 'Message' in token_pro:
            return jsonify({"msg": "Bad credentials"}), 401

        identity = dict(nit=nit, token_pres=token_pre, token_prov=token_pro)

        return jsonify(access_token=create_access_token(identity=identity)), 200

    @staticmethod
    def generate_token(nit, token):
        response = requests.get('%s/generartoken/%s/%s' % (current_app.config.get('MIPRES_API'), nit, token))
        return ''.join(c for c in response.text if c not in '"')
