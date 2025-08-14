from django.urls import  path
from . import views

urlpatterns = [
    path('',views.home ,name='home'),
    path('about/',views.about ,name='about'),
    path('login',views.log_in_user ,name='login'),
    path('logout/',views.log_out_user ,name='Log_out'),
    path('register/',views.register_user ,name='register'),
    path('update_password/',views.update_password ,name='update_password'),
    path('update_user/',views.update_user ,name='update'),
    path('update_info/',views.update_info ,name='update_info'),
    path('product/<int:pk>',views.product,name='product'),
    path('category/<str:foo>',views.category ,name='category'),
    path('category_summary/',views.category_summary ,name='category_summary'),
    path('search/',views.search ,name='search'),
]
