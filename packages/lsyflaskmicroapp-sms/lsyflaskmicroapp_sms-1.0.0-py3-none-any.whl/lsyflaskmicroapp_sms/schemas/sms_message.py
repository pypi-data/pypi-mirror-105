# -*- coding: utf-8 -*-

from lsyflasksdkcore.schema import Schema, PagerQuerySchema
from lsyflasksdkcore.utils.unique import get_uuid_str
from marshmallow import fields, post_load, validate

from lsyflaskmicroapp_sms.entitys.sms_message import SmsMessageBase, SmsMessageEdit, SmsMessageDetail, \
    SmsMessagePagerQuery, SmsMessageList
from lsyflaskmicroapp_sms.schemas.sms_send import SmsSendPersonSchema


class SmsMessageSchema(Schema):
    """ 短信通知|短信内容 Schema """
    # Id
    id = fields.Str(missing=get_uuid_str, validate=validate.Length(max=36), description="Id")
    # 消息发送媒介
    send_media = fields.Int(required=True, validate=validate.Range(min=0, max=99), description="消息发送媒介")
    # 消息主题
    msg_title = fields.Str(required=False, validate=validate.Length(max=20), allow_none=True, description="消息主题")
    # 消息内容
    msg_content = fields.Str(required=True, validate=validate.Length(max=500), description="消息内容")
    # 消息签名
    msg_sign = fields.Str(required=False, validate=validate.Length(max=20), allow_none=True, description="消息签名")
    # 消息类型
    msg_type = fields.Int(required=True, validate=validate.Range(min=0, max=99), description="消息类型")
    # 必须回复
    must_respond = fields.Int(required=True, validate=validate.Range(min=0, max=99), description="必须回复")
    # 重发次数
    again_send_count = fields.Int(required=True, validate=validate.Range(min=0, max=99), description="重发次数")
    # 记录时间
    record_date = fields.DateTime(missing=None, allow_none=True, description="记录时间")
    # 发送人
    send_person = fields.Str(required=True, validate=validate.Length(max=20), description="发送人")

    @post_load
    def make(self, data, **kwargs):
        return SmsMessageBase().__fill__(**data)


class SmsMessageListSchema(SmsMessageSchema):
    send_success = fields.Int(required=True)
    send_count = fields.Int(required=True)
    send_media = fields.Int(required=False, allow_none=True)
    msg_type = fields.Int(required=False, allow_none=True)
    again_send_count = fields.Int(required=False, allow_none=True)
    msg_content = fields.Str(required=False, allow_none=True)
    send_person = fields.Str(required=False, allow_none=True)
    must_respond = fields.Int(required=False, allow_none=True)
    record_date = fields.DateTime(allow_none=True)

    @post_load
    def make(self, data, **kwargs):
        return SmsMessageList().__fill__(**data)


class SmsMessageEditSchema(SmsMessageSchema):
    sms_send = fields.Nested(SmsSendPersonSchema, many=True)

    @post_load
    def make(self, data, **kwargs):
        return SmsMessageEdit().__fill__(**data)


class SmsMessageDetailSchema(SmsMessageSchema):

    @post_load
    def make(self, data, **kwargs):
        return SmsMessageDetail().__fill__(**data)


class SmsMessagePagerQuerySchema(PagerQuerySchema):

    @post_load
    def make(self, data, **kwargs):
        return SmsMessagePagerQuery().__fill__(**data)
