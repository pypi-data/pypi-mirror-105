from flask_sqlalchemy import SQLAlchemy
from lsyflasksdkcore.model import Model
from sqlalchemy import Column, String, ForeignKey, DateTime, SmallInteger
from sqlalchemy.orm import relationship

db = SQLAlchemy()
model = Model()


def init_db(app):
    db.init_app(app)
    model.init_app(app)


class AuthUser(db.Model):
    __tablename__ = 'auth_user'

    id = Column(String, primary_key=True)
    user_name = Column(String(30), nullable=False)

    def __repr__(self):
        return '<AuthUser %r>' % self.user_name


class SmsPerson(db.Model):
    __tablename__ = 'sms_person'

    id = Column(String, primary_key=True)
    name = Column(String(20), nullable=False)
    group_id = Column(ForeignKey('sms_group.id'))
    company = Column(String(50))
    duties = Column(String(10))
    is_head = Column(SmallInteger)
    phone_number = Column(String(15), nullable=False)
    email = Column(String(20))
    remark = Column(String(200))

    group = relationship('SmsGroup')


class SmsSend(db.Model):
    __tablename__ = 'sms_send'

    id = Column(String, primary_key=True)
    message_id = Column(ForeignKey('sms_message.id'))
    receive_number = Column(String(15), nullable=False)
    receive_person = Column(String(20))
    send_date = Column(DateTime)
    send_count = Column(SmallInteger, nullable=False)
    send_state = Column(SmallInteger, nullable=False)
    send_state_desc = Column(String(100))

    message = relationship('SmsMessage')


class SmsGroup(db.Model):
    __tablename__ = 'sms_group'

    id = Column(String, primary_key=True)
    name = Column(String(20), nullable=False)
    duty = Column(String(100))
    remark = Column(String(200))


class SmsMessage(db.Model):
    __tablename__ = 'sms_message'

    id = Column(String, primary_key=True)
    send_media = Column(SmallInteger, nullable=False)
    msg_title = Column(String(20))
    msg_content = Column(String(500), nullable=False)
    msg_sign = Column(String(20))
    msg_type = Column(SmallInteger, nullable=False)
    must_respond = Column(SmallInteger, nullable=False)
    again_send_count = Column(SmallInteger, nullable=False)
    record_date = Column(DateTime, nullable=False)
    send_person = Column(String(20), nullable=False)


class SmsReceive(db.Model):
    __tablename__ = 'sms_receive'

    id = Column(String, primary_key=True)
    msg_content = Column(String(500), nullable=False)
    send_number = Column(String(50), nullable=False)
    receive_date = Column(DateTime, nullable=False)
