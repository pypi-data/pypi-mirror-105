# -*- coding: utf-8 -*-

"""
SMS_Receive
~~~~~~~~~~~~~
短信通知|收件箱
"""

import logging

from lsyflasksdkcore import RequestQuery, eresponse, sresponse, PkQuerySchema
from lsyflasksdkcore.blueprints import Blueprint
from lsyflasksdkcore.schema import PksQuerySchema, PksQuery, PkQuery
from lsyflasksdkcore.utils.unique import get_uuid_str
from werkzeug.exceptions import InternalServerError

from lsyflaskmicroapp_sms.entitys.sms_receive import SmsReceivePagerQuery, SmsReceiveEdit
from lsyflaskmicroapp_sms.models import create_sms_receive_model
from lsyflaskmicroapp_sms.schemas.sms_receive import SmsReceivePagerQuerySchema, SmsReceiveEditSchema

logger = logging.getLogger(__name__)

bp = Blueprint('sms_receive', __name__)


@bp.route('/page', methods=['GET', 'POST'])
@bp.auth.grant_view
def page():
    try:
        query = RequestQuery(SmsReceivePagerQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: SmsReceivePagerQuery = query.data

        model = create_sms_receive_model()
        dbr, count = model.get_page_query("", qd.id, qd.msg_content, qd.send_number,
                                          qd.receive_date, qd.rows, qd.offset)
        return sresponse(dbr.json, total=count)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/add', methods=['POST'])
@bp.auth.grant_add
def add():
    try:
        query = RequestQuery(SmsReceiveEditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: SmsReceiveEdit = query.data
        entity.id = get_uuid_str()
        model = create_sms_receive_model()
        model.add(entity)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/modify', methods=['POST'])
@bp.auth.grant_edit
def modify():
    try:
        query = RequestQuery(SmsReceiveEditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: SmsReceiveEdit = query.data
        model = create_sms_receive_model()
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
        model = create_sms_receive_model()
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
        model = create_sms_receive_model()
        data = model.get_detail(qd.id).json
        return sresponse(data)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()
