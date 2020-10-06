from mipres_app.mipres import db_session
from datetime import datetime, timedelta
from flask_mongoalchemy import BaseQuery
from mipres_app.models.addressing import Addressing
from mipres_app.models.base_meta import BaseMeta


class AddressingMetaQuery(BaseQuery):
    def get_by_date(self, date):
        end = date.replace(hour=23, minute=59)
        return self.filter(self.type.document_date >= date, self.type.document_date <= end)


class AddressingMeta(BaseMeta):
    query_class = AddressingMetaQuery

    exec_date = db_session.DateTimeField()
    document_date = db_session.DateTimeField()
    observation = db_session.StringField()
    docs_amount = db_session.IntField()
    entities = db_session.ListField(db_session.IntField())

    @staticmethod
    def save_document(start_date, response, docs_amount):
        entities = []
        for entity in response:
            entities.append(Addressing.save_document(entity))

        meta = AddressingMeta(
            exec_date=datetime.utcnow(),
            document_date=start_date,
            observation='Descargado' if docs_amount > 0 else 'Dia vacio',
            docs_amount=docs_amount,
            entities=entities,
        )
        meta.save()

    @staticmethod
    def handle(identity, start_date, end_date, retrieve_addressing):
        delta = timedelta(days=1)
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end_date - start_date).days

        while start_date <= end_date:
            nit = identity.get('nit')
            days_left = (end_date - start_date).days

            BaseMeta.socketio_emit('addressing', days_left, days, nit)

            if AddressingMeta.query.get_by_date(start_date).first() is None:
                response = retrieve_addressing(nit, identity.get('token_pres'), start_date.strftime("%Y-%m-%d"))
                AddressingMeta.save_document(start_date, response, len(response))

            start_date += delta
