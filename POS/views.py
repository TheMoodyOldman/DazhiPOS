from typing import Any
from django.forms.forms import BaseForm
from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http.response import JsonResponse
from django.utils import timezone
from django.conf import settings

from .models import Product, Category, Order, OrderItem

from .forms import ProductCartForm

import os, openpyxl, datetime

# Create your views here.

class Home(TemplateView):
    template_name = 'main/home.html'

class Logout(TemplateView):
    template_name = 'registration/logged_out.html'

# ========== product ========== #

class ProductList(LoginRequiredMixin, ListView):
    model = Product
    template_name = "main/product/product_list.html"

class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "main/product/product_detail.html"

class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "main/product/product_create.html"

    fields = ['name', 'image', 'cost', 'price', 'stock_quant', 'category']
    success_url = reverse_lazy('cate')

    def form_valid(self, form):
        form.instance.order_quant = 0
        return super().form_valid(form)

class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "main/product/product_update.html"

    fields = ['name', 'cost', 'price']

    def get_success_url(self):
        return reverse_lazy('update', args=[self.kwargs['pk']])
    
class ProductStockUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "main/product/product_stock.html"

    fields = ['stock_quant']

    def form_valid(self, form):
        form.instance.last_stock = timezone.now()
        form.save()
        return super().form_valid(form)
    

    def get_success_url(self):
        return reverse_lazy('update', args=[self.kwargs['pk']])

class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "main/product/product_delete_comfirm.html"
    success_url = reverse_lazy('cate')

# ========== product ========== #
    
# ========== catrgory ========= #
    
class CategoryRedirect(LoginRequiredMixin, RedirectView):
    # 確認連結到的路徑會指向目前 id 最小的 category
    def get_redirect_url(self):
        c = list(Category.objects.order_by('id'))[:1]
        if c:
            return reverse_lazy('c_view', args=[c[0].id])
        return reverse_lazy('c_create')
    
class CategoryView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'main/category/category_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_objects'] = Category.objects.all()
        return context
        
class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'main/category/category_create.html'

    fields = ['name']
    success_url = reverse_lazy('cate')

class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = "main/category/category_update.html"
    fields = ['name']

    def get_success_url(self):
        return reverse_lazy('cate')

class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'main/category/category_delete.html'
    success_url = reverse_lazy('cate')

# ========== catrgory ========= #
    
# ========== Order ============ #
    
class AddToCart(LoginRequiredMixin, FormView):
    form_class = ProductCartForm
    template_name = 'main/order/AddToCart.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['product'] = Product.objects.get(id=self.kwargs['pid'])
        if hasattr(self, 'form'):
            ctx['form'] = self.form
        return ctx
    
    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        p = Product.objects.get(id=self.kwargs['pid'])

        if amount > p.stock_quant - p.ordering :
            # 告訴用戶當前庫存量不足
            form.add_error('amount', '目前庫存不足！')
            # form.errors['下單數量'] = '目前庫存不足！'
            self.form = form
            return super().form_invalid(form)
        else:
        
            product_list = self.request.session.get("product_list", [])
            product_list.append((self.kwargs['pid'], amount, p.price * amount))
            self.request.session["product_list"] = product_list

            p.ordering += amount
            p.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('cate')

# class UpdateCartItem(LoginRequiredMixin, FormView):

class DeleteCartItem(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        idx = self.kwargs['idx']
        product_list = self.request.session.get('product_list', [])

        if idx < len(product_list):
            p = Product.objects.get(id=product_list[idx][0])
            p.ordering -= product_list[idx][1]
            p.save()
            del product_list[idx]

        self.request.session['product_list'] = product_list
        return reverse_lazy('order')
    

class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'main/order/order_create.html'
    fields = []

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        product_list = self.request.session.get("product_list", [])
        # product_list = []
        # self.request.session['product_list'] = []
        order_item_list = []
        sum = 0
        for item in product_list:
            product = Product.objects.get(id=item[0])
            price = product.price * item[1]
            sum += price
            order_item_list.append(
                (product, item[1], price)
            )
        ctx["order_item_list"] = order_item_list
        ctx["sum"] = sum
        return ctx
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        product_list = self.request.session.get("product_list", [])
        form.save()

        for item in product_list:
            oitem = OrderItem(
                amount = item[1],
                sum = item[2], 
                product_id = item[0], 
                order_id = form.instance.id,
            )
            oitem.save()

            p = Product.objects.get(id=item[0])
            p.stock_quant -= item[1]
            p.ordering -= item[1]
            p.save()

            form.instance.sum += item[2]
            form.save()

        self.request.session["product_list"] = []
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('order')
    
class OrderList(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'main/order/orders.html'

class OrderDelete(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = "main/Order/Order_delete.html"
    success_url = reverse_lazy('ordered')

class OrderToExcel(LoginRequiredMixin, TemplateView):

    template_name = 'main/excel.html'

    def get_context_data(self, **kwargs):
        order = Order.objects.get(id=self.kwargs['pk'])
        now = datetime.datetime.now()
        date = now.strftime("%m_%d_%Y")
        time = now.strftime("%m%d%Y_%H%M%S")
        xlsx = 'excel/' + date + '.xlsx'

        if os.path.exists(xlsx):
            wb = openpyxl.load_workbook(xlsx, data_only=True)
        else:
            wb = openpyxl.Workbook() # 開啟新活頁簿
        
        wb.create_sheet("工作表"+time)
        s1 = wb['工作表'+time] 
        s1['A1'].value = '商品名稱'   
        s1['B1'].value = '下單數量'    
        s1['C1'].value = '售價'    
        s1['D1'].value = '總價格'   
        s1['E1'].value = '負責人'    
        s1['F1'].value = '出單時間'  

        s1.column_dimensions['E'].width = 25
        s1.column_dimensions['F'].width = 25

        row = 2
        for item in order.orderitem_set.all():
            s1.cell(row, 1).value = item.product.name
            s1.cell(row, 2).value = item.amount
            s1.cell(row, 3).value = item.product.price
            s1.cell(row, 4).value = item.product.price * item.amount
            s1.cell(row, 5).value = order.owner.username
            s1.cell(row, 6).value = order.time
            row += 1

        wb.save(xlsx)

        return super().get_context_data(**kwargs)
        