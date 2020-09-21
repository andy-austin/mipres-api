from flask.json import JSONEncoder
from mipres_app.models.addressing import Addressing


class JsonEncoder(JSONEncoder):

    def default(self, instance):
        if isinstance(instance, Addressing):
            return instance.json()
        return super(JsonEncoder, self).default(instance)
