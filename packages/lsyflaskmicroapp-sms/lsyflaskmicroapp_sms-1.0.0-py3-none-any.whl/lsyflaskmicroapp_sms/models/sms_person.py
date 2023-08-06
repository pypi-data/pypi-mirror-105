# -*- coding: utf-8 -*-


from typing import List, Tuple

from lsyflasksdkcore.exceptions import DBError
from lsyflasksdkcore.model import DBResult
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from lsyflaskmicroapp_sms.entitys.sms_person import SmsPersonBase, SmsPersonEdit, SmsPersonDetail
from lsyflaskmicroapp_sms.orm import db, model, SmsPerson, SmsGroup
from lsyflaskmicroapp_sms.schemas.sms_person import SmsPersonSchema, SmsPersonDetailSchema


class SmsPersonModel(object):
    """ 短信通知|人员信息表 Model
    """
    columns = [SmsPerson.id, SmsPerson.name, SmsPerson.group_id, SmsPerson.company, SmsPerson.duties, SmsPerson.is_head,
               SmsPerson.phone_number, SmsPerson.email, SmsPerson.remark]

    def __init__(self):
        self.session = db.session
        """:type: sqlalchemy.orm.Session"""

    @staticmethod
    def _get_sorted(sort: str, order: str):
        if sort and order:
            return getattr(getattr(SmsPerson, sort), order)()
        return None

    @model.entity(SmsPersonSchema)
    def get_one(self, _id: str) -> DBResult[SmsPersonBase]:
        try:
            return self.session.query(SmsPerson).filter(SmsPerson.id == _id).first()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_one error,error:{ex}")

    @model.list(SmsPersonSchema)
    def get_all(self, sort: str = None, order: str = None) -> DBResult[SmsPersonBase]:
        try:
            q = self.session.query(SmsPerson)
            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                q = q.order_by(_sorted)
            return q.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_all error,error:{ex}")

    @model.list(SmsPersonSchema)
    def get_list_group_id(self, group_id: str, sort=None, order=None) -> DBResult[SmsPersonBase]:
        try:
            query = self.session.query(SmsPerson).filter(SmsPerson.group_id == group_id)
            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                query = query.order_by(_sorted)
            return query.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_list_group_id error,error:{ex}")

    def add(self, entity: SmsPersonEdit):
        try:
            schema = SmsPersonSchema()
            d = schema.dump(entity)
            row = SmsPerson(**d)
            self.session.add(row)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"add validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"add error,error:{ex}")

    def modify(self, _id: str, entity: SmsPersonEdit):
        try:
            schema = SmsPersonSchema()
            d = schema.dump(entity)
            self.session.query(SmsPerson).filter(SmsPerson.id == _id).update(d)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"modify validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"modify error,error:{ex}")

    def delete(self, _id: str):
        try:
            self.session.query(SmsPerson).filter(SmsPerson.id == _id).delete()
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete error,error:{ex}")

    def delete_group_id(self, group_id: str):
        try:
            self.session.query(SmsPerson).filter(SmsPerson.group_id == group_id).delete()
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete_group_id error,error:{ex}")

    def tran_import(self, lst: List[SmsPersonBase]):
        try:
            for entity in lst:
                schema = SmsPersonSchema()
                d = schema.dump(entity)
                row = SmsPerson(**d)
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
            self.session.query(SmsPerson).filter(
                SmsPerson.id.in_(pks)).delete(synchronize_session=False)
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_delete error,error:{ex}")

    @model.pager(SmsPersonDetailSchema)
    def get_page_query(self, group_id, name, company, is_head, phone_number,
                       limit: int, offset: int) -> Tuple[DBResult[SmsPersonDetail], int]:
        try:
            columns = self.columns
            q = self.session.query(*columns, SmsGroup.name.label("group_id_name")) \
                .select_from(SmsPerson) \
                .outerjoin(SmsGroup, SmsGroup.id == SmsPerson.group_id). \
                filter(SmsPerson.name.contains(name))

            if group_id == "**":
                q = q.filter(SmsPerson.group_id.is_(None))
            elif group_id != "*":
                q = q.filter(SmsGroup.id == group_id)
            if is_head != "*":
                q = q.filter(SmsPerson.is_head == is_head)

            rows = None
            count = q.count()
            if count > 0:
                q = q.order_by(SmsPerson.name.asc())
                rows = q.limit(limit).offset(offset).all()
            return rows, count
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_page_query error,error:{ex}")

    def tran_modify_group(self, group_id, person_ids):
        try:
            self.session.query(SmsPerson). \
                filter(SmsPerson.id.in_(person_ids)). \
                update({"group_id": group_id}, synchronize_session=False)
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_modify_group error,error:{ex}")
