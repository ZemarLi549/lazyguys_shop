#-*- coding:utf-8 -*-
# author:Administrator
# datetime:2019/8/14 17:05
# software: PyCharm
from PIL import Image, ImageDraw, ImageFont
from . import models
from io import BytesIO
from django.shortcuts import render,HttpResponse as resp
import json
import random
import time
import os
from django.db.models import Q

def produce_code(width,height):
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(os.path.join('StaticResources/font/Ikaros.otf'), 40)
    for i in range(2000):
        position = (random.randint(0, width), random.randint(0, height))
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.point(position, color)
        pass
    # ***********字母数字组合****************
    all_char = 'QWERTYUPASDFGHJKXCVBNMqwertyuipasdfghjkbnm3456789'
    verify_code = ''
    for i in range(4):
        j = random.randint(0, len(all_char) - 1)
        verify_code += all_char[j]
        pass
    code = verify_code
    for j in range(len(code)):
        y = random.randint(0,10)
        # 0,20  30,50  60,80  90,110
        x = random.randint(j*30,(j+1)*30-20)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.text((x,y),code[j],fill=color,font=font)
        pass
    for i in range(10):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.line((begin, end), fill=color, width=2)
    pass
    f = BytesIO()
    img.save(f, 'png')
    imgdata = f.getvalue()
    return imgdata,code
def get_my_frs_info(username):#获取某人好友全部信息(头像,昵称id)
    user_info = models.User.objects.filter(username=username)[0]
    frs_quns = json.loads(user_info.frs_quns)
    frs = get_user_info(frs_quns['frs'])  # 获取某人部信息()
    return frs
def get_my_quns_info(username):# 获取某人群全部信息()
    user_info = models.User.objects.filter(username=username)[0]
    frs_quns = json.loads(user_info.frs_quns)
    quns = []
    for qun in frs_quns['quns']:
        qun_info = models.QunInfo.objects.filter(id=int(qun))
        if qun_info:
            qun_name = qun_info[0].qun_name
            qun_list = qun_info[0].qun_list
            dic2 = {"qun_id": qun, "qun_name": qun_name, "qun_list": qun_list}
            quns.append(dic2)
    return quns
def to_chat(request):
    username = request.session['user_info']['username']
    user_info = models.User.objects.filter(username=username)[0]
    frs_quns = json.loads(user_info.frs_quns)
    new_frs = get_user_info(json.loads(user_info.new_frs))#获取新好友请求昵称头像的列表
    for item in new_frs:
        while new_frs.count(item)>1:#去除重复好友请求!
            new_frs.remove(item)
    frs = get_my_frs_info(username)#获取好友昵称头像的列表
    quns = get_my_quns_info(username)#获取我的群信息的列表
    frs_list = frs_quns['frs']
    request.session['frs_list'] = frs_list
    return render(request,'chat.html',{"frs":frs,"quns":quns,"new_frs":new_frs})
def updateAvatar(request):
    avatar_update = request.FILES.get('ava_update')
    myusername = request.POST.get('myusername')
    if avatar_update:#上传不为空
        ext = os.path.splitext(avatar_update.name)[1]
        avatarname = str(time.time()*1000)[:13]+myusername+ext
        with open(os.path.join('StaticResources/users/imgs/avatars/'+avatarname),'wb') as f:
            for chunk in avatar_update.chunks(chunk_size = 1024):
                f.write(chunk)
                pass
        info = '/static/users/imgs/avatars/'+avatarname
        info_last = models.User.objects.filter(username=myusername)[0].info
        index_gang = info_last.rfind('/')
        last_img = info_last[index_gang + 1:]
        flag_remove = os.path.splitext(last_img)[0]
        if flag_remove.isdigit():
            os.remove(os.path.join('StaticResources/users/imgs/avatars/' + last_img))
        models.User.objects.filter(username=myusername).update(info=info,)
        ses = request.session['user_info']#只能全部赋值取出来再改才行,单独修改不行
        # print( request.session['user_info']['info'] )
        ses['info'] = info
        request.session['user_info'] = ses
        msg = {"status":True}
    else:
        msg = {"status":False,"tip":"更新头像为空!"}
    return resp(json.dumps(msg))
