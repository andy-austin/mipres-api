from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from mipres_app.mipres import scheduler

SWAGGER_ADDRESSING_SCHEDULER_SCHEMA = {
    '/addressing-scheduler': {
        'post': {
            'operationId': 'addressing-scheduler',
            'parameters': [
                {
                    'name': 'body',
                    'description': 'Addressing scheduler service',
                    'in': 'body',
                    'required': True,
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'interval': {'type': 'string'}
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
    }
}


def addressing_scheduler(text):
    print("printing %s" % text)


class AddressingSchedulerView(MethodView):
    job_id = 'addressing_scheduler'

    @jwt_required
    def post(self):
        data = request.json
        days = data.get('days', None)

        if not days or not isinstance(days, int):
            return jsonify({"msg": "Missing parameter"}), 400

        if scheduler.get_job(self.job_id) is not None:
            scheduler.remove_job(self.job_id)

        params = ['Hola Mundo']
        scheduler.add_job(self.job_id, func=addressing_scheduler, trigger='interval', seconds=days, args=params)
        # TODO: change seconds by days

        return jsonify(message='Scheduler started'), 200

    # @staticmethod
    # def retrieve_addressing(nit, token, date):
    #     response = requests.get(
    #         '%s/DireccionamientoXFecha/%s/%s/%s' % (current_app.config.get('MIPRES_API'), nit, token, date)
    #     )
    #     return response.json()
