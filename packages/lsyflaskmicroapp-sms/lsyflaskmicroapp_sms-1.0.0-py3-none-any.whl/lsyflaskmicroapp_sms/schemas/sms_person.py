# -*- coding: utf-8 -*-

from lsyflasksdkcore.schema import Schema, PagerQuerySchema
from lsyflasksdkcore.utils.unique import get_uuid_str
from marshmallow import fields, post_load, validate

from lsyflaskmicroapp_sms.entitys.sms_person import SmsPersonBase, SmsPersonEdit, SmsPersonDetail, \
    SmsPersonPagerQuery, SmsPersonTranModifyGroup


class SmsPersonSchema(Schema):
    """ 短信通知|人员信息表 Schema """
    # Id
    id = fields.Str(missing=get_uuid_str, validate=validate.Length(max=36), description="Id")
    # 人员名称
    name = fields.Str(required=True, validate=validate.Length(max=20), description="人员名称")
    # 所属群组
    group_id = fields.Str(required=False, validate=validate.Length(max=36), allow_none=True, description="所属群组")
    # 单位
    company = fields.Str(required=False, validate=validate.Length(max=50), allow_none=True, description="单位")
    # 职务
    duties = fields.Str(required=False, validate=validate.Length(max=10), allow_none=True, description="职务")
    # 是否负责人
    is_head = fields.Int(required=False, validate=validate.Range(min=0, max=99), allow_none=True, description="是否负责人")
    # 手机号码
    phone_number = fields.Str(required=True, validate=validate.Length(max=15), description="手机号码")
    # 电子邮箱
    email = fields.Str(required=False, validate=validate.Length(max=20), allow_none=True, description="电子邮箱")
    # 备注
    remark = fields.Str(required=False, validate=validate.Length(max=200), allow_none=True, description="备注")

    @post_load
    def make(self, data, **kwargs):
        return SmsPersonBase().__fill__(**data)


class SmsPersonEditSchema(SmsPersonSchema):

    @post_load
    def make(self, data, **kwargs):
        return SmsPersonEdit().__fill__(**data)


class SmsPersonTranModifyGroupSchema(Schema):
    """ 批量修改分组 """
    group_id = fields.Str(required=True, validate=validate.Length(max=36), description="分组ID")
    person_ids = fields.List(fields.Str(), required=True, description="人员ID列表")

    @post_load
    def make(self, data, **kwargs):
        return SmsPersonTranModifyGroup().__fill__(**data)


class SmsPersonDetailSchema(SmsPersonSchema):
    name = fields.Str(required=False)
    group_id_name = fields.Str(required=False, allow_none=True)

    @post_load
    def make(self, data, **kwargs):
        return SmsPersonDetail().__fill__(**data)


class SmsPersonPagerQuerySchema(PagerQuerySchema):
    # 所属群组
    group_id = fields.Str(required=False, description="所属群组")
    # 人员名称
    name = fields.Str(required=False, allow_none=True, description="人员名称")
    # 单位
    company = fields.Str(required=False, description="单位")
    # 是否负责人
    is_head = fields.Str(required=False, validate=validate.OneOf(("0", "1", "*")), description="是否负责人")
    # 手机号码
    phone_number = fields.Str(required=False, description="手机号码")

    @post_load
    def make(self, data, **kwargs):
        return SmsPersonPagerQuery().__fill__(**data)
