from flask import Blueprint
from flask_restless_swagger import SwagAPIManager as APIManager

from mipres_app.resources.addressing import AddressingView, SWAGGER_ADDRESSING_SCHEMA
from mipres_app.resources.security.authentication import AuthenticationView, SWAGGER_AUTHENTICATION_SCHEMA


class BlueprintAPI(Blueprint):
    CONTENT_TYPE = 'application/vnd.api+json'

    def register(self, app, options, first_registration=False):
        super(BlueprintAPI, self).register(app, options, first_registration)

        kwargs = {'host': '127.0.0.1:5000', 'produces': [self.CONTENT_TYPE], 'consumes': [self.CONTENT_TYPE]}
        db_session = options.get('db_session', None)

        api_manager = APIManager(app=app, session=db_session.session if db_session else None, url_prefix='/api')
        api_manager.swagger.update(**kwargs)

        url_prefix = options.get('url_prefix', '/api')
        paths = api_manager.swagger.get('paths', {})

        paths.update(SWAGGER_AUTHENTICATION_SCHEMA)
        app.add_url_rule('%s/login' % url_prefix, view_func=AuthenticationView.as_view('login'), methods=['POST'])

        paths.update(SWAGGER_ADDRESSING_SCHEMA)
        app.add_url_rule('%s/addressing' % url_prefix, view_func=AddressingView.as_view('addressing'), methods=['POST'])


blueprint_api = BlueprintAPI('blueprint_api', __name__)
