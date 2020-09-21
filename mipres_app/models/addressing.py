import json

from flask_mongoalchemy import BaseQuery
from mipres_app.mipres import db_session
from datetime import datetime, timedelta


class AddressingQuery(BaseQuery):
    def get_by_date_range(self, start_date, end_date):
        return self.filter(start_date >= self.type.document_date <= end_date)


class Addressing(db_session.Document):
    query_class = AddressingQuery

    exec_date = db_session.StringField()
    document_date = db_session.StringField()
    observation = db_session.StringField()
    response = db_session.StringField()
    docs_amount = db_session.IntField()

    def json(self):
        return dict(
            exec_date=self.exec_date,
            document_date=self.document_date,
            observation=self.observation,
            response=json.loads(self.response),
            docs_amount=self.docs_amount
        )

    @staticmethod
    def save_document(start_date, response, docs_amount):
        entity = Addressing(
            exec_date=datetime.utcnow().strftime('%Y-%m-%d'),
            document_date=start_date.strftime("%Y-%m-%d"),
            observation='Descargado' if docs_amount > 0 else 'Dia vacio',
            response=json.dumps(response),
            docs_amount=docs_amount
        )
        entity.save()

    @staticmethod
    def handle(identity, start_date, end_date, generate_token):
        delta = timedelta(days=1)
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        while start_date <= end_date:
            response = generate_token(identity.get('nit'), identity.get('token_pres'), start_date.strftime("%Y-%m-%d"))
            Addressing.save_document(start_date, response, len(response))
            start_date += delta
