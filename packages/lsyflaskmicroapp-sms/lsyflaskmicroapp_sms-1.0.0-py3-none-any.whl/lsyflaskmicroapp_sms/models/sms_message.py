# -*- coding: utf-8 -*-

from typing import List, Tuple

import sqlalchemy as sa
from lsyflasksdkcore.exceptions import DBError, DBRefError
from lsyflasksdkcore.model import DBRef, DBResult
from lsyflasksdkcore.schema import DBRefSchema
from marshmallow import ValidationError
from sqlalchemy import orm
from sqlalchemy.exc import SQLAlchemyError

from lsyflaskmicroapp_sms.entitys.sms_message import SmsMessageBase, SmsMessageEdit
from lsyflaskmicroapp_sms.entitys.sms_send import SmsSendBase
from lsyflaskmicroapp_sms.orm import db, model, SmsMessage, SmsSend
from lsyflaskmicroapp_sms.schemas.sms_message import SmsMessageSchema, SmsMessageListSchema
from lsyflaskmicroapp_sms.schemas.sms_send import SmsSendSchema


class SmsMessageModel(object):
    """ 短信通知|短信内容 Model
    """

    columns = [SmsMessage.id, SmsMessage.send_media, SmsMessage.msg_title, SmsMessage.msg_content, SmsMessage.msg_sign,
               SmsMessage.msg_type, SmsMessage.must_respond, SmsMessage.again_send_count, SmsMessage.record_date,
               SmsMessage.send_person]

    def __init__(self):
        self.session = db.session
        """:type: sqlalchemy.orm.Session"""

    @staticmethod
    def _get_sorted(sort: str, order: str):
        if sort and order:
            return getattr(getattr(SmsMessage, sort), order)()
        return None

    @model.entity(SmsMessageSchema)
    def get_one(self, _id: str) -> DBResult[SmsMessageBase]:
        try:
            return self.session.query(SmsMessage).filter(SmsMessage.id == _id).first()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_one error,error:{ex}")

    @model.list(SmsMessageSchema)
    def get_all(self, sort: str = None, order: str = None) -> DBResult[SmsMessageBase]:
        try:
            q = self.session.query(SmsMessage)
            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                q = q.order_by(_sorted)
            return q.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_all error,error:{ex}")

    @model.list(DBRefSchema)
    def get_refer(self, _id: str) -> DBResult[DBRef]:
        try:
            q_smssend = self.session.query(sa.literal('SmsSend').label('ref_code'),
                                           sa.literal(u'短信通知|发件箱').label('ref_desc'),
                                           sa.func.count('*').label('ref_count')). \
                select_from(SmsSend).filter(SmsSend.message_id == _id)

            q = sa.union_all(q_smssend)
            t = orm.aliased(q)
            rows = self.session.query(t).filter(t.c.ref_count > 0).all()
            return rows
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_refer error,error:{ex}")

    def add(self, entity: SmsMessageEdit, sms_send_list: List[SmsSendBase]):
        try:
            schema = SmsMessageSchema()
            d = schema.dump(entity)
            row = SmsMessage(**d)
            self.session.add(row)

            for item in sms_send_list:
                send_schema = SmsSendSchema()
                d = send_schema.dump(item)
                row = SmsSend(**d)
                self.session.add(row)

            self.session.commit()
        except ValidationError as ex:
            self.session.rollback()
            raise DBError(f"add validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"add error,error:{ex}")

    def modify(self, _id: str, entity: SmsMessageEdit):
        try:
            schema = SmsMessageSchema()
            d = schema.dump(entity)
            self.session.query(SmsMessage).filter(SmsMessage.id == _id).update(d)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"modify validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"modify error,error:{ex}")

    def delete(self, _id: str):
        refs = self.get_refer(_id).to_list()
        if refs:
            raise DBRefError(refs.pop())
        try:
            self.session.query(SmsMessage).filter(SmsMessage.id == _id).delete()
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete error,error:{ex}")

    def tran_import(self, lst: List[SmsMessageBase]):
        try:
            for entity in lst:
                schema = SmsMessageSchema()
                d = schema.dump(entity)
                row = SmsMessage(**d)
                self.session.add(row)
            self.session.commit()
        except ValidationError as ex:
            self.session.rollback()
            raise DBError(f"tran_import validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_import error,error:{ex}")

    def tran_delete(self, pks: List[str]):
        for pk in pks:
            refs = self.get_refer(pk).to_list()
            if refs:
                raise DBRefError(refs.pop())

        try:
            self.session.query(SmsMessage).filter(
                SmsMessage.id.in_(pks)).delete(synchronize_session=False)
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_delete error,error:{ex}")

    @model.pager(SmsMessageListSchema)
    def get_page_query(self, query, limit: int, offset: int) -> Tuple[DBResult[SmsMessageBase], int]:
        try:
            # 短信发送次数
            q_send_count = self.session.query(sa.func.count(SmsSend.id)). \
                select_from(SmsSend). \
                filter(SmsSend.message_id == SmsMessage.id). \
                correlate(SmsMessage).as_scalar()

            # 短信发送状态
            q_send_success = self.session.query(sa.func.count(SmsSend.id)). \
                select_from(SmsSend). \
                filter(SmsSend.message_id == SmsMessage.id). \
                filter(SmsSend.send_state == 1). \
                correlate(SmsMessage).as_scalar()

            columns = self.columns
            q = self.session.query(*columns,
                                   q_send_count.label('send_count'), q_send_success.label('send_success')). \
                select_from(SmsMessage)

            rows = None
            count = q.count()
            if count > 0:
                rows = q.limit(limit).offset(offset).all()
            return rows, count
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_page_query error,error:{ex}")
