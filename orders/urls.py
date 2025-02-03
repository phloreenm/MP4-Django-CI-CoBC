from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('my-orders/', views.my_orders, name='my_orders'),
    path('detail/<str:order_number>/', views.order_detail, name='order_detail'),
    path('cancel/<str:order_number>/', views.cancel_order, name='cancel_order'),
]