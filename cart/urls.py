from django.urls import path
from . import views
urlpatterns = [
    path('',views.cart_sum,name="cart_summary"),
    path('add/', views.cart_add, name="cart_add"),
    path('delete/', views.cart_del, name="cart_del"),
    path('update/', views.cart_upt, name="cart_upt")
]