def update_my_nn(request):
    my_nn = request.POST.get('my_nn')
    my_un = request.POST.get('my_un')
    if my_nn:
        models.User.objects.filter(username=my_un).update(nickname=my_nn)
        msg={"status":True}
        re = request.session['user_info']
        re['nickname'] = my_nn
        request.session['user_info'] = re
        pass
    else:
        msg = {"status":False,"tip":"昵称输入为空!"}
    return resp(json.dumps(msg))
def serch_content(request):
    my_username = request.POST.get('me')
    fr_username = request.POST.get('fr')
    content_list = models.Chat.objects.filter(Q(send=my_username)&Q(receive=fr_username)|Q(send=fr_username)&Q(receive=my_username))
    chat_list = []
    for chat in content_list:
        dic = {"num":chat.id,
               "content":chat.content,
               "send":chat.send,
               "receive":chat.receive,
               "time":chat.time,}
        chat_list.append(dic)


    fr_fr_list = get_fr_list(fr_username)#查找我是不是在对方好友列表中
    if my_username in fr_fr_list:
        msg = {"status":True,"chat_list":chat_list}
    else:
        msg = {"status": False}#不在对方好友列表中

    return resp(json.dumps(msg))
def serch_qun_content(request):
    qun_id = request.POST.get('qun_id')
    content_list = models.Qun.objects.filter(qun_id=qun_id)
    chat_list = []
    for chat in content_list:
        dic = {"num":chat.id,
               "content":chat.content,
               "username":chat.username,
               "nickname":chat.nickname,
               "time":chat.time,
               "info":chat.info,}
        chat_list.append(dic)
    return resp(json.dumps(chat_list))
def chat_addcontent(request):
    send = request.POST.get('send')
    receive = request.POST.get('receive')
    content = request.POST.get('content')
    my_nickname = request.POST.get('my_nickname')
    myavrtar = request.POST.get('myavrtar')
    qun_id = request.POST.get('qun_id')
    ti = time.strftime('%F %T')
    if qun_id:#如果是群聊的话
        models.Qun.objects.create(qun_id=qun_id,
                                  username=send,
                                   content=content,
                                   time=ti,
                                  nickname=my_nickname,
                                  info=myavrtar)
        msg = {'time': ti}
        pass
    else:#如果是私人对话的话
        models.Chat.objects.create(send=send,
                                        receive=receive,
                                        content=content,
                                        time=ti,)
    msg = {'time':ti}
    return resp(json.dumps(msg))
def serch_frs(request):
    keywords = request.POST.get('keywords').strip(' ')
    username = request.session['user_info']['username']
    frs_info = get_my_frs_info(username)
    serch_frs_list = []
    for fr_info in frs_info:
        if keywords in fr_info['nickname'] or keywords==fr_info['username']:
            serch_frs_list.append(fr_info)
    serch_frs_list = serch_frs_list
    return resp(json.dumps(serch_frs_list))
def rich_send_upload(request):
    username = request.session['user_info']['username']
    file = request.FILES.get('upload')
    if file:
        ext = os.path.splitext(file.name)[1]
        filename = str(time.time() * 1000)[:13]+username[-6:]+ext
        with open(os.path.join('StaticResources/upload/chat_imgs/' + filename), 'wb') as f:
            for chunk in file.chunks(chunk_size=1024):
                f.write(chunk)
                pass
        address = '/static/upload/chat_imgs/' + filename

        msg = {"uploaded":1,"url":address,"fileName":filename}
        return resp(json.dumps(msg))
        pass
    else:
        msg = {"status":False,"tip":"没有获取到文件"}
        return resp(json.dumps(msg))
def get_user_info(username_list):#根据用户名列表生成列表包括昵称和头像
    user_info = []
    for username in username_list:
        user_ls = models.User.objects.filter(username=username)
        if user_ls:
            nickname = user_ls[0].nickname
            info = user_ls[0].info
            dic = {"username": username, "nickname": nickname, "info": info}
            user_info.append(dic)
    return user_info
