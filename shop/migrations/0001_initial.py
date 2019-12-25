# Generated by Django 2.1 on 2019-09-04 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('manager', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='AskForm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(default='', max_length=500)),
                ('wen', models.CharField(default='', max_length=500)),
                ('da', models.TextField(default='[]', max_length=10000)),
                ('nickname', models.CharField(max_length=128)),
                ('wen_time', models.CharField(default='2019-09-04 11:03:08', max_length=128)),
                ('goods_id', models.IntegerField()),
                ('dianzan', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('goods_id', models.IntegerField()),
                ('goods_size', models.CharField(max_length=256)),
                ('goods_img', models.CharField(max_length=500, null=True)),
                ('goods_name', models.CharField(max_length=256)),
                ('goods_totalprice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('goods_stock', models.IntegerField()),
                ('goods_unitprice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('goods_color', models.CharField(max_length=256)),
                ('username', models.CharField(max_length=128)),
                ('number', models.IntegerField()),
                ('addtime', models.CharField(default='2019-09-04 11:03:08', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=2000, null=True)),
                ('send', models.CharField(max_length=128)),
                ('receive', models.CharField(max_length=128)),
                ('time', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('cmts_id', models.AutoField(primary_key=True, serialize=False)),
                ('goods_id', models.IntegerField()),
                ('cmts_content', models.CharField(max_length=5000)),
                ('username', models.CharField(max_length=128)),
                ('cmts_nickname', models.CharField(max_length=128)),
                ('cmts_time', models.CharField(default='2019-09-04 11:03:08', max_length=128)),
                ('cmts_star', models.DecimalField(decimal_places=1, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('original_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('current_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('goods_stock', models.IntegerField()),
                ('category_yi', models.CharField(max_length=128, null=True)),
                ('category_er', models.CharField(max_length=128, null=True)),
                ('category_san', models.CharField(max_length=128, null=True)),
                ('category_si', models.CharField(max_length=128, null=True)),
                ('fav_num', models.IntegerField(default=0)),
                ('views_count', models.IntegerField(default=0)),
                ('sale_count', models.IntegerField(default=0)),
                ('goods_brief', models.CharField(max_length=500)),
                ('goods_img', models.CharField(max_length=500, null=True)),
                ('goods_desc', models.CharField(max_length=5000, null=True)),
                ('is_sale', models.BooleanField(default=False)),
                ('is_new', models.BooleanField(default=False)),
                ('haoping', models.DecimalField(decimal_places=1, default=3.5, max_digits=10)),
                ('lirun', models.DecimalField(decimal_places=2, default=50.0, max_digits=10)),
                ('parameter', models.CharField(default='["纯棉","宽松","S款M款L款XL款","红色蓝色黑色","青年休闲"]', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='HotSearchWords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords', models.CharField(default='', max_length=128)),
                ('index', models.IntegerField(default=0)),
                ('add_time', models.CharField(default='2019-09-04 11:03:08', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20)),
                ('order_num', models.CharField(max_length=128, null=True)),
                ('goods_info', models.TextField(max_length=50000)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('receive_name', models.CharField(max_length=128)),
                ('receive_address', models.CharField(max_length=256)),
                ('receive_tel', models.CharField(max_length=20)),
                ('addtime', models.CharField(default='2019-09-04 11:03:08', max_length=128)),
                ('remark', models.CharField(max_length=128)),
                ('pay_type', models.CharField(default='货到付款', max_length=128)),
                ('pay_status', models.CharField(max_length=10)),
                ('pay_time', models.CharField(default='2019-09-04 11:03:08', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Qun',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('qun_id', models.CharField(max_length=128)),
                ('username', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=5000, null=True)),
                ('nickname', models.CharField(max_length=128)),
                ('info', models.CharField(max_length=300)),
                ('time', models.CharField(default='2019-09-04 11:03:08', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='QunInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('qun_name', models.CharField(max_length=128)),
                ('qun_list', models.TextField(max_length=10000)),
                ('create_time', models.CharField(default='2019-09-04 11:03:08', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('nickname', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=128)),
                ('birthday', models.CharField(max_length=128, null=True)),
                ('gender', models.CharField(default='女', max_length=6)),
                ('email', models.CharField(max_length=128, null=True)),
                ('info', models.CharField(max_length=300)),
                ('regist_time', models.CharField(max_length=128)),
                ('frs_quns', models.TextField(default='{"frs":["18713585378","17695938928","18522079392"],"quns":["1"]}', max_length=20000)),
                ('new_frs', models.CharField(default='[]', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20)),
                ('province', models.CharField(default='', max_length=100)),
                ('city', models.CharField(default='', max_length=100)),
                ('district', models.CharField(default='', max_length=100)),
                ('address', models.CharField(default='', max_length=100)),
                ('signer_name', models.CharField(default='', max_length=100)),
                ('signer_mobile', models.CharField(default='', max_length=11)),
                ('add_time', models.DateTimeField(default='2019-09-04 11:03:08')),
            ],
        ),
        migrations.CreateModel(
            name='UserFav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('goods_id', models.IntegerField()),
                ('add_time', models.CharField(default='2019-09-04 11:03:07', max_length=128)),
            ],
        ),
    ]