import requests
from flaskthreads import AppContextThread

from flask import jsonify, request, current_app
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from mipres_app.models.addressing import Addressing
from mipres_app.models.addressing_meta import AddressingMeta

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
    start_date = None
    end_date = None

    def dispatch_request(self, *args, **kwargs):
        data = request.json if request.json else request.args
        self.start_date = data.get('startDate', None)
        self.end_date = data.get('endDate', None)

        if not self.start_date or not self.end_date:
            return jsonify({"msg": "Missing parameter"}), 400

        return super(AddressingView, self).dispatch_request(*args, **kwargs)

    @jwt_required
    def get(self):
        documents = Addressing.query.get_by_date_range(self.start_date, self.end_date).all()
        return jsonify(documents), 200

    @jwt_required
    def post(self):
        thread = AppContextThread(
            target=AddressingMeta.handle,
            args=(get_jwt_identity(), self.start_date, self.end_date, self.retrieve_addressing)
        )
        thread.start()

        return jsonify(message='Thread started'), 200

    @staticmethod
    def retrieve_addressing(nit, token, date):
        response = requests.get(
            '%s/DireccionamientoXFecha/%s/%s/%s' % (current_app.config.get('MIPRES_API'), nit, token, date)
        )
        return response.json()