def search_qun_list(request):
    qun_id = request.POST.get('qun_id')
    if qun_id:
        qun_info = models.QunInfo.objects.filter(id=int(qun_id))
        qun_list = json.loads(qun_info[0].qun_list)
        chengyuan_list = get_user_info(qun_list)
        pass
    else:
        chengyuan_list = []
    return resp(json.dumps(chengyuan_list))
def get_fr_list(username):#获取我的好友username的列表
    re = models.User.objects.filter(username=username)
    fr_list = json.loads(re[0].frs_quns)['frs']
    return fr_list
def get_qun_list(username):
    re = models.User.objects.filter(username=username)
    qun_list = json.loads(re[0].frs_quns)['quns']
    return qun_list
def search_user_list(request):
    my_username = request.POST.get('my_username')
    search_content = request.POST.get('search_content')
    qun_info = models.QunInfo.objects.filter(id=1)
    qun_list = json.loads(qun_info[0].qun_list)
    all_user_list = get_user_info(qun_list)
    fr_list = get_fr_list(my_username)#函数鞋的
    search_list = []
    for user in all_user_list:
        if (search_content in user['nickname'] or search_content==user['username']):
            if user['username'] != my_username and not(user['username'] in fr_list ) :
                search_list.append(user)
    return resp(json.dumps(search_list))
def add_new_fr(request):
    to_username = request.POST.get('to_username')
    my_username = request.POST.get('my_username')
    if to_username and my_username:
        to_user = models.User.objects.filter(username=to_username)
        new_frs = json.loads(to_user[0].new_frs)
        new_frs.append(my_username)
        models.User.objects.filter(username=to_username).update(new_frs=json.dumps(new_frs))
        msg = {"status":True}
    else:
        msg = {"status":False}
    return resp(json.dumps(msg))
def shuaxin_new_fr(request):
    username = request.session['user_info']['username']
    user_info = models.User.objects.filter(username=username)[0]
    new_frs = get_user_info(json.loads(user_info.new_frs))  # 获取新好友请求昵称头像的列表
    return resp(json.dumps(new_frs))
def jieshou_new_fr(request):
    from_username = request.POST.get('from_username')
    to_username = request.POST.get('to_username')
    to_user_info = models.User.objects.filter(username=to_username)[0]
    new_frs_new = json.loads(to_user_info.new_frs)
    #取好友列表
    fr_list = get_fr_list(to_username)  # 函数鞋的
    qun_list = get_qun_list(to_username)  # 函数鞋的
    # 取好友列表
    fr_list.append(from_username)#添加进好友列表
    frs_quns_new = {"frs":fr_list,"quns":qun_list}
    new_frs = get_user_info(fr_list)  # 获取新好友请求昵称头像的列表
    new_frs_new.remove(from_username)#好友请求列表删除这个人
    models.User.objects.filter(username=to_username).update(new_frs=json.dumps(new_frs_new),
                                                            frs_quns=json.dumps(frs_quns_new))

    #改请求人信息
    #发个信消息
    models.Chat.objects.create(send=to_username,receive=from_username,content='你好,我们已经是好友了哦,可以开始聊天了',time=time.strftime('%F %T'))
    #发个信消息
    # 取好友列表
    fr_list_two = get_fr_list(from_username)  # 函数鞋的
    qun_list_two = get_qun_list(from_username)  # 函数鞋的
    # 取好友列表
    fr_list_two.append(to_username)  # 添加进好友列表
    frs_quns_new_two = {"frs": fr_list_two, "quns": qun_list_two}
    models.User.objects.filter(username=from_username).update(frs_quns=json.dumps(frs_quns_new_two))

    #改请求人信息
    frs = get_user_info([from_username,])
    fr = frs[0]
    return resp(json.dumps(fr))


def jujue_new_fr(request):  # 记得更新session
    from_username = request.POST.get('from_username')
    to_username = request.POST.get('to_username')
    to_user_info = models.User.objects.filter(username=to_username)[0]
    new_frs_new = json.loads(to_user_info.new_frs)
    new_frs_new.remove(from_username)  # 好友请求列表删除这个人
    models.User.objects.filter(username=to_username).update(new_frs=json.dumps(new_frs_new) )
    msg = {"status": True}
    return resp(json.dumps(msg))
