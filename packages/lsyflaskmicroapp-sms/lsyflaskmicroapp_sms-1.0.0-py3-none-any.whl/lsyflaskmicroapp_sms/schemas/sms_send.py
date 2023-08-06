# -*- coding: utf-8 -*-

from lsyflasksdkcore.schema import Schema, PagerQuerySchema
from lsyflasksdkcore.utils.unique import get_uuid_str
from marshmallow import fields, post_load, validate

from lsyflaskmicroapp_sms.entitys.sms_send import SmsSendBase, SmsSendEdit, SmsSendDetail, \
    SmsSendPagerQuery, SmsSendPerson


class SmsSendSchema(Schema):
    """ 短信通知|发件箱 Schema """
    # Id
    id = fields.Str(missing=get_uuid_str, validate=validate.Length(max=36), description="Id")
    # 消息ID
    message_id = fields.Str(required=True, validate=validate.Length(max=36), description="消息ID")
    # 接收号码
    receive_number = fields.Str(required=True, validate=validate.Length(max=15), description="接收号码")
    # 接收人
    receive_person = fields.Str(required=False, validate=validate.Length(max=20), allow_none=True,
                                description="接收人")
    # 发送时间
    send_date = fields.DateTime(required=False, allow_none=True, description="发送时间")
    # 发送次数
    send_count = fields.Int(required=True, validate=validate.Range(min=0, max=99), description="发送次数")
    # 发送状态
    send_state = fields.Int(required=True, validate=validate.Range(min=0, max=99), description="发送状态")
    # 发送状态说明
    send_state_desc = fields.Str(required=False, validate=validate.Length(max=100), allow_none=True,
                                 description="发送状态说明")

    @post_load
    def make(self, data, **kwargs):
        return SmsSendBase().__fill__(**data)


class SmsSendPersonSchema(Schema):
    """短信通知联系人"""
    # 接收号码
    receive_number = fields.Str(required=True, validate=validate.Length(max=15))
    # 接收人
    receive_person = fields.Str(required=True, validate=validate.Length(max=20))

    @post_load
    def make(self, data, **kwargs):
        return SmsSendPerson().__fill__(**data)


class SmsSendEditSchema(SmsSendSchema):

    @post_load
    def make(self, data, **kwargs):
        return SmsSendEdit().__fill__(**data)


class SmsSendDetailSchema(SmsSendSchema):

    @post_load
    def make(self, data, **kwargs):
        return SmsSendDetail().__fill__(**data)


class SmsSendPagerQuerySchema(PagerQuerySchema):
    id = fields.Str(required=False, allow_none=True)

    @post_load
    def make(self, data, **kwargs):
        return SmsSendPagerQuery().__fill__(**data)
