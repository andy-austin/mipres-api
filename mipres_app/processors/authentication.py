from flask_jwt_extended import jwt_required, jwt_optional


@jwt_required
def required_authentication(**kwargs):
    pass


@jwt_optional
def optional_authentication(**kwargs):
    pass
