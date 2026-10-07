from django.urls import path

from . import views

app_name = 'kiosk'
urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart_action, name='cart_action'),
    path('review/', views.review_order, name='review'),
    path('review/continue/', views.continue_to_payment, name='continue_payment'),
    path('payment/', views.payment, name='payment'),
    path('payment/<str:method>/', views.payment, name='payment_method'),
    path('payment/<str:method>/complete/', views.pay, name='pay'),
    path('success/', views.success, name='success'),
    path('receipt/', views.receipt, name='receipt'),
    path('receipt/<str:reference>/', views.receipt, name='receipt_reference'),
    path('new-transaction/', views.new_transaction, name='new_transaction'),
]
