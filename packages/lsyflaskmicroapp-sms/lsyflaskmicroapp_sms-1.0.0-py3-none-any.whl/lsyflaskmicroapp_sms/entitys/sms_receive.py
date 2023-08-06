# -*- coding: utf-8 -*-

from lsyflasksdkcore import AutoClass, PagerQuery


class SmsReceiveBase(AutoClass):
    """短信通知|收件箱"""

    def __init__(self):
        # Id
        self.id = ""
        # 短信内容
        self.msg_content = ""
        # 发送号码
        self.send_number = ""
        # 接收时间
        self.receive_date = None


class SmsReceiveEdit(SmsReceiveBase):
    pass


class SmsReceiveDetail(SmsReceiveBase):
    pass


class SmsReceivePagerQuery(PagerQuery):
    def __init__(self):
        super().__init__()
        self.id = ''
        self.msg_content = ''
        self.receive_date = ''
        self.send_number = ''
