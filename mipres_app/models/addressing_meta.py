from mipres_app.mipres import db_session
from datetime import datetime, timedelta

from mipres_app.models.addressing import Addressing


class AddressingMeta(db_session.Document):
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
    def handle(identity, start_date, end_date, generate_token):
        delta = timedelta(days=1)
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        while start_date <= end_date:
            response = generate_token(identity.get('nit'), identity.get('token_pres'), start_date.strftime("%Y-%m-%d"))
            AddressingMeta.save_document(start_date, response, len(response))
            start_date += delta
