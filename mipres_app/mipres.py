# -*- coding: utf-8 -*-
import os.path as op
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

root_path = op.join(op.dirname(__file__), '../')

app = Flask('mipresApi', root_path=root_path)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://sa:Rabbit99@localhost/mipresApi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '95C84B76351B248ECB7EA58319BA6'
app.config['MIPRES_API'] = "https://wsmipres.sispro.gov.co/WSSUMMIPRESNOPBS/Api"

db_session = SQLAlchemy(app)


def create_app(debug=False):
    from mipres_app.blueprints.api.blueprint import blueprint_api

    app.debug = debug

    Migrate(app, db_session)
    JWTManager(app)
    CORS(app)

    app.register_blueprint(blueprint_api, db_session=db_session, url_prefix='/api')

    return app
