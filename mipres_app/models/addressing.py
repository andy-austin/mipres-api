from flask_mongoalchemy import BaseQuery
from mipres_app.mipres import db_session


class AddressingQuery(BaseQuery):
    def get_by_date_range(self, start_date, end_date):
        start = '%s 00:00' % start_date
        end = '%s 23:59' % end_date
        return self.filter(self.type.date >= start, self.type.date <= end)


class Addressing(db_session.Document):
    query_class = AddressingQuery
    config_extra_fields = 'ignore'

    date = db_session.StringField(db_field='FecDireccionamiento')

    @staticmethod
    def save_document(document):
        entity = Addressing(**document, date=document.get('FecDireccionamiento'))
        entity.save()
        return document.get('ID')

    def json(self):
        json = self.get_extra_fields()
        json.update({'FecDireccionamiento': self.date})
        return json
