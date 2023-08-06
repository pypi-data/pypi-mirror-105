# -*- coding: utf-8 -*-


def create_sms_receive_model():
    """ 短信通知|收件箱 Model
    :return:
    """
    from .sms_receive import SmsReceiveModel
    return SmsReceiveModel()


def create_sms_send_model():
    """ 短信通知|发件箱 Model
    :return:
    """
    from .sms_send import SmsSendModel
    return SmsSendModel()


def create_sms_message_model():
    """ 短信通知|短信内容 Model
    :return:
    """
    from .sms_message import SmsMessageModel
    return SmsMessageModel()


def create_sms_group_model():
    """ 短信通知|群组管理 Model
    :return:
    """
    from .sms_group import SmsGroupModel
    return SmsGroupModel()


def create_sms_person_model():
    """ 短信通知|人员信息表 Model
    :return:
    """
    from .sms_person import SmsPersonModel
    return SmsPersonModel()
