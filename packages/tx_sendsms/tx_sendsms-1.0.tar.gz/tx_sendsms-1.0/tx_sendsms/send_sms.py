# coding:utf-8
from qcloudsms_py import SmsSingleSender
from . import setting
import random


def get_code(count: int):
    """
    获取验证码
    :param count:验证码位数
    :return:验证码
    """
    code = ''
    for i in range(count):
        num = str(random.randint(0, 9))
        code += num
    return code


def send(phone: int):
    """

    发送短信
    :param phone:手机号
    :return:
    """
    code = get_code(setting.CODE_SIZE)
    sender = SmsSingleSender(setting.APPID, setting.APPKEY)
    try:
        result = sender.send_with_param(86, phone, setting.TEMPLATE_ID, [code, ], sign=setting.SMS_SIGN, extend="",
                                        ext="")
        if result.get('result') == 0:
            return True
        else:
            raise Exception('%s手机号，短信发送失败' % phone)
    except Exception as E:
        raise Exception(E)


