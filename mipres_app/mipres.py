# -*- coding: utf-8 -*-
import os.path as op
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mongoalchemy import MongoAlchemy
from flask_jwt_extended import decode_token

root_path = op.join(op.dirname(__file__), '../')

app = Flask('mipresApi', root_path=root_path)

app.config['MONGOALCHEMY_REPLICA_SET'] = None
app.config['JWT_SECRET_KEY'] = '95C84B76351B248ECB7EA58319BA6'
app.config['MIPRES_API'] = "https://wsmipres.sispro.gov.co/WSSUMMIPRESNOPBS/Api"

db_session = MongoAlchemy()


def create_app(debug=False):
    from mipres_app.blueprints.api.blueprint import blueprint_api
    from mipres_app.json import JsonEncoder

    app.debug = debug
    app.json_encoder = JsonEncoder

    JWTManager(app)
    CORS(app)

    @app.before_request
    def before_request_func():
        token = request.headers.get('Authorization')

        if token:
            decoded_token = decode_token(request.headers.get('Authorization').split('Bearer ')[1])
            nit = decoded_token.get('identity').get('nit')
            mongourl = '%s:%s@%s/%s?retryWrites=true&w=majority' % ('mipres', 'admin', 'm2.twsaq.mongodb.net', nit)
            app.config['MONGOALCHEMY_DATABASE'] = nit
            app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb+srv://%s' % mongourl
            db_session.init_app(app)

    app.register_blueprint(blueprint_api, db_session=db_session, url_prefix='/api')

    return app
