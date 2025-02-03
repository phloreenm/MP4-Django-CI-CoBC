from django.urls import path
from . import views
from . import webhooks

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success/<str:order_number>/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]

urlpatterns += [
    path('webhook/', webhooks.webhook, name='webhook'),
]