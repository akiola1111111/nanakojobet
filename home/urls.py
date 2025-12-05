from django.urls import path
from . import views

urlpatterns = [
    path('', views.tips_list, name='home'),  # Free tips for everyone
    path('payment/', views.pay_for_admin_access, name='payment'),  # Payment page
    path('vip/', views.vip, name='vip'),  # VIP page (protected)
    path('verify-payment/', views.verify_admin_payment, name='verify_payment'),
]
