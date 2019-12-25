#-*- coding:utf-8 -*-
# author:Administrator
# datetime:2019/8/12 13:27
# software: PyCharm
from django.shortcuts import render,HttpResponse as resp
from . import models
import json
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from django.db.models import Q
from django.core import serializers
#获取个人信息
def add_new_user(guanliyuan):
    result = models.User.objects.filter(username=guanliyuan)
    fr_dic = json.loads(result[0].frs_quns)
    quns = fr_dic["quns"]
    fr_list = []
    frs = models.User.objects.filter(~Q(username=guanliyuan))  # 初始用户都有三个无需判断
    for fr in frs:
        fr_list.append(fr.username)
    frs_quns = {"frs": fr_list, "quns": quns}
    models.User.objects.filter(username=guanliyuan).update(frs_quns=json.dumps(frs_quns))

def to_account(request):
    # 管理员好友列表更新成数据库所有其他用户都是管理员好友(就不用if判断了,肯定存在)
    add_new_user('18713585378')
    add_new_user('17695938928')
    add_new_user('18522079392')
    users = models.User.objects.all()
    user_list=[]
    for user in users:
        user_list.append(user.username)
    models.QunInfo.objects.filter(id=1).update(qun_list=json.dumps(user_list))
    # 创建新用户时添加到管理员好友列表中
    username = request.session['user_info']['username']
    user = models.User.objects.filter(username=username)[0]
    cmts_list = models.Comments.objects.filter(username=username)
    wen_list = models.AskForm.objects.filter(username=username)
    return  render(request,'shop-account.html',{"user":user,"cmts_list":cmts_list,"wen_list":wen_list})


#获取个人信息
def to_standart(request):
    username = request.session['user_info']['username']
    user = models.User.objects.filter(username=username)[0]
    return render(request, 'shop-standart-forms.html', {"user":user})

#
#
# 修改个人信息
def change_forms(request):
    username = request.POST.get("username")
    nickname = request.POST.get("nn_update")
    password1 = request.POST.get("pw_update1")
    birthday = request.POST.get("birth_update")
    gender = request.POST.get("sex")
    email = request.POST.get("email_update")
    avatar_update = request.FILES.get("img_update")

    if avatar_update:#未修改
        ext = os.path.splitext(avatar_update.name)[1]
        avatarname = str(time.time()*1000)[:13]+username+ext
        with open(os.path.join('StaticResources/users/imgs/avatars/'+avatarname),'wb') as f:
            for chunk in avatar_update.chunks(chunk_size = 1024):
                f.write(chunk)
                pass
        info = '/static/users/imgs/avatars/'+avatarname
        info_last = models.User.objects.filter(username=username)[0].info
        index_gang = info_last.rfind('/')
        last_img = info_last[index_gang + 1:]
        flag_remove = os.path.splitext(last_img)[0]
        if flag_remove.isdigit():
            os.remove(os.path.join('StaticResources/users/imgs/avatars/' + last_img))

    else:
        info = models.User.objects.filter(username=username)[0].info
        pass
    models.User.objects.filter(username=username).update(nickname=nickname,
                                                         password=password1,
                                                         birthday=birthday,
                                                         gender=gender,
                                                         info=info,
                                                         email=email)
    if email:
        #发送邮件
        my_un = '1037227556@qq.com'
        my_pw = 'mrqujsvjbppzbeih'
        receive = email
        try:
            msg = MIMEText('<h2>欢迎<span style="font-size=30px;color="green";">'+nickname+'</span>同学来到<span style="font-size=30px;color="sandbrown";">懒人商城</span></h2>','html','utf-8')
            msg['Form'] = formataddr(['LazyGuys.cn',my_un])
            msg['To'] = formataddr(['懒人商城会员',receive])
            msg['Subject'] = '问候!'
            server = smtplib.SMTP_SSL('smtp.qq.com',465)
            server.login(my_un,my_pw)
            server.sendmail(my_un,receive,msg.as_string())
            server.quit()
            print('发送邮箱成功!')
        except Exception:
            print('发送邮箱失败!')
        pass
    user_info = models.User.objects.filter(username=username)
    request.session['user_info'] = {"username": user_info[0].username,
                                    "nickname": user_info[0].nickname,
                                    "info": user_info[0].info,
                                    }
    msg = {"status": True}
    return resp(json.dumps(msg))
