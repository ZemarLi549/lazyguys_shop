#-*- coding:utf-8 -*-
# author:Lizengxin
# datetime:2019/8/23 10:23
# software: PyCharm
from . import models
from django.shortcuts import render,HttpResponse
import json
import random
import os
import time
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import base64
import cv2#pip install opencv-python
from selenium.webdriver import ActionChains
def bd_spider_pic(request):
    user_agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.8 (KHTML, like Gecko) Beamrise/17.2.0.9 Chrome/17.0.939.0 Safari/535.8',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; SV1; .NET CLR 1.1.4322)',
        'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
        'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
        'Opera/9.80(Macintosh;IntelMacOSX10.6.8;U;en)Presto/2.8.131Version/11.11',
        'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11']
    ua = {'user-agent': random.choice(user_agents)}
    page_num = request.GET.get('page_num','1')
    if page_num.isdigit():
        page_num = int(page_num)
        if page_num<1:
            page_num=1
            pass
    else:
        page_num=1
    keyword = request.GET.get('keyword')
    keyword = keyword.replace(' ','')
    pics_info = []
    if keyword:
        index = 0
        params = {
            'tn': 'resultjson_com',
            'ipn': 'rj',
            'ct': 201326592,
            'is': '',
            'fp': 'result',
            'queryWord': keyword,
            'cl': 2,
            'lm': -1,
            'ie': 'utf-8',
            'oe': 'utf-8', 'adpicid': '',
            'st': -1, 'z': '',
            'ic': 0,
            'word': keyword,
            's': '',
            'se': '',
            'tab': '',
            'width': '',
            'height': '',
            'face': 0, 'istype': 2,
            'qc': '', 'nc': 1,
            'fr': '', 'pn': 30*page_num, 'rn': 30,
            'gsm': '1e', '1488942260214': ''
        }
        url = 'https://image.baidu.com/search/acjson'
        try:
            resp = requests.get(url=url, timeout=15, headers=ua, params=params)
            resp.encoding = resp.apparent_encoding

            if resp.status_code == 200:
                data = json.loads(resp.text)
                for i in data.get('data'):
                    url = i.get('thumbURL', 'null')
                    if not url == 'null':
                        index += 1
                        ext = url[url.rfind('.'):]
                        pic_name = str(index) + ext
                        # resp = requests.get(url)
                        # open(os.path.join('StaticResources/baidu_pics',pic_name), 'wb').write(resp.content)
                        # 返回前台
                        dic = {"pic_url": url}
                        pics_info.append(dic)
                        # 返回前台
        except Exception as e:
            page_num=1
            print(e)
            print('爬虫失败!', '共获取到', index, '张图')
    else:
        page_num=1
        keyword = '头像'
    return HttpResponse(json.dumps({"keyword":keyword,"pics_info":pics_info,"page_num":page_num}))
def xuanze_avatar(request):
    tu_url = request.GET.get('tu_url')
    if tu_url:
        username = request.session['user_info']['username']
        user_info = models.User.objects.filter(username=username)[0]
        info_last = user_info.info
        try:
            res = requests.get(tu_url)
            ext = os.path.splitext(tu_url)[1]
            avatarname = str(time.time() * 1000)[:13] + username + ext
            with open(os.path.join('StaticResources/users/imgs/avatars/' + avatarname), 'wb') as f:
                f.write(res.content)
            info = '/static/users/imgs/avatars/' + avatarname
            index_gang = info_last.rfind('/')
            last_img = info_last[index_gang + 1:]
            flag_remove = os.path.splitext(last_img)[0]
            if flag_remove.isdigit():
                os.remove(os.path.join('StaticResources/users/imgs/avatars/' + last_img))
            models.User.objects.filter(username=username).update(info=info)
            request.session['user_info'] = {"username": user_info.username,
                                            "nickname": user_info.nickname,
                                            "info": info,
                                            }
            msg = {"status":True}
        except Exception as e:
            print(e)
            print('修改失败!')
            msg = {"status": False}
    else:
        msg={"status":False}
    return HttpResponse(json.dumps(msg))
def duibi_jd(request):
    goods_name = request.GET.get('goods_name',None)
    if goods_name:
        request.session['jd_keyword'] = goods_name
        msg = {"status":True}
    else:
        msg = {"status": False}
    return HttpResponse(json.dumps(msg))



def get_pianyi(slideimg,backimg):
    block = cv2.imread(slideimg, 0)
    template = cv2.imread(backimg, 0)
    # 二值化后的图片名称
    blockName = os.path.join('StaticResources/jd_code/block.jpg')
    templateName = os.path.join('StaticResources/jd_code/template.jpg')
    # 将二值化后的图片进行保存
    cv2.imwrite(blockName, block)
    cv2.imwrite(templateName, template)
    block = cv2.imread(blockName)
    block = cv2.cvtColor(block, cv2.COLOR_RGB2GRAY)
    block = abs(255 - block)
    cv2.imwrite(blockName, block)
    block = cv2.imread(blockName)
    template = cv2.imread(templateName)
    # 获取偏移量
    result = cv2.matchTemplate(block, template, cv2.TM_CCOEFF_NORMED)  # 查找block在template中的位置，返回result是一个矩阵，是每个点的匹配结果
    x, y = np.unravel_index(result.argmax(), result.shape)
    print("x方向的偏移", int(y * 0.4 + 18), 'x:', x, 'y:', y)
    return y
