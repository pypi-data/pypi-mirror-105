# -*- coding: utf-8 -*-

"""
SMS_Person
~~~~~~~~~~~~~
短信通知|人员信息表
"""

import logging

from lsyflasksdkcore import RequestQuery, eresponse, sresponse, PkQuerySchema
from lsyflasksdkcore.blueprints import Blueprint
from lsyflasksdkcore.schema import PksQuerySchema, PksQuery, PkQuery
from lsyflasksdkcore.utils.unique import get_uuid_str
from werkzeug.exceptions import InternalServerError

from lsyflaskmicroapp_sms.entitys.sms_person import SmsPersonPagerQuery, SmsPersonEdit, SmsPersonTranModifyGroup
from lsyflaskmicroapp_sms.models import create_sms_person_model
from lsyflaskmicroapp_sms.schemas.sms_person import SmsPersonPagerQuerySchema, SmsPersonEditSchema, \
    SmsPersonTranModifyGroupSchema

logger = logging.getLogger(__name__)

bp = Blueprint('sms_person', __name__)


@bp.route('/page', methods=['GET', 'POST'])
def page():
    try:
        query = RequestQuery(SmsPersonPagerQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: SmsPersonPagerQuery = query.data

        model = create_sms_person_model()
        dbr, count = model.get_page_query(qd.group_id, qd.name, qd.company, qd.is_head, qd.phone_number,
                                          qd.rows, qd.offset)
        return sresponse(dbr.json, total=count)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/add', methods=['POST'])
@bp.auth.grant_add
def add():
    try:
        query = RequestQuery(SmsPersonEditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: SmsPersonEdit = query.data
        entity.id = get_uuid_str()
        model = create_sms_person_model()
        model.add(entity)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/modify', methods=['POST'])
@bp.auth.grant_edit
def modify():
    try:
        query = RequestQuery(SmsPersonEditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: SmsPersonEdit = query.data
        model = create_sms_person_model()
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
        model = create_sms_person_model()
        model.tran_delete(qd.ids)
        return sresponse()
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
        model = create_sms_person_model()
        data = model.get_detail(qd.id).json
        return sresponse(data)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/tran_modify_group', methods=['POST'])
@bp.auth.grant_view
def tran_modify_group():
    try:
        query = RequestQuery(SmsPersonTranModifyGroupSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: SmsPersonTranModifyGroup = query.data
        model = create_sms_person_model()
        model.tran_modify_group(entity.group_id, entity.person_ids)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()
