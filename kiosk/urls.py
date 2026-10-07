from django.urls import path

from . import views

app_name = 'kiosk'
urlpatterns = [path('', views.home, name='home'),
               path('cart/', views.cart_action, name='cart_action')]
