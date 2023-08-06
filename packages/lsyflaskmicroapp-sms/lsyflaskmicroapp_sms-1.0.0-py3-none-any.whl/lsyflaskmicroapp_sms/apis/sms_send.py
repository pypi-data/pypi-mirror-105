# -*- coding: utf-8 -*-

"""
SMS_Send
~~~~~~~~~~~~~
短信通知|发件箱
"""

import logging

from lsyflasksdkcore import RequestQuery, eresponse, sresponse, PkQuerySchema
from lsyflasksdkcore.blueprints import Blueprint
from lsyflasksdkcore.schema import PksQuerySchema, PksQuery, PkQuery
from lsyflasksdkcore.utils.unique import get_uuid_str
from werkzeug.exceptions import InternalServerError

from lsyflaskmicroapp_sms.entitys.sms_send import SmsSendPagerQuery, SmsSendEdit
from lsyflaskmicroapp_sms.models import create_sms_send_model
from lsyflaskmicroapp_sms.schemas.sms_send import SmsSendPagerQuerySchema, SmsSendEditSchema

logger = logging.getLogger(__name__)

bp = Blueprint('sms_send', __name__)


@bp.route('/page', methods=['GET', 'POST'])
@bp.auth.grant_view
def page():
    try:
        query = RequestQuery(SmsSendPagerQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: SmsSendPagerQuery = query.data

        model = create_sms_send_model()
        dbr, count = model.get_page_query("", qd.id, qd.rows, qd.offset)
        return sresponse(dbr.json, total=count)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/add', methods=['POST'])
@bp.auth.grant_add
def add():
    try:
        query = RequestQuery(SmsSendEditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: SmsSendEdit = query.data
        entity.id = get_uuid_str()
        model = create_sms_send_model()
        model.add(entity)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/modify', methods=['POST'])
@bp.auth.grant_edit
def modify():
    try:
        query = RequestQuery(SmsSendEditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: SmsSendEdit = query.data
        model = create_sms_send_model()
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
        model = create_sms_send_model()
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
        model = create_sms_send_model()
        data = model.get_detail(qd.id).data
        return sresponse(data)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()
