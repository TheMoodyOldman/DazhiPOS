# Generated by Django 3.1.4 on 2024-04-03 05:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='類別名稱')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='訂單送出時間')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='負責人')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='名稱')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='圖片')),
                ('cost', models.IntegerField(verbose_name='成本')),
                ('price', models.IntegerField(verbose_name='售價')),
                ('stock_quant', models.IntegerField(verbose_name='存貨數量')),
                ('ordering', models.IntegerField(default=0, verbose_name='未實現訂單')),
                ('last_stock', models.DateTimeField(auto_now_add=True, verbose_name='上次存貨日期')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='POS.category', verbose_name='種類')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='商品數量')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='POS.order', verbose_name='對應訂單')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='POS.product', verbose_name='對應產品')),
            ],
        ),
    ]
