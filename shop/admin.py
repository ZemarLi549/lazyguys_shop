from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Admin)
admin.site.register(models.Goods)
admin.site.register(models.Cart)
admin.site.register(models.Orders)
admin.site.register(models.UserFav)
admin.site.register(models.UserAddress)
admin.site.register(models.Comments)
admin.site.register(models.Qun)
admin.site.register(models.QunInfo)
admin.site.register(models.HotSearchWords)
admin.site.register(models.Chat)
admin.site.register(models.AskForm)