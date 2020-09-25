# -*- coding: utf-8 -*-
import os.path as op
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mongoalchemy import MongoAlchemy

root_path = op.join(op.dirname(__file__), '../')

app = Flask('mipresApi', root_path=root_path)

app.config['MONGOALCHEMY_DATABASE'] = '900285194'
app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb+srv://%s:%s@%s/%s?retryWrites=true&w=majority' % (
    'mipres', 'admin', 'm2.twsaq.mongodb.net', '900285194'
)
app.config['MONGOALCHEMY_REPLICA_SET'] = None
app.config['JWT_SECRET_KEY'] = '95C84B76351B248ECB7EA58319BA6'
app.config['MIPRES_API'] = "https://wsmipres.sispro.gov.co/WSSUMMIPRESNOPBS/Api"

db_session = MongoAlchemy(app)


def create_app(debug=False):
    from mipres_app.blueprints.api.blueprint import blueprint_api
    from mipres_app.json import JsonEncoder

    app.debug = debug
    app.json_encoder = JsonEncoder

    JWTManager(app)
    CORS(app)

    app.register_blueprint(blueprint_api, db_session=db_session, url_prefix='/api')

    return app
