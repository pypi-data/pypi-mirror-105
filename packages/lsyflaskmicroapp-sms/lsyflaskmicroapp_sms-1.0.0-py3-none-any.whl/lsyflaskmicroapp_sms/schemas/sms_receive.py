# -*- coding: utf-8 -*-

from lsyflasksdkcore.schema import Schema, PagerQuerySchema
from lsyflasksdkcore.utils.unique import get_uuid_str
from marshmallow import fields, post_load, validate

from lsyflaskmicroapp_sms.entitys.sms_receive import SmsReceiveBase, SmsReceiveEdit, SmsReceiveDetail, \
    SmsReceivePagerQuery


class SmsReceiveSchema(Schema):
    """ 短信通知|收件箱 Schema """
    # Id
    id = fields.Str(missing=get_uuid_str, validate=validate.Length(max=36), description="Id")
    # 短信内容
    msg_content = fields.Str(required=True, validate=validate.Length(max=500), description="短信内容")
    # 发送号码
    send_number = fields.Str(required=True, validate=validate.Length(max=50), description="发送号码")
    # 接收时间
    receive_date = fields.DateTime(required=True, description="接收时间")

    @post_load
    def make(self, data, **kwargs):
        return SmsReceiveBase().__fill__(**data)


class SmsReceiveEditSchema(SmsReceiveSchema):

    @post_load
    def make(self, data, **kwargs):
        return SmsReceiveEdit().__fill__(**data)


class SmsReceiveDetailSchema(SmsReceiveSchema):

    @post_load
    def make(self, data, **kwargs):
        return SmsReceiveDetail().__fill__(**data)


class SmsReceivePagerQuerySchema(PagerQuerySchema):
    id = fields.Str(required=False, allow_none=True)
    msg_content = fields.Str(required=False, allow_none=True)
    receive_date = fields.DateTime(required=False, allow_none=True)
    send_number = fields.Int(required=False, allow_none=True)

    @post_load
    def make(self, data, **kwargs):
        return SmsReceivePagerQuery().__fill__(**data)
