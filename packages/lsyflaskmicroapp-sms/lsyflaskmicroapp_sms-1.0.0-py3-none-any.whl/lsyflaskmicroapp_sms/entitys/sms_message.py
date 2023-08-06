# -*- coding: utf-8 -*-
from typing import List

from lsyflasksdkcore import AutoClass, PagerQuery

from lsyflaskmicroapp_sms.entitys.sms_send import SmsSendPerson


class SmsMessageBase(AutoClass):
    """短信通知|短信内容"""

    def __init__(self):
        # Id
        self.id = ""
        # 消息发送媒介
        self.send_media = None
        # 消息主题
        self.msg_title = ""
        # 消息内容
        self.msg_content = ""
        # 消息签名
        self.msg_sign = ""
        # 消息类型
        self.msg_type = None
        # 必须回复
        self.must_respond = None
        # 重发次数
        self.again_send_count = None
        # 记录时间
        self.record_date = None
        # 发送人
        self.send_person = ""


class SmsMessageList(SmsMessageBase):
    def __init__(self):
        super().__init__()
        self.send_count = None
        self.send_success = None


class SmsMessageEdit(SmsMessageBase):
    def __init__(self):
        super().__init__()
        self.sms_send: List[SmsSendPerson] = []


class SmsMessageDetail(SmsMessageBase):
    pass


class SmsMessagePagerQuery(PagerQuery):
    pass
