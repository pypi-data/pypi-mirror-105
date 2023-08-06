# -*- coding: utf-8 -*-

from lsyflaskmicroapp_sms import orm
from lsyflaskmicroapp_sms.apis import sms_group
from lsyflaskmicroapp_sms.apis import sms_message
from lsyflaskmicroapp_sms.apis import sms_person
from lsyflaskmicroapp_sms.apis import sms_receive
from lsyflaskmicroapp_sms.apis import sms_send


def init_app(app):
    orm.init_db(app)

    # 短信通知|收件箱
    app.register_blueprint(sms_receive.bp, url_prefix='/api/sms/sms_receive')
    # 短信通知|发件箱
    app.register_blueprint(sms_send.bp, url_prefix='/api/sms/sms_send')
    # 短信通知|短信内容
    app.register_blueprint(sms_message.bp, url_prefix='/api/sms/sms_message')
    # 短信通知|群组管理
    app.register_blueprint(sms_group.bp, url_prefix='/api/sms/sms_group')
    # 短信通知|人员信息表
    app.register_blueprint(sms_person.bp, url_prefix='/api/sms/sms_person')


__all__ = ['init_app']
