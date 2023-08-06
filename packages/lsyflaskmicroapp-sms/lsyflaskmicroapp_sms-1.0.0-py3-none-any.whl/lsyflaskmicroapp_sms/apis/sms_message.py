# -*- coding: utf-8 -*-

"""
SMS_Message
~~~~~~~~~~~~~
短信通知|短信内容
"""
import logging
from datetime import datetime

from flask_login import current_user
from lsyflasksdkcore import RequestQuery, eresponse, sresponse, PkQuerySchema
from lsyflasksdkcore.blueprints import Blueprint
from lsyflasksdkcore.exceptions import DBRefError
from lsyflasksdkcore.schema import PksQuerySchema, PksQuery, PkQuery
from lsyflasksdkcore.utils.unique import get_uuid_str
from werkzeug.exceptions import InternalServerError

from lsyflaskmicroapp_sms.entitys.sms_message import SmsMessagePagerQuery, SmsMessageEdit
from lsyflaskmicroapp_sms.entitys.sms_send import SmsSendBase
from lsyflaskmicroapp_sms.models import create_sms_message_model, create_sms_group_model, create_sms_person_model
from lsyflaskmicroapp_sms.schemas.sms_message import SmsMessagePagerQuerySchema, SmsMessageEditSchema

logger = logging.getLogger(__name__)

bp = Blueprint('sms_message', __name__)


@bp.route('/page', methods=['GET', 'POST'])
@bp.auth.grant_view
def page():
    try:
        query = RequestQuery(SmsMessagePagerQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: SmsMessagePagerQuery = query.data

        model = create_sms_message_model()
        dbr, count = model.get_page_query("", qd.rows, qd.offset)
        return sresponse(dbr.json, total=count)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/add', methods=['POST'])
def add():
    try:
        query = RequestQuery(SmsMessageEditSchema, cover={"send_person": current_user.user_name})
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: SmsMessageEdit = query.data
        entity.record_date = datetime.now()
        entity.id = get_uuid_str()

        send_list = []
        for item in entity.sms_send:
            sms_send = SmsSendBase()
            sms_send.id = get_uuid_str()
            sms_send.message_id = entity.id
            sms_send.receive_number = item.receive_number
            sms_send.receive_person = item.receive_person
            sms_send.send_count = len(entity.sms_send)
            sms_send.send_date = datetime.now()
            sms_send.send_state = 0
            sms_send.send_state_desc = ""
            send_list.append(sms_send)

        model = create_sms_message_model()
        model.add(entity, send_list)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/modify', methods=['POST'])
@bp.auth.grant_edit
def modify():
    try:
        query = RequestQuery(SmsMessageEditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: SmsMessageEdit = query.data
        model = create_sms_message_model()
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
        model = create_sms_message_model()
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
        model = create_sms_message_model()
        data = model.get_detail(qd.id).json
        return sresponse(data)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/tree_all', methods=['POST'])
def tree_all():
    try:
        # 分组数据
        model = create_sms_group_model()
        lst = model.get_all(sort="name", order="asc").json

        # 人员数据
        person_model = create_sms_person_model()
        person_lst = person_model.get_all().json

        result = []
        no_group_person_lst = [p for p in person_lst if p['group_id'] is None]
        if no_group_person_lst:
            result.append({"id": "**", "name": "未分组联系人", "count": len(no_group_person_lst),
                           "member": no_group_person_lst})

        for g in lst:
            group_person_lst = [p for p in person_lst if p['group_id'] == g['id']]
            g['member'] = group_person_lst
        lst += result
        return sresponse(lst)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()
