from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),  # Stripe session
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('process_payment/', views.process_payment, name='process_payment'),
]