from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('my-profile/', views.my_profile, name='my_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]