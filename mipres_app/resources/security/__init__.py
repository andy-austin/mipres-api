from mipres_app.processors.authentication import required_authentication, optional_authentication

REQUIRE_AUTHENTICATION = dict(
    GET_COLLECTION=[required_authentication],
    GET_RESOURCE=[required_authentication],
    GET_RELATION=[required_authentication],
    GET_RELATED_RESOURCE=[required_authentication],
    DELETE_RESOURCE=[required_authentication],
    POST_RESOURCE=[required_authentication],
    PATCH_RESOURCE=[required_authentication],
    GET_RELATIONSHIP=[required_authentication],
    DELETE_RELATIONSHIP=[required_authentication],
    POST_RELATIONSHIP=[required_authentication],
    PATCH_RELATIONSHIP=[required_authentication]
)


def optional_post_authentication():
    REQUIRE_AUTHENTICATION.update({'POST_RESOURCE': [optional_authentication]})
    return REQUIRE_AUTHENTICATION
