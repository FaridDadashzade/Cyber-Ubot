from sqlalchemy import Column, String

from userbot.modules.sql_helper import BASE, SESSION


class ECHOSQL(BASE):
    __tablename__ = "echo_sql"
    user_id = Column(String(14), primary_key=True)
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, user_id, chat_id):
        self.user_id = str(user_id)
        self.chat_id = str(chat_id)


ECHOSQL.__table__.create(checkfirst=True)


def c_echo(user_id, chat_id):
    try:
        return SESSION.query(ECHOSQL).get((str(user_id), str(chat_id)))
    except BaseException:
        return None
    finally:
        SESSION.close()


def echosiyahisi():
    try:
        return SESSION.query(ECHOSQL).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def echoelave(user_id, chat_id):
    adder = ECHOSQL(str(user_id), str(chat_id))
    SESSION.add(adder)
    SESSION.commit()


def esil(user_id, chat_id):
    note = SESSION.query(ECHOSQL).get((str(user_id), str(chat_id)))
    if note:
        SESSION.delete(note)
        SESSION.commit()