def shanchutuichu(request):
    my_username = request.POST.get('my_username')
    qun_id = request.POST.get('qun_id')
    fr_username = request.POST.get('fr_username')
    if qun_id:#退出群
        my_qun_list = get_qun_list(my_username)
        my_qun_list.remove(qun_id)
        my_fr_list = get_fr_list(my_username)
        frs_quns_new = {"frs":my_fr_list,"quns":my_qun_list}
        models.User.objects.filter(username=my_username).update(frs_quns=json.dumps(frs_quns_new))
        qun_list = json.loads(models.QunInfo.objects.filter(id=qun_id)[0].qun_list)
        qun_list.remove(my_username)
        models.QunInfo.objects.filter(id=qun_id).update(qun_list=json.dumps(qun_list))
        pass
    else:#删除好友
        my_qun_list = get_qun_list(my_username)
        my_fr_list = get_fr_list(my_username)
        my_fr_list.remove(fr_username)
        frs_quns_new = {"frs": my_fr_list, "quns": my_qun_list}
        models.User.objects.filter(username=my_username).update(frs_quns=json.dumps(frs_quns_new))
        pass
    return resp(json.dumps({"status":True}))
def create_qun(request):
    qun_nickname = request.POST.get('qun_nickname')
    create_user = request.POST.get('create_user')
    if create_user and qun_nickname:
        #新群加上初始创建人
        qun_list = []
        qun_list.append(create_user)
        xinqun = models.QunInfo.objects.create(qun_name=qun_nickname,qun_list=json.dumps(qun_list))
        #创建人群聊列表加上去
        qun_list_fr_new = get_qun_list(create_user)
        qun_list_fr_new.append(str(xinqun.id))
        fr_fr_list = get_fr_list(create_user)
        frs_quns_new = {"frs": fr_fr_list, "quns": qun_list_fr_new}
        models.User.objects.filter(username=create_user).update(frs_quns=json.dumps(frs_quns_new))
        # 创建人群聊列表加上去
        msg = {"status": True, "qun_nickname": qun_nickname}
        pass
    else:
        msg = {"status":False}
    return resp(json.dumps(msg))
def yaoqing_fr(request):
    yao_username = request.POST.get('yao_username')
    qun_id = request.POST.get('qun_id')
    if yao_username and qun_id:
        re = models.QunInfo.objects.filter(id=qun_id)
        qun_list_new = json.loads(re[0].qun_list)
        qun_list_new.append(yao_username)#群新加成员
        models.QunInfo.objects.filter(id=qun_id).update(qun_list=json.dumps(qun_list_new))
        #被邀请的好友新加群列表
        qun_list_fr_new = get_qun_list(yao_username)
        qun_list_fr_new.append(qun_id)
        fr_fr_list = get_fr_list(yao_username)
        frs_quns_new = {"frs":fr_fr_list,"quns":qun_list_fr_new}
        models.User.objects.filter(username=yao_username).update(frs_quns=json.dumps(frs_quns_new))
        #被邀请的好友新加群列表
        msg = {"status": True,"yao_username":yao_username}
    else:
        msg = {"status":False}
    return resp(json.dumps(msg))

def yaoqing_list(request):#被邀请好友不能存在在本群里
    my_username = request.POST.get('my_username')
    qun_id = request.POST.get('qun_id')
    my_fr_list = get_fr_list(my_username)
    qun_list = json.loads( models.QunInfo.objects.filter(id=qun_id)[0].qun_list )
    yaoqing_list = []
    for item in my_fr_list:
        if not item in qun_list:
            yaoqing_list.append(item)
    yaoqing_list_info = get_user_info(yaoqing_list)
    return resp(json.dumps(yaoqing_list_info))
