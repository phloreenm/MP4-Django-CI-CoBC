from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success/<str:order_number>/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]