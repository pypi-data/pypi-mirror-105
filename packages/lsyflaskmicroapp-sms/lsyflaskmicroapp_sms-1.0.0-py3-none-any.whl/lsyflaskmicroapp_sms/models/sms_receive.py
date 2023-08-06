# -*- coding: utf-8 -*-


from typing import List, Tuple

from lsyflasksdkcore.exceptions import DBError
from lsyflasksdkcore.model import DBResult
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from lsyflaskmicroapp_sms.entitys.sms_receive import SmsReceiveBase, SmsReceiveEdit
from lsyflaskmicroapp_sms.orm import db, model, SmsReceive
from lsyflaskmicroapp_sms.schemas.sms_receive import SmsReceiveSchema


class SmsReceiveModel(object):
    """ 短信通知|收件箱 Model
    """

    columns = [SmsReceive.id, SmsReceive.msg_content, SmsReceive.send_number, SmsReceive.receive_date]

    def __init__(self):
        self.session = db.session
        """:type: sqlalchemy.orm.Session"""

    @staticmethod
    def _get_sorted(sort: str, order: str):
        if sort and order:
            return getattr(getattr(SmsReceive, sort), order)()
        return None

    @model.entity(SmsReceiveSchema)
    def get_one(self, _id: str) -> DBResult[SmsReceiveBase]:
        try:
            return self.session.query(SmsReceive).filter(SmsReceive.id == _id).first()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_one error,error:{ex}")

    @model.list(SmsReceiveSchema)
    def get_all(self, sort: str = None, order: str = None) -> DBResult[SmsReceiveBase]:
        try:
            q = self.session.query(SmsReceive)
            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                q = q.order_by(_sorted)
            return q.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_all error,error:{ex}")

    def add(self, entity: SmsReceiveEdit):
        try:
            schema = SmsReceiveSchema()
            d = schema.dump(entity)
            row = SmsReceive(**d)
            self.session.add(row)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"add validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"add error,error:{ex}")

    def modify(self, _id: str, entity: SmsReceiveEdit):
        try:
            schema = SmsReceiveSchema()
            d = schema.dump(entity)
            self.session.query(SmsReceive).filter(SmsReceive.id == _id).update(d)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"modify validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"modify error,error:{ex}")

    def delete(self, _id: str):
        try:
            self.session.query(SmsReceive).filter(SmsReceive.id == _id).delete()
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete error,error:{ex}")

    def tran_import(self, lst: List[SmsReceiveBase]):
        try:
            for entity in lst:
                schema = SmsReceiveSchema()
                d = schema.dump(entity)
                row = SmsReceive(**d)
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
            self.session.query(SmsReceive).filter(
                SmsReceive.id.in_(pks)).delete(synchronize_session=False)
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_delete error,error:{ex}")

    @model.pager(SmsReceiveSchema)
    def get_page_query(self, query, _id, msg_content, send_number,
                       receive_date, limit: int, offset: int) -> Tuple[DBResult[SmsReceiveBase], int]:
        try:
            columns = self.columns
            q = self.session.query(*columns). \
                filter(SmsReceive.msg_content.contains(msg_content)). \
                filter(SmsReceive.send_number.contains(send_number))
            if id != '*':
                q = q.filter(SmsReceive.id == _id)

            rows = None
            count = q.count()
            if count > 0:
                rows = q.limit(limit).offset(offset).all()
            return rows, count
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_page_query error,error:{ex}")
