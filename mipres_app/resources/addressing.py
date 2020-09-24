import requests

from flask import jsonify, request, current_app
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from mipres_app.models.addressing import AddressingMeta

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
                '401': {'description': 'Missing Authorization Header'},
            },
            'tags': ['Reports']
        },
        'get': {
            'operationId': 'addressing',
            'parameters': [
                {
                    'name': 'startDate',
                    'description': 'Start date',
                    'in': 'query',
                    'required': True,
                    'schema': {
                        'type': 'string'
                    }
                },
                {
                    'name': 'endDate',
                    'description': 'End date',
                    'in': 'query',
                    'required': True,
                    'schema': {
                        'type': 'string'
                    }
                }
            ],
            'responses': {
                '200': {'description': 'Successful operation'},
                '401': {'description': 'Missing Authorization Header'},
            },
            'tags': ['Reports']
        }
    }
}


class AddressingView(MethodView):
    @staticmethod
    @jwt_required
    def get():
        start_date = request.args.get('startDate', None)
        end_date = request.args.get('endDate', None)

        documents = AddressingMeta.query.get_by_date_range(start_date, end_date).all()
        response = []
        for document in documents:
            response += document.entities

        return jsonify(response), 200

    @staticmethod
    @jwt_required
    def post():
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        start_date = request.json.get('startDate', None)
        end_date = request.json.get('endDate', None)

        if not start_date or not end_date:
            return jsonify({"msg": "Missing parameter"}), 400

        identity = get_jwt_identity()

        AddressingMeta.handle(identity, start_date, end_date, AddressingView.generate_token)

        return jsonify(message='Ok'), 200

    @staticmethod
    def generate_token(nit, token, date):
        response = requests.get(
            '%s/DireccionamientoXFecha/%s/%s/%s' % (current_app.config.get('MIPRES_API'), nit, token, date)
        )
        return response.json()
