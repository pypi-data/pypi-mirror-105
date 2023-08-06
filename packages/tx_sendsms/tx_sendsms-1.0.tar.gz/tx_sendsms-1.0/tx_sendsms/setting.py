# coding:utf-8
"""
腾讯云短信SDK配置文件
"""
# 短信应用 SDK AppID
APPID = 1400519123  # SDK AppID 以1400开头,这里只是示例
# 短信应用 SDK AppKey
APPKEY = "bbf40a70aa864cf555cb322c1a88aec1"

# 短信模板ID，需要在短信控制台中申请
TEMPLATE_ID = 953485  # NOTE: 这里的模板 ID`953485` 只是示例，真实的模板 ID 需要在短信控制台中申请
# 签名
SMS_SIGN = "腾讯云"  # NOTE: 签名参数使用的是`签名内容`，而不是`签名ID`。这里的签名"腾讯云"只是示例，真实的签名需要在短信控制台中申请

# 验证码位数
CODE_SIZE = 4
