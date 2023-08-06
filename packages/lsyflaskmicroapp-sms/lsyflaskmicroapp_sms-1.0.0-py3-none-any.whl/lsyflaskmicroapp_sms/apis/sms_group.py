# -*- coding: utf-8 -*-

"""
SMS_Group
~~~~~~~~~~~~~
短信通知|群组管理
"""

import logging

from lsyflasksdkcore import RequestQuery, eresponse, sresponse, PkQuerySchema
from lsyflasksdkcore.blueprints import Blueprint
from lsyflasksdkcore.exceptions import DBRefError
from lsyflasksdkcore.schema import PksQuerySchema, PksQuery, PkQuery
from lsyflasksdkcore.utils.unique import get_uuid_str
from werkzeug.exceptions import InternalServerError

from lsyflaskmicroapp_sms.entitys.sms_group import SmsGroupPagerQuery, SmsGroupEdit
from lsyflaskmicroapp_sms.models import create_sms_group_model, create_sms_person_model
from lsyflaskmicroapp_sms.schemas.sms_group import SmsGroupPagerQuerySchema, SmsGroupEditSchema

logger = logging.getLogger(__name__)

bp = Blueprint('sms_group', __name__)


@bp.route('/page', methods=['POST'])
@bp.auth.grant_view
def page():
    try:
        query = RequestQuery(SmsGroupPagerQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: SmsGroupPagerQuery = query.data
        model = create_sms_group_model()
        dbr, count = model.get_page_query(qd.name, qd.rows, qd.offset)
        return sresponse(dbr.json, total=count)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/add', methods=['POST'])
@bp.auth.grant_add
def add():
    try:
        query = RequestQuery(SmsGroupEditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: SmsGroupEdit = query.data
        entity.id = get_uuid_str()
        model = create_sms_group_model()
        model.add(entity)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/modify', methods=['POST'])
@bp.auth.grant_edit
def modify():
    try:
        query = RequestQuery(SmsGroupEditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: SmsGroupEdit = query.data
        model = create_sms_group_model()
        model.modify(entity.id, entity)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/delete', methods=['POST'])
@bp.auth.grant_delete
def delete():
    try:
        query = RequestQuery(PksQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: PksQuery = query.data
        model = create_sms_group_model()
        model.tran_delete(qd.ids)
        return sresponse()
    except DBRefError as ex:
        return eresponse(ex.message)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/detail', methods=['POST'])
@bp.auth.grant_view
def detail():
    try:
        query = RequestQuery(PkQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: PkQuery = query.data
        model = create_sms_group_model()
        data = model.get_detail(qd.id).json
        return sresponse(data)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/all', methods=['POST'])
@bp.auth.grant_view
def get_all():
    try:
        model = create_sms_group_model()
        data = model.get_all(sort="name", order="asc").json
        return sresponse(data)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/tree_all', methods=['POST'])
@bp.auth.grant_view
def tree_all():
    try:
        # 分组数据
        model = create_sms_group_model()
        lst = model.get_all(sort="name", order="asc").data

        # 人员数据
        person_model = create_sms_person_model()
        person_lst = person_model.get_all().data

        result = []
        no_group_person_lst = [p for p in person_lst if p.group_id is None]
        if no_group_person_lst:
            result.append({"id": "**", "name": "未分组联系人", "count": len(no_group_person_lst)})

        for g in lst:
            group_person_lst = [p for p in person_lst if p.group_id == g.id]
            result.append({"id": g.id, "name": g.name, "count": len(group_person_lst)})
        return sresponse(result)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()
