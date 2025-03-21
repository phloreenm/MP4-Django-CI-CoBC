from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('my-orders/', views.my_orders, name='my_orders'),
    path('detail/<str:order_number>/', views.order_detail, name='order_detail'),
    path('cancel/<str:order_number>/', views.cancel_order, name='cancel_order'),
    path('summary/', views.orders_summary, name='orders_summary'),
    path('edit/<str:order_number>/', views.order_edit, name='order_edit'),
    path('delete/<str:order_number>/', views.order_delete, name='order_delete'),
    path('alter/<str:order_number>/', views.order_alter, name='order_alter'),
    path('lookup/', views.order_lookup, name='order_lookup'),
    path('confirm/<str:order_number>/', views.confirm_order, name='confirm_order'),
    path('cancel-lookup/<str:order_number>/', views.cancel_order_lookup, name='cancel_order_lookup'),
    path('download/<str:order_number>/<int:product_id>/', views.download_product, name='download_product'),
]