def jd_soutu(request):
    browser = webdriver.PhantomJS()
    browser.maximize_window()
    shangpin_info = []
    # 获取前台页码和关键字
    if 'jd_keyword' in request.session.keys():
        default = request.session['jd_keyword']
        if default == '':
            default = '服装'
    else:
        default = '服装'
    keyword = request.GET.get('keyword', default)
    print('key', keyword)
    if not keyword:
        keyword = default
    request.session['jd_keyword'] = keyword
    # 获取前台页码和关键字

    try:
        url = 'https://passport.jd.com/new/login.aspx?ReturnUrl=https://www.jd.com'
        browser.get(url)
        time.sleep(5)
        browser.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div/div[3]/a').click()
        time.sleep(1)
        browser.find_element_by_id('loginname').send_keys('18713585378')
        browser.find_element_by_id('nloginpwd').send_keys('lzx666666')
        browser.find_element_by_id('loginsubmit').click()
        time.sleep(5)
        code_src = browser.find_element_by_css_selector(
            '#JDJRV-wrap-loginsubmit>div>div>div>div.JDJRV-img-panel.JDJRV-click-bind-suspend>div.JDJRV-img-wrap>div.JDJRV-bigimg>img').get_attribute(
            'src')
        small_src = browser.find_element_by_css_selector(
            '#JDJRV-wrap-loginsubmit>div>div>div>div.JDJRV-img-panel.JDJRV-click-bind-suspend>div.JDJRV-img-wrap>div.JDJRV-smallimg>img').get_attribute(
            'src')
        img_data = base64.b64decode(code_src.split(',')[1])
        sm_img_data = base64.b64decode(small_src.split(',')[1])
        with open(os.path.join('StaticResources/jd_code/img_big.png'), 'wb') as f:
            f.write(img_data)
            pass
        with open(os.path.join('StaticResources/jd_code/img_small.png'), 'wb') as f:
            f.write(sm_img_data)
            pass
        slideimg = os.path.join('StaticResources/jd_code/img_small.png')
        backimg = os.path.join('StaticResources/jd_code/img_big.png')
        pianyi = get_pianyi(slideimg, backimg)
        action = ActionChains(browser)
        s3 = '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[2]/div[3]'
        drag_btn = browser.find_element_by_xpath(s3)
        action.click_and_hold(drag_btn).perform()
        move_x = int(pianyi / (9 / 7))
        move_steps = int(move_x / 4)
        cha = move_x / 4 - move_steps
        # xjia = 0
        for i in range(0, move_steps):
            # xjia = xjia+cha#差值
            # 路程前半部分速度较快
            if i < int(move_steps / 2):
                time.sleep(random.randint(1, 10) / 500)
                # 滑块每次向右移动四个像素，鼠标Y坐标在上下5个像素内随机摆动
                action.move_by_offset(4, random.randint(-5, 5)).perform()
            else:
                # 在路程的后半段，越接近终点速度越慢
                # 每次移动之前sleep一段时间，时间为总距离与已移动距离方差的倒数
                seed = 90.0 / (pow(move_steps, 2) - pow(i, 2))
                time.sleep(seed)
                action.move_by_offset(4, random.randint(-5, 5)).perform()
            print(drag_btn.location)
            action = ActionChains(browser)
            # mouse_action = action.click_and_hold(drag_btn)
        # 到达终点时，左右摆动，假装做调整。
        time.sleep(0.1)
        action = ActionChains(browser)
        print(cha)
        action.move_by_offset(4, random.randint(-5, 5)).perform()
        time.sleep(0.2)
        action.move_by_offset(-5, random.randint(-5, 5)).perform()
        time.sleep(0.1)
        # 松开鼠标
        action = ActionChains(browser)
        action.release().perform()
        browser.save_screenshot(os.path.join('StaticResources/jd_code/hua.png'))
        time.sleep(8)
        browser.save_screenshot(os.path.join('StaticResources/jd_code/yes.png'))
    except Exception as e:
        print(e)
        print('登录京东失败！')
    try:
        input_ele = browser.find_element_by_xpath('//*[@id="key"]')
        input_ele.send_keys(keyword)
        browser.find_element_by_xpath('//*[@id="search-2014"]/div/button').click()
        time.sleep(2)

        for j in range(2):  # 前两页数据120条商品
            browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(5)
            content = browser.page_source
            print('到这了看看,能搜索到指定内容')
            soup = bs(content, 'html.parser')
            shangpin_lis = soup.find(attrs={'class', 'gl-warp'}).find_all(attrs={'class', 'gl-item'})
            for li in shangpin_lis:
                img_url = li.find('img').attrs['source-data-lazy-img']
                name = li.find(attrs={'class', 'p-name-type-2'}).find('em').text
                shangpin_url = li.find(attrs={'class', 'p-name-type-2'}).find('a').attrs['href']
                price = li.find(attrs={'class', 'p-price'}).find('strong').text
                dic = {'img_url': img_url, 'name': name, 'shangpin_url': shangpin_url, 'price': price}
                shangpin_info.append(dic)
            pass
            browser.find_element_by_xpath('//*[@id="J_bottomPage"]/span[1]/a[9]').click()
    except Exception as e:
        print(e)
        print('搜索失败！')
    browser.delete_all_cookies()
    browser.close()
    return render(request, 'jd_sou.html', {'shangpin_info': shangpin_info})



