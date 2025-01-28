from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),  # Pagina de Checkout
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),  # Crearea sesiunii Stripe
]