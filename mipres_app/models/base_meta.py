from mipres_app.mipres import socketio
from mipres_app.mipres import db_session


class BaseMeta(db_session.Document):
    @staticmethod
    def socketio_emit(event, part, total, user):
        return socketio.emit(event, dict(percent=BaseMeta.percent(part, total), user=user))

    @staticmethod
    def percent(part, total):
        return round(100 - part * 100 / total)
