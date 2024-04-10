from django.urls import path, include
from .views import *

urlpatterns = [
    path('logout/', Logout.as_view()),

    path('', Home.as_view(), name='home'),
    path('thingshere/', ProductList.as_view(), name='list'),
    path('thingshere/detail<int:pk>/', ProductDetail.as_view(), name='detail'),
    path('thingshere/new/', ProductCreate.as_view(), name='create'),
    path('thingshere/info<int:pk>/', ProductUpdate.as_view(), name='update'),
    path('thingshere/more<int:pk>/', ProductStockUpdate.as_view(), name='stock'),
    path('thingshere/byebye<int:pk>/', ProductDelete.as_view(), name='delete'),

    path('category/', CategoryRedirect.as_view(), name='cate'),
    path('category/<int:pk>/', CategoryView.as_view(), name='c_view'),
    path('category/new/', CategoryCreate.as_view(), name='c_create'),
    path('category/delete<int:pk>/', CategoryDelete.as_view(), name='c_del'),
    path('category/update<int:pk>/', CategoryUpdate.as_view(), name='c_update'),

    # path('cart/add/<int:pid>/<int:amount>/', AddToCart),
    path('cart/add/<int:pid>/', AddToCart.as_view(), name='add_to_cart'),
    path('cart/remove/<int:idx>/', DeleteCartItem.as_view(), name='order_item_delete'),
    path('cart/order/', OrderCreate.as_view(), name='order'),
    path('ordered/', OrderList.as_view(), name='ordered'),
    path('ordered/delete/<int:pk>', OrderDelete.as_view(), name='del_order'),

    path('ordered/toexcel/<int:pk>', OrderToExcel.as_view(), name='excel')
]
