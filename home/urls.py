from django.urls import path
from . import views



urlpatterns = [
    path('', views.tips_list, name='home'),
    path('vip', views.vip, name='vip'),
    path('pay-for-admin/', views.pay_for_admin_access, name='payment'),
    path('verify-admin-payment/', views.verify_admin_payment, name='verify_admin_payment'),
    
]