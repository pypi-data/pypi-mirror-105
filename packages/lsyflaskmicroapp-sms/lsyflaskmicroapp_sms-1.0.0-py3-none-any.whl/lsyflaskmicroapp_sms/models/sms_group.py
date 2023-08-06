# -*- coding: utf-8 -*-

from typing import List, Tuple

import sqlalchemy as sa
from lsyflasksdkcore.exceptions import DBError, DBRefError
from lsyflasksdkcore.model import DBRef, DBResult
from lsyflasksdkcore.schema import DBRefSchema
from marshmallow import ValidationError
from sqlalchemy import orm
from sqlalchemy.exc import SQLAlchemyError

from lsyflaskmicroapp_sms.entitys.sms_group import SmsGroupBase, SmsGroupEdit
from lsyflaskmicroapp_sms.orm import db, model, SmsGroup, SmsPerson
from lsyflaskmicroapp_sms.schemas.sms_group import SmsGroupSchema


class SmsGroupModel(object):
    """ 短信通知|群组管理 Model
    """

    columns = [SmsGroup.id, SmsGroup.name, SmsGroup.duty, SmsGroup.remark]

    def __init__(self):
        self.session = db.session
        """:type: sqlalchemy.orm.Session"""

    @staticmethod
    def _get_sorted(sort: str, order: str):
        if sort and order:
            return getattr(getattr(SmsGroup, sort), order)()
        return None

    @model.entity(SmsGroupSchema)
    def get_one(self, _id: str) -> DBResult[SmsGroupBase]:
        try:
            return self.session.query(SmsGroup).filter(SmsGroup.id == _id).first()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_one error,error:{ex}")

    @model.list(SmsGroupSchema)
    def get_all(self, sort: str = None, order: str = None) -> DBResult[SmsGroupBase]:
        try:
            q = self.session.query(SmsGroup)
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
            q_smsperson = self.session.query(sa.literal('SmsPerson').label('ref_code'),
                                             sa.literal(u'短信通知|人员信息表').label('ref_desc'),
                                             sa.func.count('*').label('ref_count')). \
                select_from(SmsPerson).filter(SmsPerson.group_id == _id)
            q = sa.union_all(q_smsperson)
            t = orm.aliased(q)
            rows = self.session.query(t).filter(t.c.ref_count > 0).all()
            return rows
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_refer error,error:{ex}")

    def add(self, entity: SmsGroupEdit):
        try:
            schema = SmsGroupSchema()
            d = schema.dump(entity)
            row = SmsGroup(**d)
            self.session.add(row)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"add validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"add error,error:{ex}")

    def modify(self, _id: str, entity: SmsGroupEdit):
        try:
            schema = SmsGroupSchema()
            d = schema.dump(entity)
            self.session.query(SmsGroup).filter(SmsGroup.id == _id).update(d)
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
            self.session.query(SmsGroup).filter(SmsGroup.id == _id).delete()
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete error,error:{ex}")

    def tran_import(self, lst: List[SmsGroupBase]):
        try:
            for entity in lst:
                schema = SmsGroupSchema()
                d = schema.dump(entity)
                row = SmsGroup(**d)
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
            self.session.query(SmsGroup).filter(
                SmsGroup.id.in_(pks)).delete(synchronize_session=False)
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_delete error,error:{ex}")

    @model.pager(SmsGroupSchema)
    def get_page_query(self, name, limit: int, offset: int) -> Tuple[DBResult[SmsGroupBase], int]:
        try:
            q = self.session.query(SmsGroup). \
                filter(SmsGroup.name.contains(name))
            rows = None
            count = q.count()
            if count > 0:
                q = q.order_by(SmsGroup.name.asc())
                rows = q.limit(limit).offset(offset).all()
            return rows, count
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_page_query error,error:{ex}")
