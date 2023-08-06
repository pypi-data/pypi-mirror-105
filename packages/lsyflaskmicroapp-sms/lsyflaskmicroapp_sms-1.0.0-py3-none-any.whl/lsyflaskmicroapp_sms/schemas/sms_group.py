# -*- coding: utf-8 -*-

from lsyflasksdkcore.schema import Schema, PagerQuerySchema
from lsyflasksdkcore.utils.unique import get_uuid_str
from marshmallow import fields, post_load, validate

from lsyflaskmicroapp_sms.entitys.sms_group import SmsGroupBase, SmsGroupEdit, SmsGroupDetail, SmsGroupPagerQuery


class SmsGroupSchema(Schema):
    """ 短信通知|群组管理 Schema """
    # Id
    id = fields.Str(missing=get_uuid_str, validate=validate.Length(max=36), description="id")
    # 名称
    name = fields.Str(required=True, validate=validate.Length(max=20), description="名称")
    # 职责
    duty = fields.Str(required=False, validate=validate.Length(max=100), allow_none=True, description="职责")
    # 备注
    remark = fields.Str(required=False, validate=validate.Length(max=200), allow_none=True, description="备注")

    @post_load
    def make(self, data, **kwargs):
        return SmsGroupBase().__fill__(**data)


class SmsGroupEditSchema(SmsGroupSchema):

    @post_load
    def make(self, data, **kwargs):
        return SmsGroupEdit().__fill__(**data)


class SmsGroupDetailSchema(SmsGroupSchema):

    @post_load
    def make(self, data, **kwargs):
        return SmsGroupDetail().__fill__(**data)


class SmsGroupPagerQuerySchema(PagerQuerySchema):
    name = fields.Str()

    @post_load
    def make(self, data, **kwargs):
        return SmsGroupPagerQuery().__fill__(**data)
