from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('about/',views.about,name='about'),
    path('login/',views.login_us,name='login'),
    path('logout/',views.logout_us,name='logout'),
    path('register/',views.register_us,name='register'),
    path('product/<int:pk>', views.product_page,name='product'),
    path('category/<str:foo>', views.categoryy, name="category"),
    path('update_usr/',views.update_usr,name ="update_usr"),
    path('update_info/',views.update_info,name ="update_info"),
    path('search_bar/',views.search_bar,name="search_bar"),
    path('orders/',views.orders,name="orders"),
]