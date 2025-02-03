from django.urls import path
from . import views
from .webhooks import webhook

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/<str:order_number>/', views.success, name='success'),  # ✅ Include order_number
    path('cancel/', views.cancel, name='cancel'),
    path('process_payment/', views.process_payment, name='process_payment'),

]

urlpatterns += [
    path('webhook/', webhook, name='webhook'),
]