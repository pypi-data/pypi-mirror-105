# -*- coding: utf-8 -*-

from lsyflasksdkcore import AutoClass, PagerQuery


class SmsSendBase(AutoClass):
    """短信通知|发件箱"""

    def __init__(self):
        # Id
        self.id = ""
        # 消息ID
        self.message_id = ""
        # 接收号码
        self.receive_number = ""
        # 接收人
        self.receive_person = ""
        # 发送时间
        self.send_date = None
        # 发送次数
        self.send_count = None
        # 发送状态
        self.send_state = None
        # 发送状态说明
        self.send_state_desc = ""


class SmsSendPerson(AutoClass):
    """短信通知联系人"""

    def __init__(self):
        self.receive_number = ""
        self.receive_person = ""


class SmsSendEdit(SmsSendBase):
    pass


class SmsSendDetail(SmsSendBase):
    pass


class SmsSendPagerQuery(PagerQuery):
    def __init__(self):
        super().__init__()
        self.id = None
