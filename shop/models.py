from django.db import models
import time
# Create your models here.
class User(models.Model):#会员表格
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)#手机号即是用户名username
    nickname = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    birthday = models.CharField(null=True,max_length=128)
    gender = models.CharField(max_length=6,default='女')
    email = models.CharField(max_length=128,null=True)
    info = models.CharField(max_length=300)#用户头像
    regist_time = models.CharField(max_length=128)
    frs_quns = models.TextField(max_length=20000, default='{"frs":["18713585378","17695938928","18522079392"],"quns":["1"]}')  # 初始好友为三个管理员
    new_frs = models.CharField(max_length=2000,default='[]')
class UserFav(models.Model):
    """
    用户收藏
    """
    username = models.CharField(max_length=20)  # 收藏人用户名
    goods_id = models.IntegerField()  # 商品编号
    add_time = models.CharField(max_length=128,default=time.strftime('%F %T'))
class UserAddress(models.Model):
    """
    用户收货地址(使用三级联动添加)
    """
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    province = models.CharField(max_length=100, default="")#省
    city = models.CharField(max_length=100, default="")#市
    district = models.CharField(max_length=100, default="")#区
    address = models.CharField(max_length=100, default="")#详细地址
    signer_name = models.CharField(max_length=100, default="")#签收人
    signer_mobile = models.CharField(max_length=11, default="")#
    add_time = models.DateTimeField(default=time.strftime('%F %T'))
class Admin(models.Model):#管理员表
    id = models.AutoField(primary_key=True)
    manager = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
class Goods(models.Model):#商品表格
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)#原价
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)#现价
    goods_stock = models.IntegerField()#总库存
    # sub_stock = models.CharField(max_length=256,null=True)#库存(不同组合的库存,例如L型号黑色的衣服,dict类型dumps成字符串了后期再加)
    category_yi = models.CharField(max_length=128,null=True)#商品所属大分类例如鞋类
    category_er =models.CharField(max_length=128,null=True)#商品所属二级分类例如鞋类
    category_san = models.CharField(max_length=128,null=True)#商品所属三级分类鞋类下的皮鞋类
    category_si = models.CharField(max_length=128,null=True)#商品四级分类所属皮鞋下的花花公子牌子
    fav_num = models.IntegerField(default=0)#收藏量
    views_count = models.IntegerField(default=0)#点击量
    sale_count = models.IntegerField(default=0)#售卖量
    goods_brief = models.CharField(max_length=500)#商品简短描述
    goods_img = models.CharField(max_length=500,null=True)#商品的三张图片,list格式jump成字符串
    goods_desc = models.CharField(max_length=5000,null=True)
    is_sale = models.BooleanField(default=False)#是否有优惠活动商品
    is_new = models.BooleanField(default=False)#是否新品
    haoping = models.DecimalField(max_digits=10, decimal_places=1,default=3.5)
    lirun = models.DecimalField(max_digits=10, decimal_places=2,default=50.00)
    parameter = models.CharField(max_length=1000
                                 ,default='["纯棉","宽松","S款M款L款XL款","红色蓝色黑色","青年休闲"]')#商品参数标签



class Cart(models.Model):#购物车
    id = models.AutoField(primary_key=True)
    goods_id = models.IntegerField()#商品编号
    goods_size = models.CharField(max_length=256)#商品尺寸
    goods_img = models.CharField(max_length=500, null=True)  # 商品的三张图片,list格式jump成字符串
    goods_name = models.CharField(max_length=256)
    goods_totalprice = models.DecimalField(max_digits=10, decimal_places=2)  # 总价单项
    goods_stock = models.IntegerField()#总库存
    goods_unitprice = models.DecimalField(max_digits=10, decimal_places=2)  # 现价
    goods_color = models.CharField(max_length=256)#商品颜色
    username = models.CharField(max_length=128)
    number = models.IntegerField()#购买数量
    addtime = models.CharField(max_length=128,default=time.strftime('%F %T'))#添加购物车时间
class Orders(models.Model):
    id = models.AutoField(primary_key=True)#设置订单号初始值为10001咋设置
    username = models.CharField(max_length=20)#下单人用户名
    order_num = models.CharField(max_length=128,null=True)#订单号
    goods_info = models.TextField(max_length=50000)  # 订单商品信息
    total = models.DecimalField(max_digits=10, decimal_places=2)#订单总价
    receive_name = models.CharField(max_length=128)#收货人姓名
    receive_address = models.CharField(max_length=256)#收货人姓名
    receive_tel = models.CharField(max_length=20)#收货人电话
    addtime = models.CharField(max_length=128,default=time.strftime('%F %T'))  # 添加订单时间
    remark = models.CharField(max_length=128)  # 订单备注
    pay_type = models.CharField(max_length=128,default='货到付款')  # 订单方式
    pay_status = models.CharField(max_length=10)#支付状态
    pay_time = models.CharField(max_length=128,default=time.strftime('%F %T'))
class Comments(models.Model):
    cmts_id = models.AutoField(primary_key=True)
    goods_id = models.IntegerField()
    cmts_content =  models.CharField(max_length=5000)
    username =  models.CharField(max_length=128)#评价人
    cmts_nickname =  models.CharField(max_length=128)
    cmts_time =  models.CharField(max_length=128, default=time.strftime('%F %T'))
    cmts_star = models.DecimalField(max_digits=10, decimal_places=1)#评价等级


class HotSearchWords(models.Model):
    """
    热搜词
    """
    keywords = models.CharField(default="", max_length=128)
    index = models.IntegerField(default=0)#搜索量次数
    add_time = models.CharField(max_length=128,default=time.strftime('%F %T'))
class AskForm(models.Model):
    """
    问区(一个问题可有多个回答)
    """
    id = models.AutoField(primary_key=True)
    username = models.CharField(default='', max_length=500)
    wen = models.CharField(default='', max_length=500)
    da = models.TextField(max_length=10000,default='[]')#答复最多10000个字为列表套字典[{"nickname":xxx,"content":xxx,"da_time":xxx}]格式
    nickname = models.CharField(max_length=128)
    wen_time = models.CharField(max_length=128,default=time.strftime('%F %T'))
    goods_id = models.IntegerField()
    dianzan = models.IntegerField(default=0)
class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=2000,null=True)
    send = models.CharField(max_length=128)
    receive = models.CharField(max_length=128)
    time = models.CharField(max_length=128)
class Qun(models.Model):
    id = models.AutoField(primary_key=True)
    qun_id = models.CharField(max_length=128)
    username = models.CharField(max_length=128)
    content = models.CharField(max_length=5000,null=True)
    nickname = models.CharField(max_length=128)
    info = models.CharField(max_length=300)
    time = models.CharField(max_length=128,default=time.strftime('%F %T'))
class QunInfo(models.Model):
    id = models.AutoField(primary_key=True)
    qun_name = models.CharField(max_length=128)
    qun_list = models.TextField(max_length=10000)  # ["username","",""]
    create_time = models.CharField(max_length=128,default=time.strftime('%F %T'))