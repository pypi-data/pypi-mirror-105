# coding:utf-8
from distutils.core import setup

setup(
    name='tx_sendsms',  # 对 外 我 们 模 块 的 名 字
    version='1.0',  # 版 本 号
    description='简单的封装腾讯发送短信接口SDK2.0,相关配置在setting中设置',  # 描 述
    author='shawn',  # 作 者
    author_email='15979391664@163.com',
    url='https://gitee.com/wx_3d25ad0b9a/send_sms.git',
    py_modules=['tx_sendsms.send_sms', 'tx_sendsms.setting']  # 要发布的模块
)