def uploadfile(request):
    username = request.session['user_info']['username']
    cmts_nickname = request.session['user_info']['nickname']
    cmts_time = time.strftime('%F %T')
    html = request.POST.get('review')
    haoping = request.POST.get('haoping')
    goods_id_review = request.POST.get('goods_id_review')
    models.Comments.objects.create(goods_id=goods_id_review,
                                   cmts_content=html,
                                   username=username,
                                   cmts_nickname=cmts_nickname,
                                   cmts_time=cmts_time,
                                   cmts_star=float(haoping))
    #商品好评量加上去
    good_info = models.Goods.objects.filter(id=goods_id_review)
    if float(haoping)<=3.0:
        haoping=3.0
    elif float(haoping) >= 4.5:
        haoping = 5
    else:
        haoping = float(haoping)
    reviews_num = models.Comments.objects.filter(goods_id=goods_id_review).count()
    haoping_new = float( (float(good_info[0].haoping)*reviews_num+haoping)/(reviews_num+1) )
    models.Goods.objects.filter(id=goods_id_review).update(haoping=haoping_new)
    #商品好评量加上去
    return resp(json.dumps({"status":True}))
def richtext_upload(request):
    username = request.session['user_info']['username']
    file = request.FILES.get('upload')
    if file:
        ext = os.path.splitext(file.name)[1]
        filename = str(time.time() * 1000)[:13]+username[-6:]+ext
        with open(os.path.join('StaticResources/upload/review_imgs/' + filename), 'wb') as f:
            for chunk in file.chunks(chunk_size=1024):
                f.write(chunk)
                pass
        address = '/static/upload/review_imgs/' + filename

        msg = {"uploaded":1,"url":address,"fileName":filename}
        return resp(json.dumps(msg))
        pass
    else:
        msg = {"status":False,"tip":"没有获取到文件"}
        return resp(json.dumps(msg))

def qingwen(request):
    goods_id = request.POST.get('goods_id')
    Ask = request.POST.get('Ask')
    nickname = request.session['user_info']['nickname']
    username = request.session['user_info']['username']
    wen_time = time.strftime('%F %T')
    if Ask and nickname and goods_id:
        models.AskForm.objects.create(wen=Ask,
                                      nickname=nickname,
                                      goods_id=goods_id,
                                      wen_time=wen_time,
                                      username=username)
    wenda_list = models.AskForm.objects.filter(goods_id=goods_id,username=username,wen_time=wen_time).order_by('-dianzan')
    wenda_list = serializers.serialize('json', wenda_list)
    wenda_list = json.loads(wenda_list)
    if wenda_list:
        for item in wenda_list:
            item['fields']['da'] = json.loads(item['fields']['da'])

    # print(wenda_list)
    return resp(json.dumps({"wenda_list":wenda_list}))
def huifu(request):
    wen_id = request.POST.get('wen_id')
    Anwser = request.POST.get('Anwser')
    nickname = request.session['user_info']['nickname']
    wenda_list = models.AskForm.objects.filter(id=wen_id)
    da = json.loads(wenda_list[0].da)
    da.append({"nickname":nickname,"content":Anwser,"da_time":time.strftime('%F %T')})
    models.AskForm.objects.filter(id=wen_id).update(da=json.dumps(da))
    wenda_list_this = models.AskForm.objects.filter(id=wen_id)#只改此问题的答复情况
    wenda_list_this = serializers.serialize('json', wenda_list_this)
    wenda_list_this = json.loads(wenda_list_this)
    if wenda_list_this:
        for item in wenda_list_this:
            item['fields']['da'] = json.loads(item['fields']['da'])
    return resp(json.dumps({"wenda_list_this":wenda_list_this}))
def dianzan(request):
    username = request.session['user_info']['username']
    wen_id = request.POST.get('wen_id')
    print(wen_id)
    wen_username = models.AskForm.objects.filter(id=wen_id)[0].username
    print(username,wen_username)
    if not username == wen_username:
        dianzan_new = models.AskForm.objects.filter(id=wen_id)[0].dianzan+1
        print('点赞',dianzan_new)
        models.AskForm.objects.filter(id=wen_id).update(dianzan=dianzan_new)
        msg = {"status":True,"zan_num":dianzan_new}
    else:
        msg = {"status":False}
    return resp(json.dumps(msg))

