#-*- coding:utf-8 -*-
# author:王雨涵&&王磊
# datetime:2019/8/12 12:36
# software: PyCharm
from django.shortcuts import render,HttpResponse as resp,redirect
from . import models
from . import tools
import json
# 登录操作
def produce_code(request):
    imgdata,code = tools.produce_code(130,50)
    request.session['keep_code'] = code
    return resp(imgdata)
def to_login(request):
    if 'user_info' in request.session.keys():
        request.session.pop('user_info')
    return render(request,'login.html')

def execute_login(request):   #登陆
    ph = request.POST.get('phone')
    pw = request.POST.get('password')
    logincode = request.POST.get('logincode')
    if logincode:
        logincode = logincode.upper()
        code = request.session['keep_code'].upper()
        if code == logincode:
            count_un = models.User.objects.filter(username=ph)
            if count_un:
                user_info = models.User.objects.filter(username=ph, password=pw)
                if user_info:
                    request.session['user_info'] = {"username": user_info[0].username,
                                                "nickname": user_info[0].nickname,
                                                "info": user_info[0].info,
                                                    }
                    msg = {'status': True}
                else:
                    msg = {'status': False, 'Tip': '密码不正确!'}
            else:
                msg = {'status': False, 'Tip': '用户不存在!'}
        else:
            msg = {'status': False, 'Tip': '验证码错误!'}

    else:
        msg = {'status': False, 'Tip': '请输入验证码!'}

    return resp(json.dumps(msg))
# 登录操作
#第三方登录
def sanfang_init(request):
    provider = request.session.get('social_auth_last_login_backend','default')
    user_info_sanfang = request.session.get('user_info_sanfang',None)
    if user_info_sanfang:
        user_info = user_info_sanfang
        username = provider+str(user_info['id'])
        password = '88888888'
        nickname = user_info['username']
        info = user_info['profile_image_url']
        print(username,nickname,info)
        if user_info['gender'] == 'm':
            gender = '男'
        else:
            gender = '女'
        regist_time = time.strftime('%F %T')
        result = models.User.objects.filter(username=username).count()
        if result==0:
            models.User.objects.create(username=username,
                                       password=password,
                                       nickname=nickname,
                                       info=info,
                                       gender=gender,
                                       regist_time=regist_time, )
        request.session['user_info'] = {'username': username,
                                        'nickname': nickname,
                                        'info': info}
        return redirect('/')
    else:
        return resp('<h1>第三方登录失败!请检验账号密码!</h1>')
#第三方登录
# 注册操作
import time
import os
def to_shop_register(request):
    if 'user_info' in request.session.keys():
        request.session.pop('user_info')
    return render(request,'reg.html')
def check_reg(request):
    username = request.POST.get('username')
    password = request.POST.get('pwd1')
    msg_code = request.POST.get('verifycode')
    nickname = request.POST.get('nickname')
    regist_time = time.strftime('%F %T')
    info = '/static/users/imgs/avatars/default.jpg'
    if 'msgcode_info' in request.session.keys():
        msgcode_info = request.session['msgcode_info']
        if username == msgcode_info["username"] and msg_code == msgcode_info["msg_code"]:
            models.User.objects.create(username=username,
                                       password=password,
                                       nickname=nickname,
                                       info=info,
                                       regist_time=regist_time,)
            msg = {"status": True}
            #欢迎新用户群里消息加
            nickname_admin=models.User.objects.filter(username='18713585378')[0].nickname
            info_admin=models.User.objects.filter(username='18713585378')[0].info
            content_welcome = '欢迎'+nickname+'同学来到懒人商城会员群!'
            models.Qun.objects.create(username='18713585378',qun_id='1',nickname=nickname_admin,
                                      content=content_welcome,info=info_admin)
            #欢迎新用户群里消息加
        else:
            msg = {"status": False, "tips": "验证码或手机号错误!"}
    else:
        msg = {"status": False, "tips": "请点击发送短信验证码"}

    #由注册页面直接进入主页需要改缓存有个小bug,点击取消再不通过登录进入主页的话就有此注册人的信息
    request.session['user_info']={'username': username,
                                    'nickname': nickname,
                                    'info': info}
    # 由注册页面直接进入主页需要改缓存
    return resp(json.dumps(msg))
def check_un(request):
    username = request.POST.get('register_form')
    re = models.User.objects.filter(username=username)
    if not re:
        msg = {"status": True}
    else:
        msg = {"status": False, "tips": "用户名重复"}
    return resp(json.dumps(msg))
# 注册操作