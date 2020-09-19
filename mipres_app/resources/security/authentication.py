from flask import jsonify, request
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
                            'token_prep': {'type': 'string'},
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
        token_prep = request.json.get('token_prep', None)
        token_prov = request.json.get('token_prov', None)

        if not nit or not token_prep or not token_prov:
            return jsonify({"msg": "Missing parameter"}), 400

        # TODO:

        return jsonify(access_token=create_access_token(identity="")), 200
