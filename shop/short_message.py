#-*- coding:utf-8 -*-
# author:Administrator
# datetime:2019/8/28 14:01
# software: PyCharm
from django.shortcuts import HttpResponse as resp
from . import models
import json
import random
import re
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

def msg_code_make(request):
    username = request.POST.get('username')
    pattern = r'^1[3456789]\d{9}$'
    if re.match(pattern,username):
        msg_code = ''
        for i in range(4):
            jj = str(random.randint(0, 9))
            msg_code = msg_code+jj
            request.session['msgcode_info'] = {"username":username,"msg_code":msg_code}

        # 短信应用 SDK AppID
        appid = 1400253831  # SDK AppID 以1400开头
        # 短信应用 SDK AppKey
        appkey = "d26fff7bf4302e7661df631bd550f0d8"
        # 需要发送短信的手机号码
        phone_numbers = [username, ]
        # 短信模板ID，需要在短信控制台中申请
        template_id = 411677  # NOTE: 这里的模板 ID`7839`只是示例，真实的模板 ID 需要在短信控制台中申请
        # 签名
        sms_sign = "LazyGuys.cn"  # NOTE: 签名参数使用的是`签名内容`，而不是`签名ID`。这里的签名"腾讯云"只是示例，真实的签名需要在短信控制台中申请
        ssender = SmsSingleSender(appid, appkey)
        params = [msg_code]  # 当模板没有参数时，`params = []`
        try:
          result = ssender.send_with_param(86, phone_numbers[0],
              template_id, params, sign=sms_sign, extend="", ext="")
          msg = {"status": True}
        except HTTPError as e:
          print(e)
          msg = {"status": False, "tips": "网络错误!"}
        except Exception as e:
          print(e)
          msg = {"status": False, "tips": "网络错误!"}

    else:
        print('手机号不符合正则')
        msg = {"status":False,"tips":"手机号不正确!"}
    return resp(json.dumps(msg))


def msg_code_verify(request):
    username = request.POST.get('phone_f2')
    msg_code = request.POST.get('verifycode')
    if 'msgcode_info' in request.session.keys():
        msgcode_info = request.session['msgcode_info']

        if username == msgcode_info["username"] and msg_code == msgcode_info["msg_code"]:
            re = models.User.objects.filter(username=username)
            if re:
                request.session['user_info'] = {"username": re[0].username,
                                                "nickname": re[0].nickname,
                                                "info": re[0].info,
                                                }
                msg = {"status":True}
                pass
            else:
                msg = {"status":True,"tips":"用户名不是会员!请先注册"}
            pass
        else:
            msg = {"status":False,"tips":"验证码或手机号错误!"}
    else:
        msg = {"status": False, "tips": "请点击发送短信验证码!"}
    return resp(json.dumps(msg))