from django.conf.urls import include
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('store/', views.store, name='store'),
    path('register/', views.register, name='register'),
    path('saveenquiry/', views.inquiry, name='saveenquiry'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name="update_item"),
    path('productSearch/', views.productSearch, name="productSearch")
]
