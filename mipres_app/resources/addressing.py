import requests
from flask import jsonify, request, current_app
from flask.views import MethodView

SWAGGER_ADDRESSING_SCHEMA = {
    '/addressing': {
        'post': {
            'operationId': 'addressing',
            'parameters': [
                {
                    'name': 'body',
                    'description': 'Addressing service',
                    'in': 'body',
                    'required': True,
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'startDate': {'type': 'string'},
                            'endDate': {'type': 'string'},
                        }
                    }
                }
            ],
            'responses': {
                '200': {'description': 'Successful operation'},
                '400': {'description': 'Missing parameter'},
            },
            'tags': ['Reports']
        }
    }
}


class AddressingView(MethodView):
    @staticmethod
    def post():
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        start_date = request.json.get('startDate', None)
        end_date = request.json.get('endDate', None)

        if not start_date or not end_date:
            return jsonify({"msg": "Missing parameter"}), 400

        # response_pres = AuthenticationView.generate_token(nit, token_pres)

        return jsonify(data=dict()), 200

    @staticmethod
    def generate_token(nit, token):
        response = requests.get('%s/generartoken/%s/%s' % (current_app.config.get('MIPRES_API'), nit, token))
        return ''.join(c for c in response.text if c not in '"')