def luxun_news(request):
    my_username = request.POST.get('my_username')
    user_info = models.User.objects.filter(username=my_username)[0]
    frs_quns = json.loads(user_info.frs_quns)
    fr_list_now =  frs_quns['frs']
    frs_list = request.session['frs_list']#原来的好友列表
    news_last = request.POST.get('news_last','NO')  # 前台获取的
    if len(fr_list_now)>len(frs_list):#有新好友通过该验证了
        tt = len(fr_list_now)-len(frs_list)#可能有几个新好友
        new_fr_list = fr_list_now[-tt:]
        new_frs_info = get_user_info(new_fr_list)
        msg = {"status":True,"new_frs":new_frs_info}
        request.session['frs_list']=fr_list_now
    else:#没有新好友就继续执行新消息轮询
        if news_last=='NO':#一开始浏览器可能没缓存返回一个session给前台
            news_init = {}
            for fr_username in frs_list:
                content_list = models.Chat.objects.filter(Q(send=fr_username) & Q(receive=my_username))
                news_init[fr_username] = content_list.count()
            msg = {"status":False,"status_news": False,"news_init":news_init}
            pass
        else:#轮询信息用原来的好友列表即可

            news_now = {}#和上一次肯定一样长度的
            news_last = json.loads(news_last)
            for fr_username in frs_list:
                content_list = models.Chat.objects.filter(Q(send=fr_username) & Q(receive=my_username))
                news_now[fr_username]=content_list.count()
            pass
            if news_last.keys()==news_now.keys():
                
                news_compare = {}
                for k,v in news_now.items():
                    news_compare[k] = v-news_last[k]
                
                msg = {"status": False, "status_news": True, "news_compare":news_compare}
            else:#上一次缓存不是我的好友的登录可能是其他账号的
                msg = {"status": False, "status_news": False, "news_init": news_now}
                pass
    return resp(json.dumps(msg))
def lunxun_header_news(request):
    my_username = request.POST.get('my_username')
    user_info = models.User.objects.filter(username=my_username)[0]
    frs_quns = json.loads(user_info.frs_quns)
    fr_list_now = frs_quns['frs']
    frs_list = request.session['frs_list']  # 原来的好友列表
    news_last = request.POST.get('news_last','NO')  # 前台获取的
    if len(fr_list_now) > len(frs_list):  # 有新好友通过该验证了
        tt = len(fr_list_now) - len(frs_list)  # 可能有几个新好友
        new_fr_list = fr_list_now[-tt:]
        new_frs_info = get_user_info(new_fr_list)
        msg = {"status": True, "new_frs": new_frs_info}
        request.session['frs_list'] = fr_list_now
    else:  # 没有新好友就继续执行新消息轮询
        if news_last == 'NO':  # 一开始浏览器可能没缓存返回一个session给前台
            news_init = {}
            for fr_username in frs_list:
                content_list = models.Chat.objects.filter(Q(send=fr_username) & Q(receive=my_username))
                news_init[fr_username] = content_list.count()
            msg = {"status": False, "status_news": False, "news_init": news_init}
            pass
        else:  # 轮询信息用原来的好友列表即可

            news_now = {}  # 和上一次肯定一样长度的
            news_last = json.loads(news_last)
            for fr_username in frs_list:
                content_list = models.Chat.objects.filter(Q(send=fr_username) & Q(receive=my_username))
                news_now[fr_username] = content_list.count()
            pass
            if news_last.keys() == news_now.keys():

                news_compare = {}
                for k, v in news_now.items():
                    reee = models.User.objects.filter(username=k)
                    if reee:
                        nickname = reee[0].nickname
                        news_compare[k] = [v - news_last[k],nickname]

                msg = {"status": False, "status_news": True, "news_compare": news_compare}
            else:  # 上一次缓存不是我的好友的登录可能是其他账号的
                msg = {"status": False, "status_news": False, "news_init": news_now}
                pass
    return resp(json.dumps(msg))
def click_remove_news(request):
    my_username = request.POST.get('my_username')
    frs_list = request.session['frs_list']  # 原来的好友列表
    news_init = {}
    for fr_username in frs_list:
        content_list = models.Chat.objects.filter(Q(send=fr_username) & Q(receive=my_username))
        news_init[fr_username] = content_list.count()
    msg = {"status": True, "news_init": news_init}
    return resp(json.dumps(msg))