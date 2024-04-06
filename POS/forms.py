from django.forms import ModelForm, Form
from django.forms import IntegerField
from .models import Product

class ProductCartForm(Form):
    amount = IntegerField(max_value=10000, min_value=1, label="下單數量")