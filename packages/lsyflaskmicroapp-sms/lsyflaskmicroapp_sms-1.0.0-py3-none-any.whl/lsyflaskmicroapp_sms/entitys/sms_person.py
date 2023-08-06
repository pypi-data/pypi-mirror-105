# -*- coding: utf-8 -*-

from lsyflasksdkcore import AutoClass, PagerQuery


class SmsPersonBase(AutoClass):
    """短信通知|人员信息表"""

    def __init__(self):
        # Id
        self.id = ""
        # 人员名称
        self.name = ""
        # 所属群组
        self.group_id = ""
        # 单位
        self.company = ""
        # 职务
        self.duties = ""
        # 是否负责人
        self.is_head = None
        # 手机号码
        self.phone_number = ""
        # 电子邮箱
        self.email = ""
        # 备注
        self.remark = ""


class SmsPersonEdit(SmsPersonBase):
    pass


class SmsPersonTranModifyGroup(AutoClass):
    def __init__(self):
        self.person_ids = []
        self.group_id = ""


class SmsPersonDetail(SmsPersonBase):
    def __init__(self):
        super().__init__()
        self.group_id_name = ""


class SmsPersonPagerQuery(PagerQuery):
    def __init__(self):
        super().__init__()
        self.group_id = "*"
        self.name = ""
        self.company = ""
        self.is_head = "*"
        self.phone_number = ""
