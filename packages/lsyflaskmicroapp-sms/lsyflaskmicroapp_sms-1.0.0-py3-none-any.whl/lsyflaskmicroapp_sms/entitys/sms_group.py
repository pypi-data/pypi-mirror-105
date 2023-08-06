# -*- coding: utf-8 -*-

from lsyflasksdkcore import AutoClass, PagerQuery


class SmsGroupBase(AutoClass):
    """短信通知|群组管理"""

    def __init__(self):
        # Id
        self.id = ""
        # 名称
        self.name = ""
        # 职责
        self.duty = ""
        # 备注
        self.remark = ""


class SmsGroupEdit(SmsGroupBase):
    pass


class SmsGroupDetail(SmsGroupBase):
    pass


class SmsGroupPagerQuery(PagerQuery):
    def __init__(self):
        super().__init__()
        self.name = ""
