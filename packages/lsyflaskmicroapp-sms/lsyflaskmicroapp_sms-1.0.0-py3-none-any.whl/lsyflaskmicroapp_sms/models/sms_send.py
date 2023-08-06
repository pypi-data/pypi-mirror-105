# -*- coding: utf-8 -*-


from typing import List, Tuple

from lsyflasksdkcore.exceptions import DBError
from lsyflasksdkcore.model import DBResult
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from lsyflaskmicroapp_sms.entitys.sms_send import SmsSendBase, SmsSendEdit
from lsyflaskmicroapp_sms.orm import db, model, SmsSend, SmsMessage
from lsyflaskmicroapp_sms.schemas.sms_send import SmsSendSchema


class SmsSendModel(object):
    """ 短信通知|发件箱 Model
    """

    columns = [SmsSend.id, SmsSend.message_id, SmsSend.receive_number, SmsSend.receive_person, SmsSend.send_date,
               SmsSend.send_count, SmsSend.send_state, SmsSend.send_state_desc]

    def __init__(self):
        self.session = db.session
        """:type: sqlalchemy.orm.Session"""

    @staticmethod
    def _get_sorted(sort: str, order: str):
        if sort and order:
            return getattr(getattr(SmsSend, sort), order)()
        return None

    @model.entity(SmsSendSchema)
    def get_one(self, _id: str) -> DBResult[SmsSendBase]:
        try:
            return self.session.query(SmsSend).filter(SmsSend.id == _id).first()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_one error,error:{ex}")

    @model.list(SmsSendSchema)
    def get_all(self, sort: str = None, order: str = None) -> DBResult[SmsSendBase]:
        try:
            q = self.session.query(SmsSend)
            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                q = q.order_by(_sorted)
            return q.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_all error,error:{ex}")

    @model.list(SmsSendSchema)
    def get_list_message_id(self, message_id: str, sort=None, order=None) -> DBResult[SmsSendBase]:
        try:
            query = self.session.query(SmsSend).filter(SmsSend.message_id == message_id)
            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                query = query.order_by(_sorted)
            return query.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_list_message_id error,error:{ex}")

    def add(self, entity: SmsSendEdit):
        try:
            schema = SmsSendSchema()
            d = schema.dump(entity)
            row = SmsSend(**d)
            self.session.add(row)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"add validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"add error,error:{ex}")

    def modify(self, _id: str, entity: SmsSendEdit):
        try:
            schema = SmsSendSchema()
            d = schema.dump(entity)
            self.session.query(SmsSend).filter(SmsSend.id == _id).update(d)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"modify validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"modify error,error:{ex}")

    def delete(self, _id: str):
        try:
            self.session.query(SmsSend).filter(SmsSend.id == _id).delete()
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete error,error:{ex}")

    def delete_message_id(self, message_id: str):
        try:
            self.session.query(SmsSend).filter(SmsSend.message_id == message_id).delete()
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete_message_id error,error:{ex}")

    def tran_import(self, lst: List[SmsSendBase]):
        try:
            for entity in lst:
                schema = SmsSendSchema()
                d = schema.dump(entity)
                row = SmsSend(**d)
                self.session.add(row)
            self.session.commit()
        except ValidationError as ex:
            self.session.rollback()
            raise DBError(f"tran_import validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_import error,error:{ex}")

    def tran_delete(self, pks: List[str]):
        try:
            self.session.query(SmsSend).filter(
                SmsSend.id.in_(pks)).delete(synchronize_session=False)

            self.session.commit()
        except ValidationError as ex:
            self.session.rollback()
            raise DBError(f"tran_delete validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_delete error,error:{ex}")

    @model.pager(SmsSendSchema)
    def get_page_query(self, query, key, limit: int, offset: int) -> Tuple[DBResult[SmsSendBase], int]:
        try:
            columns = self.columns
            q = self.session.query(*columns). \
                select_from(SmsSend). \
                outerjoin(SmsMessage, SmsSend.message_id == SmsMessage.id)

            if key != '*':
                q = q.filter(SmsMessage.id == key)

            rows = None
            count = q.count()
            if count > 0:
                rows = q.limit(limit).offset(offset).all()
            return rows, count
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_page_query error,error:{ex}")
