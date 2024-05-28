from django.urls import path
from . import views
urlpatterns = [
    path('payments_success', views.payments_success,name='payments_success'),
    path('checkout', views.checkout, name='checkout'),
    path('info_page',views.info_page,name="info_page"),
    path("order_received",views.order_received,name="order_received"),

]