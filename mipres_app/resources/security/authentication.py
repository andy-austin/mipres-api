import requests
from flask import jsonify, request, current_app
from flask.views import MethodView

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

        response_pres = AuthenticationView.generate_token(nit, token_pres)
        response_prov = AuthenticationView.generate_token(nit, token_prov)

        return jsonify(temp_token_pres=response_pres, temp_token_prov=response_prov), 200

    @staticmethod
    def generate_token(nit, token):
        response = requests.get('%s/generartoken/%s/%s' % (current_app.config.get('MIPRES_API'), nit, token))
        return ''.join(c for c in response.text if c not in '"')
