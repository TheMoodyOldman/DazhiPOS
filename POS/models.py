from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Category(models.Model):

    name = models.CharField("類別名稱", max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField("名稱", max_length=50)

    image = models.ImageField("圖片", blank=True, null=True)

    cost = models.IntegerField("成本", validators=[MinValueValidator(1)])

    price = models.IntegerField("售價", validators=[MinValueValidator(1)])

    stock_quant = models.IntegerField("存貨數量", validators=[MinValueValidator(1)])

    ordering = models.IntegerField("未實現訂單", default=0, validators=[MinValueValidator(1)])

    last_stock = models.DateTimeField("上次存貨日期", auto_now_add=True)

    category = models.ForeignKey(
        Category, models.CASCADE, null=True, verbose_name="種類")
    
    def __str__(self):
        return self.name

class Order(models.Model):

    sum = models.IntegerField("訂單總價格", default = 0, validators=[MinValueValidator(1)])

    time = models.DateTimeField("訂單送出時間", auto_now_add=True)

    owner = models.ForeignKey(
        User, models.CASCADE, null=True, verbose_name="負責人")
    
    # def __str__(self):
    #     return self.name
    class Meta:
        ordering = ['-id']

class OrderItem(models.Model):

    amount = models.IntegerField("商品數量", validators=[MinValueValidator(1)])

    sum = models.IntegerField("總價格", default=0, validators=[MinValueValidator(1)])

    product = models.ForeignKey(
        Product, models.CASCADE, null=True, verbose_name="對應產品")

    order = models.ForeignKey(
        Order, models.CASCADE, null=True, verbose_name="對應訂單")
    
    # def __str__(self):
    #     return self.name